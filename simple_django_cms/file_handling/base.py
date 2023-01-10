class BaseFileStorageBackend:

    def __init__(self):
        self.setup()

    def file_exists(self, path):
        raise NotImplemented()

    def get_full_url(self, path):
        raise NotImplemented()

    def get_full_path(self, path):
        raise NotImplemented()

    def upload(self, path, file):
        raise NotImplemented()

    def remove(self, path):
        raise NotImplemented()

    def setup(self):
        pass
