from rest_framework import serializers

from ..models import Category, Smartphones, Bricks, BuildingBlocks, Customer, Order


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]


class BaseProductSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)
    quantity = serializers.DecimalField(max_digits=9, decimal_places=0, required=True)
    size = serializers.CharField(required=True)


class SmartphoneSerializer(BaseProductSerializer, serializers.ModelSerializer):

    diagonal = serializers.CharField(required=True)
    colour = serializers.CharField(required=True)
    sd = serializers.BooleanField(required=True)
    sd_volume_max = serializers.CharField(required=True)

    class Meta:
        model = Smartphones
        fields = '__all__'


class BrickSerializer(BaseProductSerializer, serializers.ModelSerializer):

    factory = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    material = serializers.CharField(required=True)
    voidness = serializers.CharField(required=True)
    surface = serializers.CharField(required=True)
    colour = serializers.CharField(required=True)
    chamfer = serializers.BooleanField(required=True)
    endurance = serializers.CharField(required=True)
    frost_resistance = serializers.CharField(required=True)
    water_absorption = serializers.CharField(required=True)
    weight = serializers.DecimalField(max_digits=9, decimal_places=3, required=True)
    packaging = serializers.CharField(required=True)
    warehouse = serializers.CharField(required=True)

    class Meta:
        model = Bricks
        fields = '__all__'


class BuildingBlockSerializer(BaseProductSerializer, serializers.ModelSerializer):

    factory = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    material = serializers.CharField(required=True)
    colour = serializers.CharField(required=True)
    density = serializers.CharField(required=True)
    endurance = serializers.CharField(required=True)
    thermal_conductivity = serializers.CharField(required=True)
    frost_resistance = serializers.CharField(required=True)
    weight = serializers.DecimalField(max_digits=9, decimal_places=3, required=True)
    packaging = serializers.CharField(required=True)
    warehouse = serializers.CharField(required=True)

    class Meta:
        model = BuildingBlocks
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'
