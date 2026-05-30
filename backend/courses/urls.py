from django.urls import path
from . import views

urlpatterns = [
    #Đăng nhập/Đăng ký
    path('api/signup/', views.api_signup, name='api_signup'),
    path('api/login/', views.api_login, name='api_login'),
    #Quản lý khoá học
    path('api/courses/', views.api_course_list, name='api_course_list'),
    path('api/courses/<int:course_id>/', views.api_course_detail, name='api_course_detail'),
    #Đăng ký khoá học
    path('api/enroll/', views.api_enroll_course, name='api_enroll_course'),
    path('api/my-courses/<int:user_id>/', views.api_my_courses, name='api_my_courses'),
    path('api/unenroll/', views.api_unenroll_course, name='api_unenroll_course'),
    #Review
    path('api/review/add/', views.api_add_review, name='api_add_review'),
    #Ranking views
    path('api/courses/ranking/', views.api_course_ranking, name='api_course_ranking'),
    #Ranking reviews
    path('api/courses/rating-ranking/', views.api_rating_ranking, name='api_rating_ranking'),
]