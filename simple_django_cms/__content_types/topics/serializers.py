from django.shortcuts import reverse

from ... import constants

from ..serializers import ItemSerializer


class TopicSerializer(ItemSerializer):

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
