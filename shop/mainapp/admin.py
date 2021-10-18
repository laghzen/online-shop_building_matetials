from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

from PIL import Image


class SmartphonesAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: #000000'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


class ImageSaveAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            "<span style='color:red;'>Изображение с разрешением меньше {}x{} не будет загружено!<br></span>"
            "<span style='color:red;'>Изображение с разрешением больше {}x{} будет сжато!<br></span>"
            "<span style='color:red;'>Размер изображения не должен превышать 3MB!</span>".format(
                *Product.MIN_RESOLUTION, *Product.MAX_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data["image"]
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        print(img, image, '-----------------------------------------')
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должен превышать 3MB!")
        if img.width < min_width or img.height < min_height:
            raise ValidationError("Разрешение изображения меньше минимального!")
        return image


class BricksAdmin(admin.ModelAdmin):
    form = ImageSaveAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="bricks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BuildingBlocksAdmin(admin.ModelAdmin):
    form = ImageSaveAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="buildingblocks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphonesAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'
    # form = ImageSaveAdminForm
    form = SmartphonesAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Bricks, BricksAdmin)
admin.site.register(BuildingBlocks, BuildingBlocksAdmin)
admin.site.register(Smartphones, SmartphonesAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
