from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# 1. Bảng Course
class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên khóa học")
    university = models.CharField(max_length=255, verbose_name="Trường đại học")
    difficulty_level = models.CharField(max_length=50, verbose_name="Cấp độ khó")
    url = models.URLField(max_length=500, verbose_name="Đường dẫn khóa học")
    about = models.TextField(blank=True, null=True, verbose_name="Mô tả ngắn")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả chi tiết")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Khóa học"
        verbose_name_plural = "Danh sách Khóa học"


# 2. Bảng Enrollment
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'Đang học'),
        ('Completed', 'Đã hoàn thành'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Học viên")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Khóa học")
    date_enrolled = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng ký")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress', verbose_name="Trạng thái")

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

    class Meta:
        verbose_name = "Lượt đăng ký"
        verbose_name_plural = "Danh sách Đăng ký học"
        # Đảm bảo một user không thể đăng ký trùng 1 khóa học nhiều lần
        unique_together = ('user', 'course')


# 3. Bảng Review
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Học viên")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name="Khóa học")
    rating = models.IntegerField(verbose_name="Số sao đánh giá") # Từ 1 đến 5
    comment = models.TextField(blank=True, null=True, verbose_name="Bình luận")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đánh giá")

    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.rating} sao)"

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Danh sách Đánh giá"


# 4. Bảng CourseView
class CourseView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_views', verbose_name="Học viên")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_views', verbose_name="Khóa học")
    view_count = models.PositiveIntegerField(default=1, verbose_name="Số lượt xem")
    last_viewed = models.DateTimeField(auto_now=True, verbose_name="Lần cuối xem")

    def __str__(self):
        return f"{self.user.username} xem {self.course.name} ({self.view_count} lần)"

    class Meta:
        verbose_name = "Lượt xem khóa học"
        verbose_name_plural = "Theo dõi Lượt xem"
        unique_together = ('user', 'course')