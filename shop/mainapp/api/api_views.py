from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from .serializers import (CategorySerializer,
                          SmartphoneSerializer,
                          CustomerSerializer,
                          BrickSerializer,
                          BuildingBlockSerializer)
from ..models import (Category,
                      Smartphones,
                      Customer,
                      Bricks,
                      BuildingBlocks)


class CategoryPagination(PageNumberPagination):

    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('items', data)
        ]))


class CategoryAPIView(ListCreateAPIView, RetrieveUpdateAPIView):

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    queryset = Category.objects.all()
    #lookup_field = 'id'


class SmartphoneListAPIView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphones.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        'price'
    ]


class SmartphoneDetailAPIView(RetrieveAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphones.objects.all()
    lookup_field = 'id'


class BrickListAPIView(ListAPIView):

    serializer_class = BrickSerializer
    queryset = Bricks.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        'price'
    ]


class BrickDetailAPIView(RetrieveAPIView):

    serializer_class = BrickSerializer
    queryset = Bricks.objects.all()
    lookup_field = 'id'


class BuildingBlockListAPIView(ListAPIView):

    serializer_class = BuildingBlockSerializer
    queryset = BuildingBlocks.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        'price'
    ]


class BuildingBlockDetailAPIView(RetrieveAPIView):

    serializer_class = BuildingBlockSerializer
    queryset = BuildingBlocks.objects.all()
    lookup_field = 'id'


class CustomerAPIView(ListAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()