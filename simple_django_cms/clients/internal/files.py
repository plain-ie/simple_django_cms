import uuid

from ...conf import settings


class FileClient:

    def get_file_url(self, path):
        return settings.FILE_HANDLING_BACKEND.get_full_url(path)

    def extensions_match(self, file_name_1, file_name_2):
        extension_1 = file_name_1.split('.')[-1]
        extension_2 = file_name_2.split('.')[-1]
        return extension_1 == extension_2

    def get_file_name(self, name):
        return f'{uuid.uuid4().hex}-{name}'

    def get_file_path(self, project_id, tenant_id, name):

        file_name = self.get_file_name(name)

        if project_id is None:
            project_id = '0'

        if tenant_id is None:
            tenant_id = '0'

        return f'/projects/{project_id}/tenants/{tenant_id}/{file_name}'

    def file_exists(self, path):
        settings.FILE_HANDLING_BACKEND.file_exists(path)

    def upload(self, path, file):
        settings.FILE_HANDLING_BACKEND.upload(path, file)

    def remove(self, path):
        settings.FILE_HANDLING_BACKEND.remove(path)
