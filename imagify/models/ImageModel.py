from django.utils import timezone
from django.db import models
from users.models import User
import re
import urllib.parse

transformation_types=(
    ('gen_background_replace','generative_background'),
    ('gen_fill','generative_fill'),
    ('enhance','enhancement'),
    ('gen_replace','generative_replace'),
    ('gen_recolor','generative_recolor'),
    ('gen_restore','generative_restore'),
    ('no_trans','no_transformation'),
)

class ImageModel(models.Model):
    title=models.TextField()
    image=models.ImageField( upload_to='images/',blank=True,max_length=10000)
    author=models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True)
    cloudinary_id=models.CharField(blank=True)
    transformation_url=models.URLField(blank=True)
    is_minted_NFT=models.BooleanField(default=False)
    create_at=models.DateTimeField(default=timezone.now)
    update_at=models.DateTimeField(default=timezone.now)
    
    def save(self,*args,**kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        if self.image:
            decoded_url = urllib.parse.unquote(self.image.url)
            match = re.search(r"v1/(.+)", decoded_url)

            if match:
                self.cloudinary_id = match.group(1)
                ImageModel.objects.filter(pk=self.pk).update(cloudinary_id=self.cloudinary_id)

class TransformationHistory(models.Model):
    original_image=models.ForeignKey(ImageModel,related_name="transformations",on_delete=models.PROTECT)
    title=models.TextField()
    transformation_type=models.CharField(choices=transformation_types)
    image_url=models.URLField()
    transformed_by=models.ForeignKey(User, on_delete=models.PROTECT)
    transformed_at=models.DateTimeField(default=timezone.now)
    
        
    