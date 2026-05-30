import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def show_course_list_page():
    st.header("🔍 Tìm kiếm & Khám phá Khóa học")

    #Khởi tạo các biến trạng thái
    if "current_course_page" not in st.session_state:
        st.session_state.current_course_page = 1
    if "loaded_courses" not in st.session_state:
        st.session_state.loaded_courses = []
    if "has_next_page" not in st.session_state:
        st.session_state.has_next_page = False

    common_univs = [
        "Massachusetts Institute of Technology",
        "Harvard University",
        "The University of Queensland",
        "The University of Michigan",
        "University of Adelaide",
        "Curtin University",
        "Delft University of Technology",
        "edX"
    ]

    #Giao diện bộ lọc
    col1, col2, col3 = st.columns([2, 1, 1])

    search_q = col1.text_input("Nhập từ khóa tìm kiếm (Tên môn học...)", "")
    level_q = col2.selectbox(
        "Chọn cấp độ khó", ["Tất cả", "Beginner", "Intermediate", "Advanced"]
    )
    univ_q = col3.selectbox("Chọn trường Đại học", ["Tất cả"] + sorted(common_univs))

    api_search = search_q.strip()
    api_level = "" if level_q == "Tất cả" else level_q
    api_univ = "" if univ_q == "Tất cả" else univ_q

    current_filter_state = f"{api_search}_{api_level}_{api_univ}"

    if "last_filter_state" not in st.session_state:
        st.session_state.last_filter_state = current_filter_state

    if current_filter_state != st.session_state.last_filter_state:
        st.session_state.current_course_page = 1
        st.session_state.loaded_courses = []
        st.session_state.last_filter_state = current_filter_state

    #Gọi api phân trang
    params = {
        "search": api_search,
        "level": api_level,
        "university": api_univ,
        "page": st.session_state.current_course_page
    }

    if st.session_state.current_course_page == 1 and not st.session_state.loaded_courses:
        should_fetch = True
    elif st.session_state.current_course_page > 1:
        should_fetch = True
    else:
        should_fetch = False

    if should_fetch:
        try:
            res = requests.get(f"{BACKEND_URL}/api/courses/", params=params)
            if res.status_code == 200:
                result_data = res.json()
                new_courses = result_data.get("courses", [])
                st.session_state.has_next_page = result_data.get("has_next", False)

                if st.session_state.current_course_page == 1:
                    st.session_state.loaded_courses = new_courses
                else:
                    already_loaded_ids = {c['id'] for c in st.session_state.loaded_courses}
                    for nc in new_courses:
                        if nc['id'] not in already_loaded_ids:
                            st.session_state.loaded_courses.append(nc)
            else:
                st.error("Không thể tải danh sách khóa học từ Backend.")
        except Exception:
            st.error("Lỗi kết nối hệ thống khi hiển thị danh sách.")

    #Hiển thị số lượng khoá học đang hiện
    st.write(f"Đang hiển thị **{len(st.session_state.loaded_courses)}** khóa học phù hợp.")
    st.divider()

    #Hiển thị danh sách khoá học
    with st.container(height=500, border=True):
        if not st.session_state.loaded_courses:
            st.info("Không tìm thấy khóa học nào phù hợp với bộ lọc.")
        else:
            for idx, c in enumerate(st.session_state.loaded_courses):
                c_col1, c_col2 = st.columns([4, 1])
                with c_col1:
                    st.subheader(c["name"])
                    st.caption(f"🏛️ {c['university']} | 📈 Cấp độ: {c['difficulty_level']}")
                with c_col2:
                    st.write("")
                    if st.button("Xem chi tiết", key=f"btn_{c['id']}_{idx}", use_container_width=True):
                        st.session_state.selected_course_id = c["id"]
                        st.rerun()
                st.divider()

    #Nút xem thêm để add thêm khoá học vào danh sách hiển thị
    if st.session_state.has_next_page:
        st.write("")
        if st.button("🔽 Xem thêm khóa học", key="load_more_courses_btn", use_container_width=True):
            st.session_state.current_course_page += 1
            st.rerun()