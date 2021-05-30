from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ProductManager(models.Manager):
    def get_queryset(self):
        super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    create_by = models.ForeignKey(
        User, related_name='product_creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-create_at', )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
