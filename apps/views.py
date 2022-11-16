from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Category, ProductImage, Product
from apps.serializer import CategoryModelSerializer, ProductImagesModelSerializer, ProductModelSerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.order_by('-created_at')
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'


class ProductImageApiView(GenericAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImagesModelSerializer
    parser_classes = (MultiPartParser, )

    def get(self, request):
        images = ProductImage.objects.all()
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
