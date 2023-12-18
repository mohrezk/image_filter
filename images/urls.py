from django.urls import path
from .views import ImageListView, ImageCreateView, ImageDetailView, ApplyFilterView, ApplyFilterOnSelectedView, ClassifyImageView, ImageListClassifyView, ClassifySelectedImagesView

urlpatterns = [
    path('', ImageListView.as_view(), name="list_images"),
    path('add/', ImageCreateView.as_view(), name='image_create'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('apply_filter/<int:id>/', ApplyFilterView.as_view(), name="apply_filter"),
    path('apply_filter_on_selected/', ApplyFilterOnSelectedView.as_view(), name='apply_filter_on_selected'),
    
    path('classify/', ImageListClassifyView.as_view(), name="classify_list"),
    path('classify_image/<int:id>', ClassifyImageView.as_view(), name="classify_image"),
    path('classify_images/', ClassifySelectedImagesView.as_view(), name="classify_images")
]
