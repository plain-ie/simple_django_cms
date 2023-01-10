class TransaltionRegistry:

    translations = {}

    def register(self, key, language, translation):
        if key not in self.translations.keys():
            self.translations[key] = {}
        self.translations[key][language] = translation

    def translate(self, key, language):
        try:
            return self.translations[key][language]
        except KeyError:
            pass
        return key
