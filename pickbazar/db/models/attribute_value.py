# Django imports
from django.db import models

# Module imports
from .base import BaseModel


def default_translated_languages():
    return ["en"]


class AttributeValue(BaseModel):
    attribute = models.ForeignKey('db.Attribute', related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    meta = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"
