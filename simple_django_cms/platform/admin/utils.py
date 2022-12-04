from django.contrib import messages
from django.shortcuts import reverse

from ... import constants
from ...clients.internal.content_types import ContentTypeQuerySetClient


def create_message(level, request, text):
    msg = getattr(messages, level, None)
    if msg is None:
        raise ValueError(f'Message tag "{level}" does not exist')
    msg(request, text)


def get_management_link_delete_item(
    project_id,
    tenant_id,
    item_id,
    language,
    default_language
):
    return {
        'href': get_item_delete_url(project_id, tenant_id, item_id),
        'text': 'Delete'
    }


def get_management_link_new_item(
    project_id,
    tenant_id,
    content_type,
    language,
    default_language
):
    return {
        'href': get_new_item_url(project_id, tenant_id, content_type),
        'text': 'Create new'
    }


def get_management_link_toggle_publish_item(
    project_id,
    tenant_id,
    item_id,
    published,
    language,
    default_language
):

    text = 'Unpublish'
    if published is False:
        text = 'Publish'

    return {
        'href': get_item_toggle_publish_url(project_id, tenant_id, item_id),
        'text': text
    }


def get_management_link_project_items(
    project_id,
    language,
    default_language
):
    return {
        'href': get_project_items_url(project_id),
        'text': 'Browse items'
    }


def get_management_link_create_item_previous(
    project_id,
    content_type,
    language,
    default_language
):

    href = '#'
    text = 'Back'
    ct = ContentTypeQuerySetClient().get_content_type(content_type)

    if ct.has_tenant is True:
        href= reverse(
            constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_TENANT,
            kwargs={
                'content_type': content_type,
                'project_id': project_id
            }
        )
        text = 'Change tenant'
    else:
        href= reverse(
            constants.URLNAME_ADMIN_CREATE_ITEMS_SELECT_CONTENT_TYPE,
            kwargs={
                'project_id': project_id
            }
        )
        text = 'Change content type'

    return {
        'href': href,
        'text': text
    }


def get_item_admin_url(project_id, tenant_id, content_type, item_id):

    ct = ContentTypeQuerySetClient().get_content_type(content_type)

    if ct.has_tenant is True:
        return reverse(

            constants.URLNAME_ADMIN_RETRIEVE_ITEMS,
            kwargs={
                'project_id': project_id,
                'tenant_id': tenant_id,
                'item_id': item_id
            }
        )

    return reverse(
        constants.URLNAME_ADMIN_RETRIEVE_PROJECT_ITEMS,
        kwargs={
            'project_id': project_id,
            'item_id': item_id
        }
    )


def get_new_item_url(project_id, tenant_id, content_type):

    ct = ContentTypeQuerySetClient().get_content_type(content_type)

    if ct.has_tenant is True:
        return reverse(
            constants.URLNAME_ADMIN_CREATE_ITEMS,
            kwargs={
                'project_id': project_id,
                'tenant_id': tenant_id,
                'content_type': content_type
            }
        )

    return reverse(
        constants.URLNAME_ADMIN_CREATE_PROJECT_ITEMS,
        kwargs={
            'project_id': project_id,
            'content_type': content_type
        }
    )


def get_project_items_url(project_id):
    return reverse(
        constants.URLNAME_ADMIN_LIST_ITEMS,
        kwargs={'project_id': project_id}
    )


def get_item_delete_url(project_id, tenant_id, item_id):

    urlname = constants.URLNAME_ADMIN_DELETE_PROJECT_ITEMS
    kwargs = {
        'project_id': project_id,
        'item_id': item_id
    }

    if tenant_id is not None:
        urlname = constants.URLNAME_ADMIN_DELETE_ITEMS
        kwargs['tenant_id'] = tenant_id

    return reverse(urlname, kwargs=kwargs)


def get_item_toggle_publish_url(project_id, tenant_id, item_id):

    urlname = constants.URLNAME_ADMIN_TOGGLE_PUBLISH_PROJECT_ITEMS
    kwargs = {
        'project_id': project_id,
        'item_id': item_id
    }

    if tenant_id is not None:
        urlname = constants.URLNAME_ADMIN_TOGGLE_PUBLISH_ITEMS
        kwargs['tenant_id'] = tenant_id

    return reverse(urlname, kwargs=kwargs)
