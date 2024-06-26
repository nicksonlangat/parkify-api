import uuid
from itertools import chain

from django.db import models


class BaseManager(models.Manager):
    pass


class BaseModel(models.Model):
    """Parent model for all models in the project."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = [
            "-updated_at",
        ]

    def to_dict(self, exclude=None, include=None):
        """Custom implementation of Django's model_to_dict()."""

        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        for f in opts.many_to_many:
            if exclude and f.name in exclude:
                continue
            data[f.name] = [i.to_dict() for i in f.value_from_object(self)]
        if include:
            for f in include:
                data[f] = getattr(self, f)
        return data
