import logging
import sys
from typing import TYPE_CHECKING, Any, Literal

from django import get_version
from django.apps import apps
from django.views import View
from neapolitan.views import Role
from pydantic import BaseModel, field_validator, model_serializer

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise

logger = logging.getLogger(__name__)


class DuplicateAppError(Exception):
    pass


class NotRegisteredError(Exception):
    pass


class ModelLink(BaseModel):
    name: str
    role: Role
    view_class: type[View]
    url: str

    def get_url(self):
        return self.role.reverse(self.view_class)

    @model_serializer
    def get_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "view_class": self.view_class,
            "url": self.get_url(),
        }


class ModelViewsConfiguration(BaseModel):
    verbose_name: str
    views_class: type[View]
    menu_roles: list[Role] = [Role.LIST, Role.CREATE]


class ProjectApp(BaseModel):
    name: str | Any
    registered_models: list[tuple[str, type[View]] | ModelViewsConfiguration] = []

    @field_validator("name", mode="before")
    @classmethod
    def str_from_str_or_promise(cls, value: "StrOrPromise | str") -> str:
        return str(value) if not isinstance(value, str) else value

    def get_model(self, model_name: str):
        return apps.get_model(self.name, model_name)

    def get_actions(self) -> list[ModelLink]:
        action_links = []
        for model in self.registered_models:
            views_config = (
                model
                if isinstance(model, ModelViewsConfiguration)
                else ModelViewsConfiguration(
                    verbose_name=model[0], views_class=model[1]
                )
            )
            if Role.LIST in views_config.menu_roles:
                list_link = ModelLink(
                    name=views_config.verbose_name,
                    role=Role.LIST,
                    view_class=views_config.views_class,
                    url="",
                )
                action_links.append(list_link)
            if Role.CREATE in views_config.menu_roles:
                create_link = ModelLink(
                    name=views_config.verbose_name,
                    role=Role.CREATE,
                    view_class=views_config.views_class,
                    url="",
                )
                action_links.append(create_link)

        return action_links

    def register(self, model: tuple[str, type[View]] | ModelViewsConfiguration):
        """Register a model to the app.

        Arguments:
          model: tuple of `(model_name, view_class)`
        """
        if not isinstance(model, ModelViewsConfiguration):
            msg = f"{model[0]} being cast as ModelViewsConfiguration"
            logger.debug(msg)

            model = ModelViewsConfiguration(verbose_name=model[0], views_class=model[1])
        self.registered_models.append(model)


class ProjectRegistry(BaseModel):
    apps: list[ProjectApp] = []
    _django_version: str | None = None
    _python_version: (
        tuple[int, int, int, Literal["alpha", "beta", "candidate", "final"], int] | None
    ) = None
    project_version: str = ""

    @property
    def django_version(self):
        if self._django_version is None:
            self._django_version = get_version()

        return self._django_version

    @property
    def python_version(self) -> str:
        if self._python_version is None:
            self._python_version = sys.version_info
        # "major.minor.micro_releaselevel" format e.g. "3.9.7_final"
        return (
            f"{self._python_version.major}."
            f"{self._python_version.minor}.{self._python_version.micro}_"
            f"{self._python_version.releaselevel}"
        )

    def register(self, app: ProjectApp | tuple[str, tuple[str, type[View]]]):
        """Registers a model/app with the project.

        Arguments:
          app: definition of project "application", either as ProjectApp object or as
          a tuple of `(app_name, (model_name, view_class))`
        """
        if not isinstance(app, ProjectApp):
            app_name, app_model = app
            if not self.is_registered(app_name):
                app = ProjectApp(name=app_name)
            else:
                app = self.get_app_by_name(app_name)
            app.register(app_model)
        self.apps.append(app)

    def is_registered(self, app_name: str) -> bool:
        registered_apps = self.get_app_names()
        return app_name in registered_apps

    def get_app_names(self):
        return [app.name for app in self.apps]

    def get_app_by_name(self, app_name: str) -> ProjectApp:
        named_apps = [app for app in self.apps if app_name in app.name]
        if len(named_apps) > 1:
            raise DuplicateAppError
        if len(named_apps) != 1:
            raise NotRegisteredError
        return named_apps[0]

    def get_context_data(self, *args, **kwargs):
        return [
            {
                "app_name": app.name,
                "views": [action.model_dump() for action in app.get_actions()],
            }
            for app in self.apps
        ]
