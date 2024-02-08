from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Review
from main.serializers import ReviewSerializer, ProductListSerializer, ProductDetailsSerializer


@api_view(['GET'])
def products_list_view(request):
    """реализуйте получение всех товаров из БД
    реализуйте сериализацию полученных данных
    отдайте отсериализованные данные в Response"""
    products_list = Product.objects.all()
    ser = ProductListSerializer(products_list, many=True)
    return Response(ser.data)


class ProductDetailsView(APIView):
    def get(self, request, product_id):
        """реализуйте получение товара по id, если его нет, то выдайте 404
        реализуйте сериализацию полученных данных
        отдайте отсериализованные данные в Response"""
        try:
            review = Review.objects.filter(product=product_id)
            product = Product.objects.get(id=product_id)
            ser = ProductDetailsSerializer(product)
            return Response(ser.data)
        except Product.DoesNotExist:
            raise Http404


# доп задание:
class ProductFilteredReviews(APIView):
    def get(self, request, product_id):
        """обработайте значение параметра mark и
        реализуйте получение отзывов по конкретному товару с определённой оценкой
        реализуйте сериализацию полученных данных
        отдайте отсериализованные данные в Response"""
        mark = request.query_params.get('mark')
        mark_value = mark if mark is not None else ''
        review = Review.objects.filter(product=product_id, mark__endswith=mark_value)
        ser = ReviewSerializer(review, many=True)
        return Response(ser.data)
