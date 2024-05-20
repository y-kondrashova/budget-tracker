from django.test import TestCase
from django.urls import reverse

BUDGET_LIST_URL = reverse("planner:budget-list")


class PublicBudgetViewTest(TestCase):
    def test_login_required_budget(self):
        res = self.client.get(BUDGET_LIST_URL)
        self.assertNotEqual(res.status_code, 200)
