import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course, CourseView


class Command(BaseCommand):
    help = 'Script riêng biệt để mô phỏng ngẫu nhiên lượt xem khóa học từ danh sách học viên hiện có'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("=== Bắt đầu mô phỏng dữ liệu lượt xem khóa học ==="))

        # 1. Lấy danh sách khóa học và tài khoản người dùng hiện tại
        all_courses = list(Course.objects.all())
        all_users = list(User.objects.filter(is_staff=False, is_superuser=False))  # Chỉ lấy tài khoản học viên ảo

        if not all_courses:
            self.stdout.write(
                self.style.ERROR("Lỗi: Không tìm thấy khóa học nào! Vui lòng chạy lệnh import_csv trước."))
            return

        if not all_users:
            self.stdout.write(self.style.ERROR(
                "Lỗi: Không tìm thấy tài khoản học viên nào! Vui lòng chạy lệnh generate_test_data trước để sinh học viên."))
            return

        view_count_records = 0

        # 2. Duyệt qua từng học viên đang có trong hệ thống để tạo lượt tương tác xem bài
        for user in all_users:
            # Mỗi học viên sẽ xem ngẫu nhiên từ 3 đến 8 khóa học khác nhau
            num_courses_to_view = random.randint(3, 8)
            courses_to_view = random.sample(all_courses, min(num_courses_to_view, len(all_courses)))

            for course in courses_to_view:
                # Sử dụng cấu trúc lưu lượt xem ảo dựa trên hàm get_or_create chuẩn của bạn
                cv, created = CourseView.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={'view_count': random.randint(2, 12)}
                    # Số lượt click tích lũy ngẫu nhiên tự nhiên từ 2-12 lần
                )

                # Nếu bản ghi đã tồn tại từ trước, ta cộng thêm lượt click ngẫu nhiên để giả lập người dùng tương tác tiếp
                if not created:
                    cv.view_count += random.randint(1, 5)
                    cv.save()

                view_count_records += 1

        self.stdout.write(self.style.SUCCESS(
            f"=== Hoàn tất mô phỏng lượt xem! ===\n"
            f"- Đã xử lý tương tác cho {len(all_users)} học viên.\n"
            f"- Đã ghi nhận mới/cập nhật thêm {view_count_records} bản ghi lượt xem khóa học thành công vào Database."
        ))