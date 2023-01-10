from django.shortcuts import reverse

from pydantic import BaseModel

from .... import constants

from ..serializers import ItemSerializer


class RedirectDataSerializer(BaseModel):

    source: str
    redirect_to: str


class RedirectSerializer(ItemSerializer):

    data: RedirectDataSerializer

    def get_edit_url(self):
        return reverse(
            constants.URLNAME_ADMIN_RETRIEVE_PROJECT_ITEMS,
            kwargs={
                'project_id': str(self.project.id),
                'item_id': str(self.id)
            }
        )

    def get_tenant(self):
        return None

    def get_title(self, language, default_language):
        return self.data.source
