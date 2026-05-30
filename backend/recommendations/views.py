from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from courses.models import Course
from .engine import calculate_course_recommendations

#[GET] /api/courses/<course_id>/recommendations/
class CourseRecommendationAPIView(View):
    def get(self, request, course_id):
        try:
            recommended_ids = calculate_course_recommendations(int(course_id), top_n=5)

            if not recommended_ids:
                return JsonResponse({"recommendations": []}, status=200)

            courses_queryset = Course.objects.filter(id__in=recommended_ids)

            sorted_courses = sorted(courses_queryset, key=lambda x: recommended_ids.index(x.id))

            data = []
            for course in sorted_courses:
                data.append({
                    "id": course.id,
                    "name": course.name,
                    "university": course.university,
                    "difficulty_level": course.difficulty_level,
                })

            return JsonResponse({"recommendations": data}, status=200, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)