from django.test import TestCase

from ..readability.analyzer import reading_score


class ReadabilityTestCase(TestCase):

    def test_one(self):

        text = 'This sentence, taken as a reading passage unto itself, is being used to prove a point. '

        score = 69
        calculated_score = round(reading_score(text), 0)
        self.assertEquals(score, calculated_score)

    def test_two(self):

        text = 'The Australian platypus is seemingly a hybrid of a mammal and reptilian creature. '

        score = 37.5
        calculated_score = round(reading_score(text), 1)
        self.assertEquals(score, calculated_score)

    def test_three(self):

        text = 'The cat sat on the mat. '

        score = 116
        calculated_score = round(reading_score(text), 0)
        self.assertEquals(score, calculated_score)
