from django.test import TestCase
from .models import Category, Product

# Create your tests here.


class TestCategoryModel(TestCase):

    def setUp(self) -> None:
        self.data1 = Category.objects.create(name='Clother', slug='clother')

    def test_category_model_entry(self) -> None:
        data = self.data1
        self.assertTrue(isinstance(data, Category))
