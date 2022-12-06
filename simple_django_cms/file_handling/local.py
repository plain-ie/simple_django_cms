import os
import re

from pathlib import Path

from django.conf import settings as dj_settings

from .base import BaseFileStorageBackend


class LocalFileStorageBackend(BaseFileStorageBackend):

    def file_exists(self, path):
        return os.path.exists(path)

    def get_full_url(self, path):

        file_path = dj_settings.MEDIA_URL

        if file_path.startswith('/') is False:
            file_path = f'/{file_path}'

        file_path = re.sub(r'\/$', '', file_path)

        if path.startswith('/') is False:
            file_path = f'{file_path}/'

        file_path += path

        return file_path

    def get_full_path(self, path):

        file_path = dj_settings.MEDIA_ROOT

        if path.startswith('/') is False and file_path.endswith('/') is False:
            file_path += '/'

        file_path += path

        return file_path

    def upload(self, path, file):

        full_path = self.get_full_path(path)

        file_path = Path(full_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open('wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return True

    def remove(self, path):

        file_path = self.get_full_path(path)

        if self.file_exists(file_path) is True:
            try:
                os.remove(file_path)
            except OSError as e:
                print(f'Error: {e.filename} - {e.strerror}.')
