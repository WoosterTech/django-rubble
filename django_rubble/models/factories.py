from factory import Faker
from factory.django import DjangoModelFactory

from django_rubble.models.numbered_model import TestNumberedModel


class NumberedModelFactory(DjangoModelFactory):
    class Meta:
        model = TestNumberedModel

    description = Faker("sentence", nb_words=4)
