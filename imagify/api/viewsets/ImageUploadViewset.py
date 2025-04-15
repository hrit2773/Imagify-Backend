from rest_framework import viewsets
from imagify.models.ImageModel import ImageModel
from imagify.api.serializers.ImageUploadSerializer import ImageUploadSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser,FormParser

class ImageUploadViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = ImageModel.objects.all()
    serializer_class=ImageUploadSerializer
    parser_classes=[MultiPartParser,FormParser]
    