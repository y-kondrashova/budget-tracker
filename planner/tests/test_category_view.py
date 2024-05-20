from django.test import TestCase
from django.urls import reverse


CATEGORY_LIST_URL = reverse("planner:category-list")


class PublicCategoryViewTest(TestCase):
    def test_login_required_category(self):
        res = self.client.get(CATEGORY_LIST_URL)
        self.assertNotEqual(res.status_code, 200)
