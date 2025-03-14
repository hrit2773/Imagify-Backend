from rest_framework import serializers
from imagify.models.ImageModel import ImageModel

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"
     