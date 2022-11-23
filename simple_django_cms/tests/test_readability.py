from django.test import TestCase

from . import fleish

class ReadabilityTestCase(TestCase):

    def test_one(self):

        text = ''
        test_text = 'This sentence, taken as a reading passage unto itself, is being used to prove a point. '
        for x in '01234567890':
            text += test_text

        score = 69
        calculated_score = round(fleish.reading_score(text), 0)
        self.assertEquals(score, calculated_score)

    def test_two(self):

        text = ''
        test_text = 'The Australian platypus is seemingly a hybrid of a mammal and reptilian creature. '
        for x in '01234567890':
            text += test_text

        score = 37.5
        calculated_score = round(fleish.reading_score(text), 1)
        self.assertEquals(score, calculated_score)

    def test_three(self):

        text = ''
        test_text = 'The cat sat on the mat. '
        for x in '012345678901234567890012345678900123456789001234567890':
            text += test_text

        score = 116
        calculated_score = round(fleish.reading_score(text), 0)
        self.assertEquals(score, calculated_score)
