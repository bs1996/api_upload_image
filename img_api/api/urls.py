from django.urls import path, include
from rest_framework import routers
from . import views
from .views import ImagesViewSet, Customer, sign_in, Image, ImageAPIView, GenerateLinkView, ValidateLinkView



router = routers.DefaultRouter()
router.register(r'images', ImagesViewSet, basename='Images')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload/', ImageAPIView.as_view()),
    path('image/<int:number>/<int:time>/', GenerateLinkView.as_view()),
    path('image/<int:id>/<int:number>/bin/', ValidateLinkView.as_view()),
    path('image/<int:id>/<int:number>/<str:type>/', Image),
    path('login/', sign_in),

]

