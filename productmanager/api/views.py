import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Product
from .constants import API_VERSION
from .forms import ProductForm


def index(_):
    return JsonResponse(
        {
            "message": "Welcome to the Product Manager API",
            "version": API_VERSION,
            "endpoints": {
                "/products": {
                    "GET": "Get list of all existing products",
                    "POST": "Create a new product",
                },
            },
        }
    )


@method_decorator(csrf_exempt, name="dispatch")
class ProductsView(View):
    def get(self, _):
        data = [
            {**model_to_dict(product), "price": float(product.price)}
            for product in Product.objects.all()
        ]

        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        form = ProductForm(data)

        if form.is_valid():
            product = form.save(commit=False)
            product.price = Decimal(str(data["price"]))
            product.save()
            return JsonResponse(
                {**model_to_dict(product), "price": float(product.price)},
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)
