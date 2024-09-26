from django.test import TestCase
from django.urls import reverse
from catalog.models import Author

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        number_authors=13
        Author.objects.create(
            first_name=,last_name=
        )
