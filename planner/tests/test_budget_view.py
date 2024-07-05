from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from planner.models import Budget

BUDGET_LIST_URL = reverse("planner:budget-list")


class PublicBudgetViewTest(TestCase):
    def test_login_required_budget(self):
        res = self.client.get(BUDGET_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateBudgetViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_budget(self):
        Budget.objects.create(title="Test_budget",
                              balance=50,
                              owner=self.user)
        Budget.objects.create(title="Test_budget2",
                              balance=100,
                              owner=self.user)
        res = self.client.get(BUDGET_LIST_URL)
        budgets = Budget.objects.filter(owner=self.user)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["budget_list"]), list(budgets))
        self.assertContains(res, "Test_budget")
        self.assertContains(res, "Test_budget2")
