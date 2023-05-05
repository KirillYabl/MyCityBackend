from django.test import TestCase
from ..models import FAQ

class TestFAQ(TestCase):

    def test_questions(self):
        question = FAQ.objects.get(id=1)
        self.assertEquals(question.get_absolute_url(), '/faq/1')
