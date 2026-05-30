import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def show_course_detail_page():
    if st.button("⬅️ Quay lại danh sách khóa học", key="back_to_list"):
        st.session_state.selected_course_id = None
        st.rerun()

    params = {"user_id": st.session_state.user_id}

    try:
        res = requests.get(f"{BACKEND_URL}/api/courses/{st.session_state.selected_course_id}/", params=params)
        if res.status_code == 200:
            course = res.json()

            #Nút đăng ký
            head_col1, head_col2 = st.columns([3, 1])
            with head_col1:
                st.header(f"📘 {course['name']}")
                st.caption(
                    f"🏫 Trường cung cấp: **{course['university']}** | 🎚️ Cấp độ: **{course['difficulty_level']}**")

            with head_col2:
                st.write("")
                is_enrolled = False
                try:
                    check_res = requests.get(f"{BACKEND_URL}/api/my-courses/{st.session_state.user_id}/")
                    if check_res.status_code == 200:
                        enrolled_ids = [c['id'] for c in check_res.json().get("my_courses", [])]
                        if course['id'] in enrolled_ids:
                            is_enrolled = True
                except:
                    pass

                if is_enrolled:
                    if st.button("❌ Hủy đăng ký học", use_container_width=True, type="secondary",
                                 key="detail_unenroll_btn"):
                        unenroll_payload = {"user_id": st.session_state.user_id, "course_id": course['id']}
                        un_res = requests.post(f"{BACKEND_URL}/api/unenroll/", json=unenroll_payload)
                        if un_res.status_code == 200:
                            st.toast("Đã hủy đăng ký thành công!", icon="✅")
                            st.rerun()
                else:
                    if st.button("📥 Đăng ký học ngay", use_container_width=True, type="primary",
                                 key="detail_enroll_btn"):
                        enroll_payload = {"user_id": st.session_state.user_id, "course_id": course['id']}
                        enroll_res = requests.post(f"{BACKEND_URL}/api/enroll/", json=enroll_payload)
                        if enroll_res.status_code == 200:
                            st.toast("Đăng ký thành công!", icon="✅")
                            st.rerun()

            st.info(f"📊 Bạn đã nhấn xem khóa học này tổng cộng: **{course['user_views_count']}** lần.")

            #Hiển thị thông tin chi tiết
            st.subheader("Mô tả nội dung môn học")
            st.write(course["description"] if course["description"] else "Chưa có mô tả chi tiết cho khóa học này.")
            st.markdown(f"[🔗 Đi tới liên kết gốc khóa học trên edX]({course['url']})")

            st.divider()

            #Gửi đánh giá
            if is_enrolled:
                st.subheader("✍️ Viết đánh giá của bạn")
                with st.form(key="review_form", clear_on_submit=True):
                    rating = st.selectbox("Chọn mức độ hài lòng (Số sao)", [5, 4, 3, 2, 1],
                                          format_func=lambda x: f"{x} ⭐")
                    comment = st.text_area("Nhập nội dung bình luận nhận xét...",
                                           placeholder="Khóa học này rất bổ ích, giảng viên nhiệt tình...")

                    col1, col2 = st.columns([8, 1])
                    with col2:
                        submit_button = st.form_submit_button(label="🚀 Gửi đánh giá", use_container_width=False)

                    if submit_button:
                        if comment.strip() == "":
                            st.warning("Vui lòng nhập nội dung nhận xét trước khi gửi!")
                        else:
                            review_payload = {
                                "user_id": st.session_state.user_id,
                                "course_id": course['id'],
                                "rating": rating,
                                "comment": comment
                            }
                            review_res = requests.post(f"{BACKEND_URL}/api/review/add/", json=review_payload)
                            if review_res.status_code == 200:
                                st.success("🎉 Cảm ơn bạn đã gửi đánh giá phản hồi!")
                                st.rerun()
                            else:
                                st.error("Lỗi hệ thống, không thể gửi bình luận.")
            else:
                st.caption("🔒 *Hãy bấm đăng ký khóa học này để có thể viết bình luận và đánh giá số sao.*")

            st.divider()

            st.subheader("💬 Đánh giá từ các học viên khác")
            if course["reviews"]:
                for r in course["reviews"]:
                    st.markdown(f"**{r['username']}** ({r['rating']}⭐) - *Ngày {r['created_at']}*")
                    st.write(r["comment"])
                    st.caption("---")
            else:
                st.text("Chưa có lượt đánh giá nào cho khóa học này. Hãy là người đầu tiên trải nghiệm!")

            #Chức năng hiển thị khoá học tương tự
            st.write("")
            st.divider()
            st.markdown("### 💡 Khóa học tương tự có thể bạn quan tâm")
            st.caption("Danh sách được tự động phân tích và tính toán độ tương đồng từ Recommendations Engine.")

            try:
                rec_res = requests.get(f"{BACKEND_URL}/api/courses/{st.session_state.selected_course_id}/recommendations/")
                if rec_res.status_code == 200:
                    rec_list = rec_res.json().get("recommendations", [])

                    if not rec_list:
                        st.caption("ℹ️ Chưa có khóa học gợi ý phù hợp cho môn học này.")
                    else:
                        cols = st.columns(len(rec_list))
                        for idx, rec_item in enumerate(rec_list):
                            with cols[idx]:
                                st.html(f"""
                                    <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; background-color: #ffffff; min-height: 120px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                                        <div style="font-size: 11px; color: #64748b; font-weight: 500; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;">🏛️ {rec_item['university']}</div>
                                        <div style="font-size: 13px; font-weight: 600; margin: 4px 0; color: #1e293b; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.3;">{rec_item['name']}</div>
                                        <span style="font-size: 10px; background-color: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #475569; font-weight: 500;">⚡ {rec_item['difficulty_level']}</span>
                                    </div>
                                """)
                                if st.button("Xem ngay", key=f"rec_click_btn_{rec_item['id']}_{idx}", use_container_width=True):
                                    st.session_state.selected_course_id = rec_item['id']
                                    st.rerun()
                else:
                    st.error("Không thể tải danh sách khóa học gợi ý.")
            except Exception:
                st.error("Lỗi kết nối với dịch vụ gợi ý khóa học.")

        else:
            st.error("Không tìm thấy thông tin chi tiết khóa học.")
    except Exception:
        st.error("Lỗi khi tải thông tin khóa học từ Backend.")