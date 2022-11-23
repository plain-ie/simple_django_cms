class BaseSerializer:
    pass


class BaseContentType:

    browsable = False
    name = 'base'

    def serialize(self, data, many=False, **kwargs):
        raise NotImplemented()
