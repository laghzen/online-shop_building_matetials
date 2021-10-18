from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphones


register = template.Library()


TABLE_HEAD = '''
            <table class="table table-sm table-striped">
                <tbody>
            '''

TABLE_TAIL = '''
                </tbody>
            </table>
            '''

TABLE_CONTENT = '''
                    <tr>
                        <td>{name}</td>
                        <td>{value}</td>
                    </tr>
                '''

PRODUCT_SPEC = {
    'bricks': {
        "Завод": 'factory',
        "Тип": 'type',
        "Материал": 'material',
        "Пустотность": 'voidness',
        "Поверхность": 'surface',
        "Цвет": 'colour',
        "Фаска": 'chamfer',
        "Прочность": 'endurance',
        "Морозостойкость": 'frost_resistance',
        "Водопоглощение": 'water_absorption',
        "Вес 1 шт, кг": 'weight',
        "Упаковка": 'packaging',
        "Склад": 'warehouse'
    },
    'buildingblocks': {
        "Завод": 'factory',
        "Тип": 'type',
        "Материал": 'material',
        "Цвет": 'colour',
        "Плотность": 'density',
        "Прочность": 'endurance',
        "Теплопроводность": 'thermal_conductivity',
        "Морозостойкость": 'frost_resistance',
        "Вес 1 шт, кг": 'weight',
        "Упаковка": 'packaging',
        "Склад": 'warehouse'
    },
    'smartphones': {
        "Диагональ": 'diagonal',
        "Цвет": 'colour',
        "Наличие SD": 'sd',
        "Максимальный объем встраиваемой памяти": 'sd_volume_max'
    }
}

def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphones):
        if not product.sd:
            PRODUCT_SPEC['smartphones'].pop('Максимальный объем встраиваемой памяти')
        else:
            PRODUCT_SPEC['smartphones']['Максимальный объем встраиваемой памяти'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
