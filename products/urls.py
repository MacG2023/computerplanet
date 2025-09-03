from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, product_list
)

urlpatterns = [
    path("", product_list, name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
