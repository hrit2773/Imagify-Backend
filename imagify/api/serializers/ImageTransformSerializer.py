from rest_framework import serializers
from imagify.models.ImageModel import TransformationHistory

aspect_types={(
    ('square','Square'),
    ('portrait','Portrait'),
    ('landscape','Landscape'),
    ('custom','Custom')
)}
class GenerativeBackgroundSerializer(serializers.Serializer):
    title=serializers.CharField()
    prompt=serializers.CharField()
    
class GenerativeFillSerializer(serializers.Serializer):
    title=serializers.CharField()
    aspect_ratio=serializers.CharField(choices=aspect_types,allow_blank=True)
    width=serializers.IntegerField(allow_blank=True)
    height=serializers.IntegerField(allow_blank=True)
    
class GenerativeReplaceSerializer(serializers.Serializer):
    transform_from=serializers.CharField()
    transform_to=serializers.CharField()
    replace_all=serializers.BooleanField()
    
class TransformationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformationHistory
        fields = "__all__"