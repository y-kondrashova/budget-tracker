from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from planner.models import Transaction, Budget, Category

TRANSACTION_LIST_URL = reverse("planner:transaction-list")


class PublicTransactionViewTest(TestCase):
    def test_login_required_transaction(self):
        res = self.client.get(TRANSACTION_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTransactionViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_transaction(self):
        budget = Budget.objects.create(title="Test_budget",
                                       balance=50,
                                       owner=self.user)
        category = Category.objects.create(title="Test category",
                                           owner=self.user)

        transaction1 = Transaction.objects.create(transaction_type="Income",
                                                  amount=100,
                                                  budget=budget,
                                                  category=category)
        transaction2 = Transaction.objects.create(transaction_type="Outcome",
                                                  amount=50,
                                                  budget=budget,
                                                  category=category)
        res = self.client.get(TRANSACTION_LIST_URL)
        transactions = Transaction.objects.filter(budget__owner=self.user)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["transaction_list"]),
                         list(transactions))
        self.assertContains(res, transaction1.amount)
        self.assertContains(res, transaction2.amount)
