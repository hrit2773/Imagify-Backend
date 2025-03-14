from rest_framework import routers
from imagify.api.viewsets.ImageUploadViewset import ImageUploadViewset
from imagify.api.viewsets.ImageTransformViewset import ImageTransformViewset,TransformationHistoryViewset

router=routers.SimpleRouter()
router.register(r'images',ImageUploadViewset)
router.register(r'transform_image',ImageTransformViewset)
router.register(r'transformation_history',TransformationHistoryViewset)
url_patterns=router.urls