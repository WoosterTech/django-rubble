from typing import Literal

try:
    from infisical_client import (
        AuthenticationOptions,
        ClientSettings,
        GetSecretOptions,
        InfisicalClient,
        UniversalAuthMethod,
    )
except ImportError as e:
    msg = 'Unable to import infisical_client, did you install the "secrets" extra?'
    raise ImportError(msg) from e
from os import getenv

from pydantic import BaseModel, SecretStr


class LongSecretStr(SecretStr):
    def __repr__(self):
        value = self.get_secret_value()
        return f"LongSecretStr('{value[:5]}***{value[-5:]}')"


class Secrets(BaseModel):
    """Safely retrieve secrets from Infisical.

    Does not expose the client secret in the repr.

    Attributes:
        client_id (str): The Infisical client ID. Defaults to the INFISICAL_CLIENT_ID
        client_secret (LongSecretStr): The Infisical client secret. Defaults to the
            INFISICAL_CLIENT_SECRET
        project_id (str): The Infisical project ID. Defaults to the INFISICAL_PROJECT_ID
        environment (Literal["prod", "dev", "staging"]): The Infisical environment.
            Defaults to the INFISICAL_ENVIRONMENT or "dev"
        debug (bool): Whether to run in debug mode. Defaults to False
    """

    client_id: str = getenv("INFISICAL_CLIENT_ID")
    client_secret: LongSecretStr = getenv("INFISICAL_CLIENT_SECRET")
    project_id: str = getenv("INFISICAL_PROJECT_ID")
    environment: Literal["prod", "dev", "staging"] = getenv(
        "INFISICAL_ENVIRONMENT", default="dev"
    )
    debug: bool = False
    _client: InfisicalClient | None = None

    def create_client(self):
        client_secret = self.client_secret.get_secret_value()
        universal_auth = UniversalAuthMethod(
            client_id=self.client_id, client_secret=client_secret
        )

        self._client = InfisicalClient(
            ClientSettings(auth=AuthenticationOptions(universal_auth=universal_auth)),
            debug=self.debug,
        )

    @property
    def client(self):
        if self._client is None:
            self.create_client()
        return self._client

    def get_secret(
        self, secret_name: str, *, environment: str | None = None, mask: bool = False
    ):
        """Retrieve a secret from Infisical.

        Args:
            secret_name: The name of the secret to retrieve.
            environment: The environment to retrieve the secret from. Defaults to the
                environment set in the class.
            mask: Whether to mask the secret in the repr. Defaults to False.
        """
        if mask:
            msg = "Masking is not yet implemented"
            raise NotImplementedError(msg)
        if self._client is None:
            self.create_client()
        if environment is None:
            environment = self.environment
        return self._client.getSecret(
            options=GetSecretOptions(
                environment=environment,
                project_id=self.project_id,
                secret_name=secret_name,
            )
        )
