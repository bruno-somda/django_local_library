import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from catalog.models import Author,Book,Genre,BookInstance,Language

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        number_authors=13
        for author_id in range(number_authors):

            Author.objects.create(
                first_name= f' Christian {author_id}',last_name= f' Surname {author_id}'
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/authors/")
        self.assertEqual(response.status_code,200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code,200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'catalog/author_list.html')
    
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code,200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(len(response.context["author_list"])==10)
    
    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') +"?page=2")
        self.assertEqual(response.status_code,200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)

class LoanedBookInstancesByUserListViewTest(TestCase):

    def setUp(cls):
        test_user1 = User.objects.create(sername='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create(sername='testuser2', password='2X<ISRUkw+tuK')
        test_user1.save()
        test_user2.save()
        
        test_author =Author.objects.create(first_name='John', last_name='Smith')
