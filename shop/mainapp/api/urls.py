from django.urls import path

from .api_views import (
    CategoryAPIView,
    SmartphoneListAPIView,
    SmartphoneDetailAPIView,
    CustomerAPIView,
    BrickListAPIView,
    BrickDetailAPIView,
    BuildingBlockListAPIView,
    BuildingBlockDetailAPIView
)


urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories_list'),
    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphone_list'),
    path('smartphones/<str:id>/', SmartphoneDetailAPIView.as_view(), name='smartphone_detail'),
    path('bricks/', BrickListAPIView.as_view(), name='brick_list'),
    path('bricks/<str:id>/', BrickDetailAPIView.as_view(), name='brick_detail'),
    path('buildingblocks/', BuildingBlockListAPIView.as_view(), name='buildingblock_list'),
    path('buildingblocks/<str:id>/', BuildingBlockDetailAPIView.as_view(), name='buildingblock_detail'),
    path('customers/', CustomerAPIView.as_view(), name='customers_list')
]
