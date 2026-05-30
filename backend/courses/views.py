import json
from datetime import timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Course, CourseView, Enrollment, Review

#Helper
def success_response(data=None, status=200):
    return JsonResponse(data or {}, status=status, json_dumps_params={"ensure_ascii": False})

def error_response(message, status=400):
    return success_response({"error": message}, status=status)

def method_not_allowed():
    return error_response("Method không hợp lệ", status=405)

def get_json_body(request):
    return json.loads(request.body or "{}")
#============
#Serializer
def serialize_course(course):
    return {
        "id": course.id,
        "name": course.name,
        "university": course.university,
        "difficulty_level": course.difficulty_level,
        "url": course.url,
        "about": course.about,
    }

def serialize_course_detail(course, views_count, reviews):
    return {
        "id": course.id,
        "name": course.name,
        "university": course.university,
        "difficulty_level": course.difficulty_level,
        "url": course.url,
        "description": course.description,
        "user_views_count": views_count,
        "reviews": [serialize_review(review) for review in reviews],
    }

def serialize_enrollment(enrollment):
    return {
        "id": enrollment.course.id,
        "name": enrollment.course.name,
        "university": enrollment.course.university,
        "date_enrolled": enrollment.date_enrolled.strftime("%d/%m/%Y"),
        "status": enrollment.get_status_display(),
    }

def serialize_review(review):
    return {
        "username": review.user.username,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.strftime("%d/%m/%Y"),
    }

def serialize_view_ranking(item):
    return {
        "id": item["course__id"],
        "name": item["course__name"],
        "university": item["course__university"],
        "unique_users": item["unique_users"],
    }

def serialize_rating_ranking(item):
    return {
        "id": item["course__id"],
        "name": item["course__name"],
        "university": item["course__university"],
        "avg_rating": round(item["avg_rating"], 1),
        "review_count": item["review_count"],
    }
#==================
#Sub-logic
def update_course_view_count(user_id, course):
    if not user_id:
        return 0

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return 0

    course_view, created = CourseView.objects.get_or_create(user=user, course=course)
    if not created:
        course_view.view_count += 1
        course_view.save()

    return course_view.view_count

def get_course_views_by_period(period):
    queryset = CourseView.objects.all()
    now = timezone.now()

    period_filters = {
        "day": now - timedelta(days=1),
        "week": now - timedelta(weeks=1),
        "month": now - timedelta(days=30),
    }

    start_date = period_filters.get(period)
    if start_date:
        queryset = queryset.filter(last_viewed__gte=start_date)

    return queryset
#==================
#GET
#[GET]  /api/courses/
def api_course_list(request):
    courses = Course.objects.all().order_by("id")

    search_query = request.GET.get("search", "").strip()
    level_query = request.GET.get("level", "")
    univ_query = request.GET.get("university", "")

    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    if level_query:
        courses = courses.filter(difficulty_level__iexact=level_query)
    if univ_query:
        courses = courses.filter(university__icontains=univ_query)

    paginator = Paginator(courses, 20)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return success_response({
        "courses": [serialize_course(course) for course in page_obj],
        "has_next": page_obj.has_next(),
    })

#[GET]  /api/courses/<course_id>/
@csrf_exempt
def api_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    views_count = update_course_view_count(request.GET.get("user_id"), course)
    reviews = Review.objects.filter(course=course)

    return success_response(serialize_course_detail(course, views_count, reviews))
#[GET]  /api/my-courses/<user_id>/
def api_my_courses(request, user_id):
    user = get_object_or_404(User, id=user_id)
    enrollments = Enrollment.objects.filter(user=user)

    return success_response({
        "my_courses": [serialize_enrollment(enrollment) for enrollment in enrollments]
    })
#[GET]  /api/courses/ranking/
def api_course_ranking(request):
    period = request.GET.get("period", "all")
    queryset = get_course_views_by_period(period)

    rankings = (
        queryset.values("course__id", "course__name", "course__university")
        .annotate(unique_users=Count("user"))
        .order_by("-unique_users")[:10]
    )

    return success_response({
        "ranking": [serialize_view_ranking(item) for item in rankings]
    })
#[GET]  /api/courses/rating-ranking/
def api_rating_ranking(request):
    rating_rankings = (
        Review.objects.values("course__id", "course__name", "course__university")
        .annotate(
            avg_rating=Avg("rating"),
            review_count=Count("id"),
        )
        .filter(review_count__gt=0)
        .order_by("-avg_rating", "-review_count")[:10]
    )

    return success_response({
        "ranking": [serialize_rating_ranking(item) for item in rating_rankings]
    })
#====================
#POST
#[POST] /api/signup/
@csrf_exempt
def api_signup(request):
    if request.method != "POST":
        return method_not_allowed()

    try:
        data = get_json_body(request)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email", "")

        if User.objects.filter(username=username).exists():
            return error_response("Tên đăng nhập đã tồn tại!")

        user = User.objects.create_user(username=username, password=password, email=email)
        return success_response({
            "message": "Đăng ký tài khoản thành công!",
            "user_id": user.id,
        })
    except Exception as e:
        return error_response(str(e))
#[POST] /api/login/
@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return method_not_allowed()

    try:
        data = get_json_body(request)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return error_response("Sai tài khoản hoặc mật khẩu!")

        return success_response({
            "message": "Đăng nhập thành công!",
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_staff or user.is_superuser,
        })
    except Exception as e:
        return error_response(str(e))
#[POST] /api/enroll/
@csrf_exempt
def api_enroll_course(request):
    if request.method != "POST":
        return method_not_allowed()

    try:
        data = get_json_body(request)
        user = User.objects.get(id=data.get("user_id"))
        course = Course.objects.get(id=data.get("course_id"))

        _, created = Enrollment.objects.get_or_create(user=user, course=course)
        if not created:
            return success_response({"message": "Bạn đã đăng ký khóa học này trước đó rồi!"})

        return success_response({"message": "Đăng ký khóa học thành công!"})
    except Exception as e:
        return error_response(str(e))
#[POST] /api/unenroll/
@csrf_exempt
def api_unenroll_course(request):
    if request.method != "POST":
        return method_not_allowed()

    try:
        data = get_json_body(request)
        enrollment = Enrollment.objects.filter(
            user_id=data.get("user_id"),
            course_id=data.get("course_id"),
        )

        if not enrollment.exists():
            return error_response("Bạn chưa đăng ký khóa học này nên không thể hủy.")

        enrollment.delete()
        return success_response({"message": "Đã hủy đăng ký khóa học thành công!"})
    except Exception as e:
        return error_response(str(e))
#[POST] /api/review/add/
@csrf_exempt
def api_add_review(request):
    if request.method != "POST":
        return method_not_allowed()

    try:
        data = get_json_body(request)
        user = User.objects.get(id=data.get("user_id"))
        course = Course.objects.get(id=data.get("course_id"))
        rating = int(data.get("rating", 5))
        comment = data.get("comment", "")

        review = Review.objects.create(
            user=user,
            course=course,
            rating=rating,
            comment=comment,
        )
        return success_response({
            "message": "Gửi đánh giá thành công!",
            "review_id": review.id,
        })
    except Exception as e:
        return error_response(str(e))