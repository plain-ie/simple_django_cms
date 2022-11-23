class TransaltionRegistry:

    translations = {}

    def __init__(self):
        pass

    def register(self, key, language, translation):
        if key not in self.translations.keys():
            self.translations[key] = {}
        self.translations[key][language] = translation

    def bulk_register(self, list_of_translations):
        for x in list_of_translations:
            self.register(*x)

    def translate(self, key, language):
        try:
            return self.translations[key][language]
        except KeyError:
            pass
        return key
