import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course, Enrollment, Review, CourseView


class Command(BaseCommand):
    help = 'Tạo nhanh 50 học viên ảo, tự động đăng ký học và đánh giá bình luận khóa học ngẫu nhiên'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("=== Bắt đầu khởi tạo dữ liệu ảo ==="))

        # Kiểm tra hệ thống phải có khóa học trước
        all_courses = list(Course.objects.all())
        if not all_courses:
            self.stdout.write(self.style.ERROR(
                "Lỗi: Không tìm thấy khóa học nào trong database! Vui lòng chạy lệnh import_csv trước."))
            return

        # Danh sách cứng tổng cộng 50 tài khoản học viên ảo
        students_data = [
            # 20 học viên ban đầu của bạn
            {"username": "nguyenvan_anh", "email": "anh.nv@gmail.com", "first_name": "Anh", "last_name": "Nguyễn Văn"},
            {"username": "tran_bao", "email": "bao.tran@gmail.com", "first_name": "Bảo", "last_name": "Trần Thị"},
            {"username": "le_cuong", "email": "cuong.le@gmail.com", "first_name": "Cường", "last_name": "Lê"},
            {"username": "pham_dung", "email": "dung.pham@gmail.com", "first_name": "Dũng", "last_name": "Phạm Tiến"},
            {"username": "hoang_yen", "email": "yen.hoang@gmail.com", "first_name": "Yến", "last_name": "Hoàng"},
            {"username": "vu_dat", "email": "dat.vu@gmail.com", "first_name": "Đạt", "last_name": "Vũ Quốc"},
            {"username": "phan_huong", "email": "huong.phan@gmail.com", "first_name": "Hương", "last_name": "Phan"},
            {"username": "dang_khanh", "email": "khanh.dang@gmail.com", "first_name": "Khánh", "last_name": "Đặng"},
            {"username": "bui_lam", "email": "lam.bui@gmail.com", "first_name": "Lâm", "last_name": "Bùi"},
            {"username": "ngo_minh", "email": "minh.ngo@gmail.com", "first_name": "Minh", "last_name": "Ngô Quang"},
            {"username": "duong_nam", "email": "nam.duong@gmail.com", "first_name": "Nam", "last_name": "Dương"},
            {"username": "ly_oanh", "email": "oanh.ly@gmail.com", "first_name": "Oanh", "last_name": "Lý Ngọc"},
            {"username": "do_phong", "email": "phong.do@gmail.com", "first_name": "Phong", "last_name": "Đỗ Thanh"},
            {"username": "ho_quan", "email": "quan.ho@gmail.com", "first_name": "Quân", "last_name": "Hồ"},
            {"username": "nguyen_son", "email": "son.nguyen@gmail.com", "first_name": "Sơn",
             "last_name": "Nguyễn Tùng"},
            {"username": "dinh_thao", "email": "thao.dinh@gmail.com", "first_name": "Thảo", "last_name": "Đinh"},
            {"username": "quach_tuan", "email": "tuan.quach@gmail.com", "first_name": "Tuấn", "last_name": "Quách"},
            {"username": "phung_vinh", "email": "vinh.phung@gmail.com", "first_name": "Vinh", "last_name": "Phùng"},
            {"username": "ta_uyen", "email": "uyen.ta@gmail.com", "first_name": "Uyên", "last_name": "Tạ"},
            {"username": "ha_long", "email": "long.ha@gmail.com", "first_name": "Long", "last_name": "Hà"},
            # 30 học viên mới được bổ sung
            {"username": "mai_duc", "email": "duc.mai@gmail.com", "first_name": "Đức", "last_name": "Mai Văn"},
            {"username": "trinh_giang", "email": "giang.trinh@gmail.com", "first_name": "Giang",
             "last_name": "Trịnh Trường"},
            {"username": "doan_ha", "email": "ha.doan@gmail.com", "first_name": "Hà", "last_name": "Doãn Thu"},
            {"username": "ha_hai", "email": "hai.ha@gmail.com", "first_name": "Hải", "last_name": "Hà Minh"},
            {"username": "duong_hiep", "email": "hiep.duong@gmail.com", "first_name": "Hiệp", "last_name": "Dương Văn"},
            {"username": "lam_hoang", "email": "hoang.lam@gmail.com", "first_name": "Hoàng", "last_name": "Lâm"},
            {"username": "ton_hung", "email": "hung.ton@gmail.com", "first_name": "Hùng", "last_name": "Tôn Thất"},
            {"username": "nguyen_huy", "email": "huy.nguyen@gmail.com", "first_name": "Huy",
             "last_name": "Nguyễn Quang"},
            {"username": "dang_khoa", "email": "khoa.dang@gmail.com", "first_name": "Khoa", "last_name": "Đặng Đăng"},
            {"username": "vu_linh", "email": "linh.vu@gmail.com", "first_name": "Linh", "last_name": "Vũ Diệu"},
            {"username": "cao_loi", "email": "loi.cao@gmail.com", "first_name": "Lợi", "last_name": "Cao Thành"},
            {"username": "bui_nga", "email": "nga.bui@gmail.com", "first_name": "Nga", "last_name": "Bùi Thanh"},
            {"username": "le_ngan", "email": "ngan.le@gmail.com", "first_name": "Ngân", "last_name": "Lê Thị"},
            {"username": "pham_ngoc", "email": "ngoc.pham@gmail.com", "first_name": "Ngọc", "last_name": "Phạm Bảo"},
            {"username": "hoang_nhan", "email": "nhan.hoang@gmail.com", "first_name": "Nhân", "last_name": "Hoàng"},
            {"username": "phan_phat", "email": "phat.phan@gmail.com", "first_name": "Phát", "last_name": "Phan Tấn"},
            {"username": "ly_phuong", "email": "phuong.ly@gmail.com", "first_name": "Phương", "last_name": "Lý Thu"},
            {"username": "quach_tai", "email": "tai.quach@gmail.com", "first_name": "Tài", "last_name": "Quách"},
            {"username": "ngo_tam", "email": "tam.ngo@gmail.com", "first_name": "Tâm", "last_name": "Ngô"},
            {"username": "ta_tan", "email": "tan.ta@gmail.com", "first_name": "Tấn", "last_name": "Tạ Minh"},
            {"username": "vu_thang", "email": "thang.vu@gmail.com", "first_name": "Thắng", "last_name": "Vũ Đức"},
            {"username": "doan_thanh", "email": "thanh.doan@gmail.com", "first_name": "Thành", "last_name": "Doãn"},
            {"username": "bui_thao_vy", "email": "vy.bt@gmail.com", "first_name": "Vy", "last_name": "Bùi Thảo"},
            {"username": "pham_thien", "email": "thien.pham@gmail.com", "first_name": "Thiên", "last_name": "Phạm"},
            {"username": "ho_thinh", "email": "thinh.ho@gmail.com", "first_name": "Thịnh", "last_name": "Hồ Đức"},
            {"username": "nguyen_thuy", "email": "thuy.nv@gmail.com", "first_name": "Thủy", "last_name": "Nguyễn Vũ"},
            {"username": "le_toan", "email": "toan.le@gmail.com", "first_name": "Toàn", "last_name": "Lê Đăng"},
            {"username": "tran_trang", "email": "trang.tran@gmail.com", "first_name": "Trang", "last_name": "Trần Thu"},
            {"username": "vuong_tri", "email": "tri.vuong@gmail.com", "first_name": "Trí", "last_name": "Vương"},
            {"username": "nguyen_tu", "email": "tu.nguyen@gmail.com", "first_name": "Tú", "last_name": "Nguyễn Minh"}
        ]

        # Danh sách mẫu các câu bình luận phục vụ việc random đánh giá
        sample_comments = [
            "Khóa học rất hay, kiến thức áp dụng thực tế tốt.",
            "Nội dung chi tiết, dễ hiểu đối với người mới bắt đầu.",
            "Giảng viên giải thích rất kỹ càng, bài tập thực hành cuốn hút.",
            "Rất đáng đầu tư thời gian để học tập kỹ năng này.",
            "Tài liệu tham khảo phong phú và chất lượng cao.",
            "Một số đoạn âm thanh hơi nhỏ nhưng tổng thể nội dung xuất sắc.",
            "Tôi học hỏi được thêm nhiều tư duy mới từ khóa học này.",
            "Giao trình sắp xếp logic khoa học, dễ tiếp thu bài."
        ]

        user_count = 0
        enroll_count = 0
        review_count = 0

        for item in students_data:
            # Tạo tài khoản học viên (nếu chưa tồn tại)
            user, created = User.objects.get_or_create(
                username=item["username"],
                defaults={
                    "email": item["email"],
                    "first_name": item["first_name"],
                    "last_name": item["last_name"]
                }
            )
            if created:
                user.set_password("123456aA")  # Đặt mật khẩu chung cho dễ test
                user.save()
                user_count += 1

            # Lấy ngẫu nhiên từ 1 đến 5 khóa học không trùng lặp cho học viên này
            num_courses_to_enroll = random.randint(1, 5)
            enrolled_courses = random.sample(all_courses, min(num_courses_to_enroll, len(all_courses)))

            for course in enrolled_courses:
                # Tạo lượt đăng ký học ảo
                status_choice = random.choice(['In Progress', 'Completed'])
                enroll, enroll_created = Enrollment.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={'status': status_choice}
                )
                if enroll_created:
                    enroll_count += 1

                # Tạo thêm lượt xem ảo cho đồng bộ chức năng click tracking (Sử dụng get_or_create chuẩn của bạn)
                CourseView.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={'view_count': random.randint(2, 10)}
                )

            # Lấy ngẫu nhiên từ 1 đến 3 khóa học trong số các khóa đã đăng ký để viết đánh giá
            num_courses_to_review = random.randint(1, min(3, len(enrolled_courses)))
            review_courses = random.sample(enrolled_courses, num_courses_to_review)

            for course in review_courses:
                # Tạo lượt đánh giá bình luận ảo
                rev, rev_created = Review.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={
                        'rating': random.choice([4, 5]),  # Thường học viên ảo đánh giá 4 hoặc 5 sao
                        'comment': random.choice(sample_comments)
                    }
                )
                if rev_created:
                    review_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"=== Khởi tạo thành công! ===\n"
            f"- Tổng số tài khoản học viên trong danh sách: {len(students_data)} (Đã tạo mới {user_count} tài khoản).\n"
            f"- Đã đăng ký {enroll_count} lượt học ngẫu nhiên.\n"
            f"- Đã viết {review_count} lượt đánh giá bình luận."
        ))