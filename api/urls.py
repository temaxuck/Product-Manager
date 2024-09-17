from django.urls import path
from .views import index, ProductsView

app_name = "api"
urlpatterns = [
    path("", index, name="index"),
    path("products", ProductsView.as_view(), name="products"),
]
