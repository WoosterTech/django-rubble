from factory import Faker
from factory.django import DjangoModelFactory

from django_rubble.models.number_models import TestNumberedModel


class NumberedModelFactory(DjangoModelFactory):
    class Meta:
        model = TestNumberedModel

    description = Faker("sentence", nb_words=4)
