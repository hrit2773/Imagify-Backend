from rest_framework import viewsets,status
from imagify.models.ImageModel import ImageModel,TransformationHistory
from imagify.api.serializers.ImageTransformSerializer import GenerativeBackgroundSerializer,GenerativeFillSerializer, GenerativeReplaceSerializer,TransformationHistorySerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import mixins
from rest_framework.decorators import action
from cloudinary import CloudinaryImage
from rest_framework.response import Response
from django.db import transaction
from rest_framework.serializers import ValidationError

class ImageTransformViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return ImageModel.objects.filter(author=self.request.user)
    
    def get_serializer_class(self):
        if self.action == "generative_background":
            return GenerativeBackgroundSerializer
        elif self.action == "generative_fill":
            return GenerativeFillSerializer
        elif self.action == "generative_replace":
            return GenerativeReplaceSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['POST'])
    def generative_background(self,request,pk=None):
        serializer=self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        image_data=self.get_object()
        public_id=image_data.cloudinary_id
        prompt= request.data.get('prompt')
        title= request.data.get('title')
        
        with transaction.atomic():
            transformed_url=CloudinaryImage(public_id).build_url(
                transformation=[
                    {
                        "effect":f"gen_background_replace:prompt_{prompt}"
                    } 
                ]
            )
            ImageModel.objects.filter(pk=pk).update(
                transformation_url=transformed_url,
                title=title
            )
            TransformationHistory.objects.create(
                title= title,
                transformation_type='gen_background_replace',
                image_url=transformed_url,
                transformed_by=request.user
            )
            return Response(status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['POST'])
    def generative_fill(self,request,pk=None):
        serializer=self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        image_data=self.get_object()
        public_id=image_data.cloudinary_id
        title=request.data.get('title')
        aspect_ratio=request.data.get('aspect_ratio')
        width=request.data.get('width')
        height=request.data.get('height')
        
        with transaction.atomic():
            if aspect_ratio == 'square':
                transformed_url=CloudinaryImage(public_id).build_url(transformation=[
                    {
                        "aspect_ratio":"1:1", 
                        "gravity":"center", 
                        "background":"gen_fill", 
                        "crop":"pad"       
                    }
                ])
            elif aspect_ratio == 'portrait':
                transformed_url=CloudinaryImage(public_id).build_url(transformation=[
                    {
                        "aspect_ratio":"9:16", 
                        "gravity":"center", 
                        "background":"gen_fill", 
                        "crop":"pad"       
                    }
                ])
            elif aspect_ratio == 'landscape':
                transformed_url=CloudinaryImage(public_id).build_url(transformation=[
                    {
                        "aspect_ratio":"16:9", 
                        "gravity":"center", 
                        "background":"gen_fill", 
                        "crop":"pad"       
                    }
                ])
            else:
                if not width or not height:
                    ValidationError("Width and Height are not specified")
                transformed_url=CloudinaryImage(public_id).build_url(transformation=[
                    {
                        "width":width, 
                        "gravity":height, 
                        "background":"gen_fill", 
                        "crop":"pad"       
                    }
                ])
            ImageModel.objects.filter(pk=pk).update(
                transformation_url=transformed_url,
                title=title
            )
            TransformationHistory.objects.create(
                title= title,
                transformation_type='gen_fill',
                image_url=transformed_url,
                transformed_by=request.user
            )
            return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def enhance(self,request,pk=None):
        image_data=self.get_object()
        public_id=image_data.cloudinary_id
        title=request.data.get('title')
        transformed_url=transformed_url=CloudinaryImage(public_id).build_url(transformation=[
            {
                "effect":"enhance"       
            }
        ])
        ImageModel.objects.filter(pk=pk).update(
            transformation_url=transformed_url,
            title=title
        )
        TransformationHistory.objects.create(
            title= title,
            transformation_type='gen_background_replace',
            image_url=transformed_url,
            transformed_by=request.user
        )
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def generative_fill(self,request,pk=None):
        serializer=self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        image_data=self.get_object()
        public_id=image_data.cloudinary_id
        title=request.data.get('title')
        transform_from=request.data.get('transform_from')
        transform_to=request.data.get('transform_to')
        replace_all=request.data.get('replace_all')
        with transaction.atomic():
            transformed_url=CloudinaryImage(public_id).build_url(
                transformation=[{
                    "effect":f"gen_replace:from_{transform_from};to_{transform_to}{";multiple_True" if replace_all else ""}"
                }]
            )
            ImageModel.objects.filter(pk=pk).update(
                transformation_url=transformed_url,
                title=title
            )
            TransformationHistory.objects.create(
                title= title,
                transformation_type='gen_background_replace',
                image_url=transformed_url,
                transformed_by=request.user
            )
            return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def generative_restore(self,request,pk=None):
        image_data=self.get_object()
        public_id=image_data.cloudinary_id
        title=request.data.get('title')
        transformed_url=transformed_url=CloudinaryImage(public_id).build_url(transformation=[
            {
                "effect":"gen_restore"     
            }
        ])
        ImageModel.objects.filter(pk=pk).update(
            transformation_url=transformed_url,
            title=title
        )
        TransformationHistory.objects.create(
            title= title,
            transformation_type='gen_background_replace',
            image_url=transformed_url,
            transformed_by=request.user
        )
        return Response(status=status.HTTP_200_OK)
    
class TransformationHistoryViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class=TransformationHistorySerializer
    def get_queryset(self):
        return TransformationHistory.objects.filter(transformed_by=self.request.user)
    permission_classes=[IsAuthenticated]