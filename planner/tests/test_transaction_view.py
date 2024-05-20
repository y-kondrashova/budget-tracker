from django.test import TestCase
from django.urls import reverse

TRANSACTION_LIST_URL = reverse("planner:transaction-list")


class PublicTransactionViewTest(TestCase):
    def test_login_required_transaction(self):
        res = self.client.get(TRANSACTION_LIST_URL)
        self.assertNotEqual(res.status_code, 200)
