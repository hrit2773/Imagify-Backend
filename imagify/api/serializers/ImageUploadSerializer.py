from rest_framework import serializers
from imagify.api.serializers.ImageTransformSerializer import TransformationHistorySerializer
from imagify.models.ImageModel import ImageModel
from users.serializers import UserSerializer
class ImageUploadSerializer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    transformations=TransformationHistorySerializer(many=True,read_only=True)
    class Meta:
        model = ImageModel
        fields = "__all__"
     