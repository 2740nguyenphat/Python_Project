import streamlit as st
from components.auth import show_auth_page
from components.course_list import show_course_list_page
from components.course_detail import show_course_detail_page
from components.ranking import show_ranking_sidebar
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hệ thống Quản lý Khóa học edX", layout="wide")

#session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "selected_course_id" not in st.session_state:
    st.session_state.selected_course_id = None

if not st.session_state.logged_in:
    st.title("🎓 Hệ Thống Quản Lý Khoá Học Online")
    show_auth_page()
else:
    top_title_col, top_user_col = st.columns([7, 2])

    with top_title_col:
        st.title("🎓 Hệ thống Quản lý Khóa học Online")

    with top_user_col:
        st.write("")
        st.write("")
        u_col1, u_col2 = st.columns([2, 2])
        with u_col1:
            st.write(f"👋 Học viên:  \n**{st.session_state.username}**")
        with u_col2:
            if st.button(
                    "🚪 Đăng xuất",
                    key="global_logout_btn",
                    use_container_width=False,
            ):
                st.session_state.logged_in = False
                st.session_state.user_id = None
                st.session_state.username = ""
                st.session_state.selected_course_id = None
                st.rerun()

    if st.session_state.selected_course_id is not None:
        show_course_detail_page()
    else:
        tab_home, tab_my_progress = st.tabs(
            ["🏠 Khám phá Khóa học", "📚 Tiến độ học tập cá nhân"]
        )

        #Khám phá khoá học
        with tab_home:
            col_courses, col_ranking = st.columns([5, 2], gap="large")

            with col_courses:
                st.header("✨ Khóa học dành cho bạn")
                show_course_list_page()

            with col_ranking:
                show_ranking_sidebar()

        #Tiến độ cá nhân
        with tab_my_progress:
            st.header("🗂️ Danh sách Khóa học của tôi")

            try:
                res = requests.get(f"{BACKEND_URL}/api/my-courses/{st.session_state.user_id}/")
                if res.status_code == 200:
                    my_courses = res.json().get("my_courses", [])

                    if not my_courses:
                        st.info(
                            "💡 Bạn chưa đăng ký khóa học nào. Hãy qua tab 'Khám phá Khóa học' để chọn môn học yêu thích nhé!")
                    else:
                        st.write(f"Bạn đang tham gia **{len(my_courses)}** khóa học:")

                        for index, mc in enumerate(my_courses):
                            with st.expander(f"📖 {mc['name']} ({mc['university']})"):
                                col_info1, col_info2 = st.columns(2)
                                with col_info1:
                                    st.write(f"📅 **Ngày đăng ký:** {mc['date_enrolled']}")
                                with col_info2:
                                    st.write(f"🎯 **Trạng thái:** `{mc['status']}`")

                                btn_col1, btn_col2 = st.columns([1, 1])
                                with btn_col1:
                                    if st.button("Xem chi tiết khoá học", key=f"my_rec_{mc['id']}_{index}"):
                                        st.session_state.selected_course_id = mc['id']
                                        st.rerun()
                                with btn_col2:
                                    if st.button("❌ Hủy khóa học", key=f"unenroll_{mc['id']}_{index}",
                                                 use_container_width=True):
                                        unenroll_payload = {"user_id": st.session_state.user_id, "course_id": mc['id']}
                                        un_res = requests.post(f"{BACKEND_URL}/api/unenroll/", json=unenroll_payload)
                                        if un_res.status_code == 200:
                                            st.toast("Đã hủy khóa học thành công!", icon="🗑️")
                                            st.rerun()
                                        else:
                                            st.error("Không thể hủy khóa học.")
                else:
                    st.error("Không thể tải danh sách khóa học cá nhân.")
            except Exception:
                st.error("Lỗi kết nối máy chủ khi tải tiến độ học tập.")