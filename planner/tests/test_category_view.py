from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from planner.models import Category

CATEGORY_LIST_URL = reverse("planner:category-list")


class PublicCategoryViewTest(TestCase):
    def test_login_required_category(self):
        res = self.client.get(CATEGORY_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCategoryViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_category(self):
        Category.objects.create(title="Test category", owner=self.user)
        Category.objects.create(title="Test2", owner=self.user)
        res = self.client.get(CATEGORY_LIST_URL)
        categories = Category.objects.filter(owner=self.user)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["category_list"]), list(categories))
        self.assertContains(res, "Test category")
        self.assertContains(res, "Test2")
