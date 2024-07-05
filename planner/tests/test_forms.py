from datetime import date

from django.test import TestCase

from planner.forms import DateSearchForm


class SearchFormTest(TestCase):
    def test_date_search_form_valid(self):
        form_data = {
            "start_date": date(2024, 5, 10),
            "end_date": date(2024, 5, 15)
        }
        form = DateSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["start_date"], date(2024, 5, 10))
        self.assertEqual(form.cleaned_data["end_date"], date(2024, 5, 15))

    def test_date_search_form_empty(self):
        form_data = {
            "start_date": None,
            "end_date": None
        }
        form = DateSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["start_date"], None)
        self.assertEqual(form.cleaned_data["end_date"], None)
