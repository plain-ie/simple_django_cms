from django.test import TestCase

from ..content_types.serializers import ItemSerializer
from ..models import Item, Project, Tenant, ItemRelation, User, ProjectAdmin, Tenancy, TenantUser


class ContentTypesFormsTestCase(TestCase):

    a_code = 'a'
    b_code = 'b'
    content_type = 'abc'

    a_content = {
        'language': a_code,
        'title': f'{a_code}Hello world',
        'slug': f'{a_code}-hello-world',
        'content': f'{a_code} Content is king'
    }

    b_content = {
        'language': b_code,
        'title': f'{b_code} Hello world',
        'slug': f'{b_code}-hello-world',
        'content': f'{b_code} GA Content is king'
    }

    item = {
        'data': {
            'translatable_contents': [
                a_content,
                b_content,
            ]
        },
        'content_type': content_type,
        'project_id': 1,
        'tenant_id': 1,
        'published': False,
    }


    def test_item_serializer(self):

        user1 = User.objects.create(email='x@xx.com')
        user2 = User.objects.create(email='y@yy.com')

        project = Project.objects.create(name='1')

        ProjectAdmin.objects.create(project=project, user=user1)

        tenant = Tenant.objects.create(name='1')

        Tenancy.objects.create(project=project, tenant=tenant)
        TenantUser.objects.create(tenant=tenant, user=user2)

        item1  = Item.objects.create(**self.item)
        item2  = Item.objects.create(**self.item)

        ItemRelation.objects.create(parent=item1, child=item2, status='a')
        ItemRelation.objects.create(parent=item1, child=item2, status='b')

        # ---

        with self.assertNumQueries(3):
            item = Item.objects.filter(
                id=item2.id
            ).select_related(
                'project',
                'tenant',
            ).prefetch_related(
                'parents__parent',
            ).first()

        with self.assertNumQueries(0):
            serialized_data = ItemSerializer.from_orm(item).dict()

        # ---

        with self.assertNumQueries(1):
            item = Item.objects.get(id=item2.id)

        with self.assertNumQueries(5):
            serialized_data = ItemSerializer.from_orm(item).dict()

        # --

        items = Item.objects.filter(
            id=item2.id
        ).select_related(
            'project',
            'tenant',
        ).prefetch_related(
            'parents__parent',
        )

        serialized_data = ItemSerializer.from_orm(items, many=True)
