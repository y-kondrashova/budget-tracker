from django.test import TestCase
from django.urls import reverse

TRANSFER_LIST_URL = reverse("planner:transfer-list")


class PublicTransactionViewTest(TestCase):
    def test_login_required_transaction(self):
        res = self.client.get(TRANSFER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)
