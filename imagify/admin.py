from django.contrib import admin
from .models.ImageModel import ImageModel,TransformationHistory

@admin.register(ImageModel)
class AdminImage(admin.ModelAdmin):
    fields=["title","image","author"]

@admin.register(TransformationHistory)
class AdminImage(admin.ModelAdmin):
    fields=["__all__"]