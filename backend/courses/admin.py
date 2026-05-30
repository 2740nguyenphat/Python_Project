from django.contrib import admin
from .models import Course, Enrollment, Review, CourseView

# 1. Cấu hình giao diện Admin cho Khóa học
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'university', 'difficulty_level', 'url')
    list_filter = ('difficulty_level', 'university')
    search_fields = ('name', 'university', 'about')
    list_per_page = 20

# 2. Cấu hình giao diện Admin cho việc Đăng ký học
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'date_enrolled', 'status')
    list_filter = ('status', 'date_enrolled')
    search_fields = ('user__username', 'course__name')
    date_hierarchy = 'date_enrolled'


# 3. Cấu hình giao diện Admin cho phần Đánh giá & Bình luận
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'course__name', 'comment')


# 4. Cấu hình giao diện Admin cho phần Theo dõi lượt xem khóa học
@admin.register(CourseView)
class CourseViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'view_count', 'last_viewed')
    list_filter = ('last_viewed',)
    search_fields = ('user__username', 'course__name')
    ordering = ('-view_count',)