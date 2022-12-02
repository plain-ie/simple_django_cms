from datetime import datetime
from typing import List, Optional, Union

from django.shortcuts import reverse

from djantic import ModelSchema
from pydantic import BaseModel

from .. import constants
from ..conf import settings
from ..models import Item, Project, Tenant, ItemRelation


class DisplayDataSerializer(BaseModel):

    content_type: str
    created_at: datetime
    edit_url: str
    published: bool
    site_url: str
    tenant: Union[str, None]
    title: str


class ProjectSerializer(ModelSchema):

    class Config:
        model = Project


class TenantSerializer(ModelSchema):

    class Config:
        model = Tenant


class ItemRelationSerializer(ModelSchema):

    class Config:
        model = ItemRelation


class TranslatableContentSerializer(BaseModel):

    language: str
    title: str
    slug: str
    content: Union[str, None]


class DataSerializer(BaseModel):

    translatable_contents: Optional[List[TranslatableContentSerializer]]


class ItemSerializer(ModelSchema):

    class Config:
        model = Item

    data: Union[DataSerializer, None]

    project: ProjectSerializer
    tenant: Union[TenantSerializer, None]

    parents: Optional[List[ItemRelationSerializer]]

    published_at: Union[datetime, None]
    created_at: Union[datetime, None]
    updated_at: Union[datetime, None]

    def get_content_type(self, language, default_language):
        return self.content_type

    def get_created_at(self):
        return self.created_at

    def get_edit_url(self):
        return reverse(
            constants.URLNAME_ADMIN_RETRIEVE_ITEMS,
            kwargs={
                'project_id': str(self.project.id),
                'tenant_id': str(self.tenant.id),
                'item_id': str(self.id)
            }
        )

    def get_published(self):
        return self.published

    def get_site_url(self, language, default_language):
        return '#'

    def get_tenant(self):
        return self.tenant.name

    def get_title(self, language, default_language):
        return self.get_translated_content(language, default_language).title

    def get_translated_content(self, language, default_language):

        _content = None
        _default_content = None

        for translatable_content in self.data.translatable_contents:

            if translatable_content.language == language:
                _content = translatable_content

            if translatable_content.language == default_language:
                _default_content = translatable_content

        if language == default_language:
            return _default_content

        if _content is not None:
            return _content

        return _default_content

    def get_display_data(
    	self,
        language=settings.DEFAULT_LANGUAGE,
        default_language=settings.DEFAULT_LANGUAGE,
    ):

        data = {
            'content_type': self.get_content_type(language, default_language),
            'created_at': self.get_created_at(),
            'edit_url': self.get_edit_url(),
            'published': self.get_published(),
            'site_url': self.get_site_url(language, default_language),
            'tenant': self.get_tenant(),
            'title': self.get_title(language, default_language),
        }

        return DisplayDataSerializer(**data)
