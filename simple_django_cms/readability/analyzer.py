from . import utils


class TextAnalyzerWord:

    def __init__(self, text):
        self.text = text
        self.analyzer = TextAnalyzer(self.text)

    @property
    def analyze(self):
        reading_ease = self.analyzer.reading_ease
        html = f'<span class="text-analyzer text-analyzer-word {reading_ease}">{self.text}</span>'
        return {
            'html': html,
            'reading_ease': reading_ease,
            'text': self.text
        }


class TextAnalyzerSentence:

    def __init__(self, text):
        self.text = text
        self.analyzer = TextAnalyzer(self.text)

    @property
    def analyze(self):
        reading_ease = self.analyzer.reading_ease
        html = f'<span class="text-analyzer text-analyzer-sentence {reading_ease}">{self.text}</span>'
        return {
            'html': html,
            'reading_ease': reading_ease,
            'text': self.text,
        }


class TextAnalyzer:

    text = ''

    sentences = []
    syllables = []
    words = []

    sentences_count = 0
    syllables_count = 0
    words_count = 0

    def __init__(self, text):
        self.text = text
        self.sentences = utils.get_sentences(self.text)
        self.syllables = utils.get_syllables(self.text)
        self.words = utils.get_words(self.text)
        self.sentences_count = len(self.sentences)
        self.syllables_count = len(self.syllables)
        self.words_count = len(self.words)

    @property
    def reading_score(self):
        try:
            score = 206.835 - (1.015 * (self.words_count/self.sentences_count)) - (84.6 * (self.syllables_count/self.words_count))
        except ZeroDivisionError:
            return None
        return score

    @property
    def reading_ease(self):

        score = self.reading_score

        if score is None:
            return None

        if score >= 90:
            return 'very_easy'
        elif score >= 80 and score < 90:
            return 'easy'
        elif score >= 70 and score < 80:
            return 'fairly_easy'
        elif score >= 60 and score < 70:
            return 'plain_english'
        elif score >= 50 and score < 60:
            return 'fairly_difficult'
        elif score >= 30 and score < 50:
            return 'difficult'
        elif score >= 10 and score < 30:
            return 'very_difficult'

        return 'extremely_difficult'

    @property
    def grade_level(self):
        try:
            score = 0.39 * (self.words_count/self.sentences_count)
            score += 11.8 * (self.syllables_count/self.words_count)
            score -= 15.59
        except ZeroDivisionError:
            return None
        return score

    @property
    def analyze(self):

        sentences = []
        for x in self.sentences:
            sentences.append(TextAnalyzerSentence(x).analyze)

        data = {
            'grade_level': self.grade_level,
            'reading_ease': self.reading_ease,
            'reading_score': self.reading_score,
            'sentences': sentences
        }

        return data

def reading_score(text):
    return TextAnalyzer(text).reading_score


def ease(text):
    return TextAnalyzer(text).reading_ease


def grade_levels(text):
    return TextAnalyzer(text).grade_level


def analyze(text):
    return TextAnalyzer(text).analyze
