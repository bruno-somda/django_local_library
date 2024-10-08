import datetime
from django.test import TestCase
from catalog.forms import RenewBookForm
from django.utils import timezone


class ReswBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.field['renewal_date'].label == None or
        form.field['renewal_date'].label=='renewal_date')
    
    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.field['renewal_date'].help_text,
        'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date':date})
        self.assertFalse(form.is_valid())
    
    def test_renew_form_date_in_past(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date':date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() 
        form = RenewBookForm(data={'renewal_date':date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_in_past(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4) 
        form = RenewBookForm(data={'renewal_date':date})
        self.assertTrue(form.is_valid())