from ..conf import settings


def translate(key, language):
    registry = settings.TRANSLATION_REGISTRY
    return registry.translate(key, language)


def register(key, language, translation):
    registry = settings.TRANSLATION_REGISTRY
    return registry.register(key, language, translation)
