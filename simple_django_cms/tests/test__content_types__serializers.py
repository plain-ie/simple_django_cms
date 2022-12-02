from django.test import TestCase

from ..content_types.serializers import ItemSerializer


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
        'archived': False,
        'deleted': False,
    }


    def test_item_serializer(self):

        serializer_class = ItemSerializer
        serializer = serializer_class(**self.item)

        display_data = serializer.get_display_content(
            language=self.a_code,
            default_language=self.a_code
        )

        self.assertEqual(
            display_data.title,
            self.a_content['title']
        )

        display_data = serializer.get_display_content(
            language=self.b_code,
            default_language=self.a_code
        )

        self.assertEqual(
            display_data.title,
            self.b_content['title']
        )
