from typing import List, Optional

from django.forms.models import model_to_dict
from django.shortcuts import reverse

from djantic import ModelSchema

from .. import constants
from ..models import Item, ItemRelation, TranslatableContent


class ItemRelationSchema(ModelSchema):

    class Config:
        exclude = [
            'child',
        ]
        model = ItemRelation


class TranslatableContentSchema(ModelSchema):

    class Config:
        exclude = [
            'item',
        ]
        model = TranslatableContent


class ItemSchema(ModelSchema):

    translatable_contents: List[TranslatableContentSchema]

    class Config:
        exclude = [
            'project',
            'tenant',
            'children',
        ]
        model = Item


class BaseSerializer:

    def __init__(self, object):
        self.object = object
        self.data = self.get_data(self.object)

    def get_data(self, object):
        return ItemSchema.from_orm(object).dict()


class BaseContentType:

    browsable = False
    name = 'base'
    display_name_plural = 'base'
    display_name_singular = 'base'
    serializer = BaseSerializer

    def get_admin_url(self, object):
        return reverse(
            constants.URLNAME_ADMIN_RETRIEVE_ITEMS,
            kwargs={
                'project_id': str(object.project_id),
                'tenant_id': str(object.tenant_id),
                'item_id': str(object.id)
            }
        )

    def matches(self, object):
        return object.content_type == self.name

    def serialize(self, object, **kwargs):

        data = self.serializer(object).data

        data['display_data'] = {
            'title': 'XXX :)',
            'admin_url': self.get_admin_url(object),
            'content_type': self.display_name_singular,
            'tenant': object.tenant.name,
            'created_at': object.created_at
        }

        return data
