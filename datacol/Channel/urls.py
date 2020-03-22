from django.urls import path, include
from django.db.models import Q
from .views import (

    ChannelUpdateView,
    TopicCreateView,
)
from . import views
from . import lazy_loading
from .models import ProductService
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view

class ProductServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductService
        fields = ['id', 'product_name', 'admins', 'url', 'guide_info', 'product_info','product_profife_picture', 'date_created', 'topic', 'business']

    # Validations of data passed in

    def validate_product_name(self, value):
        qs = ProductService.objects.filter(product_name__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('The product name has been used')
        return value
    

class ProductServiceViewSet(viewsets.ModelViewSet):
    queryset = ProductService.objects.all()
    serializer_class = ProductServiceSerializer
    
    # Searching

    def get_queryset(self):
        qs = ProductService.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(product_name__icontains=query)|Q(product_info__icontains=query)).distinct()
        return qs


router = routers.DefaultRouter()
router.register('products', ProductServiceViewSet)


urlpatterns = [
    path('create_channel/', views.create_channel, name='create-channel'),
    path('channel/<channel_code>/', views.channel_home, name='channel-detail'),
    path('channel/<pk>/update/', ChannelUpdateView.as_view(), name='channel-update'),
    path('', include(router.urls)),
    path('product/<pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('channel/<str:channel_code>/add_question', views.QuestionCreateView.as_view(), name='add-question'),
    path('channel/<str:channel_code>/new_question', views.QuestionCreateView.as_view(), name='new-question'),
    path('channel/<str:channel_code>/question/<int:pk>/answer/add/', views.AnswerCreateView.as_view(), name='new-answer'),

    path('channel/<channel_code>/subscription/', views.channel_subscribe, name='channel-subscription'),
    path('channel/<channel_code>/create_topic/', views.create_channel_topic, name='create-channel-topic'),
    path('channel/<channel_code>/lazy/', lazy_loading.lazy_loading_topics, name='lazy_load_topics'),

]
