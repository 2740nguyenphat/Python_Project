from django.urls import path
from .views import CourseRecommendationAPIView

urlpatterns = [
    path('courses/<int:course_id>/recommendations/', CourseRecommendationAPIView.as_view(), name='api_course_recommendations'),
]