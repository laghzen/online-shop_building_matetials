from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone

import sys
from PIL import Image
from io import BytesIO

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get("with_respect_to")
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by("-id")[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Смартфоны': 'smartphones__count',
        'Кирпичи': 'bricks__count',
        'Строительные блоки': 'buildingblocks__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count("smartphones", "buildingblocks", "bricks")
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (900, 900)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    quantity = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="Количество")
    size = models.CharField(max_length=255, verbose_name="Размер", null=True)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.width < min_width or img.height < min_height:
            raise MinResolutionErrorException("Разрешение изображения меньше минимального!")
        else:
            if img.width > img.height:
                width_new = max_width
                height_new = (max_width * img.height) // img.width
            else:
                width_new = (max_height * img.width) // img.height
                height_new = max_height
            new_img = img.convert("RGB")
            resized_new_img = new_img.resize((width_new, height_new))

            base_img_white = Image.open('media/base/white_background.png')
            base_img_white.paste(resized_new_img, (500-width_new//2, 500-height_new//2))
            resized_new_img = base_img_white

            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=95)
            filestream.seek(0)
            name = '{}.{}'.format(*self.image.name.split('.'))
            self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)


class Bricks(Product):
    factory = models.CharField(max_length=255, verbose_name="Завод")
    type = models.CharField(max_length=255, choices=[("facing", "Облицовочный"),
                                                     ("construction", "Строительный"),
                                                     ("warm_ceramics", "Теплая керамика")],
                            verbose_name="Тип")
    material = models.CharField(max_length=255, verbose_name="Материал")
    voidness = models.CharField(max_length=255, choices=[("full-bodied", "Полнотелый"),
                                                         ("hollow", "Пустотелый")],
                                verbose_name="Пустотность")
    surface = models.CharField(max_length=255, choices=[("smooth", "Гладкая"),
                                                        ("grainy", "Зернистая")],
                               verbose_name="Поверхность")
    colour = models.CharField(max_length=255, verbose_name="Цвет")
    chamfer = models.BooleanField(default=True, verbose_name="Фаска")
    endurance = models.CharField(max_length=255, verbose_name="Прочность")
    frost_resistance = models.CharField(max_length=255, verbose_name="Морозостойкость")
    water_absorption = models.CharField(max_length=255, verbose_name="Водопоглощение")
    weight = models.DecimalField(max_digits=9, decimal_places=3, verbose_name="Вес 1 шт, кг")
    packaging = models.CharField(max_length=255, verbose_name="Упаковка")
    warehouse = models.CharField(max_length=255, verbose_name="Склад")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class BuildingBlocks(Product):
    factory = models.CharField(max_length=255, verbose_name="Завод")
    type = models.CharField(max_length=255, choices=[("aerated_concrete", "Газобетонный"),
                                                     ("ceramic", "Керамический"),
                                                     ("expanded_clay_concrete", "Керамзитобетонный"),
                                                     ("foundation_fbs", "Фундаментные ФБС"),
                                                     ("concrete", "Бетонный"),
                                                     ("pazogrebnevye", "Пазогребневый")],
                            verbose_name="Тип")
    material = models.CharField(max_length=255, verbose_name="Материал")
    colour = models.CharField(max_length=255, verbose_name="Цвет")
    density = models.CharField(max_length=255, verbose_name="Плотность")
    endurance = models.CharField(max_length=255, verbose_name="Прочность")
    thermal_conductivity = models.CharField(max_length=255, verbose_name="Теплопроводность")
    frost_resistance = models.CharField(max_length=255, verbose_name="Морозостойкость")
    weight = models.DecimalField(max_digits=9, decimal_places=3, verbose_name="Вес 1 шт, кг")
    packaging = models.CharField(max_length=255, verbose_name="Упаковка")
    warehouse = models.CharField(max_length=255, verbose_name="Склад")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphones(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    colour = models.CharField(max_length=255, verbose_name="Цвет")
    sd = models.BooleanField(default=True, verbose_name='Наличие SD')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраиваемой памяти'
    )

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    # @property
    # def sd(self):
    #     if self.sd:
    #         return 'Да'
    #     return 'Нет'


class CartProduct(models.Model):
    user = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey("Customer", null=True, verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="Общая цена")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name="Адрес", null=True, blank=True)
    orders = models.ManyToManyField('Order', related_name='related_customer', verbose_name='Заказы покупателя')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )
    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    cart = models.ForeignKey(Cart, verbose_name='Корзина', null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='related_orders', verbose_name="Покупатель", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=1024, verbose_name="Адрес", null=True, blank=True)
    status = models.CharField(
        max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
