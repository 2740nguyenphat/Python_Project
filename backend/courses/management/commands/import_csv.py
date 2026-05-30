import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from courses.models import Course


class Command(BaseCommand):
    help = 'Import danh sách khóa học từ file EdX.csv nằm trong thư mục data'

    def handle(self, *args, **kwargs):
        # Đường dẫn động tìm đến thư mục data/EdX.csv (nằm cùng cấp với thư mục backend)
        base_dir = settings.BASE_DIR  # Thường chỉ vào thư mục backend/
        csv_file_path = os.path.join(base_dir, '..', 'data', 'EdX.csv')

        # Kiểm tra xem file có tồn tại thực sự không
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"Không tìm thấy file dữ liệu tại đường dẫn: {csv_file_path}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Đang đọc dữ liệu từ: {csv_file_path}..."))

        count_created = 0
        count_skipped = 0

        # Mở file CSV và đọc dữ liệu bằng UTF-8
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    # Trích xuất dữ liệu từ các cột của file EdX.csv
                    # DictReader giúp lấy giá trị thông qua tên cột ở dòng đầu tiên
                    name = row.get('Course Name', row.get('Name', '')).strip()
                    university = row.get('University', '').strip()
                    difficulty_level = row.get('Difficulty Level', '').strip()
                    url = row.get('Course URL', row.get('Link', '')).strip()
                    about = row.get('About', '').strip()
                    description = row.get('Course Description', '').strip()

                    # Bỏ qua nếu dòng đó trống tên khóa học
                    if not name:
                        count_skipped += 1
                        continue

                    # Sử dụng get_or_create để tránh việc import trùng lặp nếu chạy lại script nhiều lần
                    course, created = Course.objects.get_or_create(
                        name=name,
                        university=university,
                        defaults={
                            'difficulty_level': difficulty_level,
                            'url': url,
                            'about': about,
                            'description': description
                        }
                    )

                    if created:
                        count_created += 1
                    else:
                        count_skipped += 1

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Lỗi khi import dòng {row.get('Name')}: {e}"))
                    count_skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Quá trình import hoàn tất!\n"
            f"- Đã thêm mới thành công: {count_created} khóa học.\n"
            f"- Đã bỏ qua/Trùng lặp: {count_skipped} dòng."
        ))