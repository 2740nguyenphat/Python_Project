import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def show_auth_page():
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        st.subheader("🔑 Đăng nhập tài khoản")
        tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký tài khoản"])

        with tab1:
            st.write("Vui lòng đăng nhập tài khoản để vào hệ thống quản lý khóa học.")
            login_user = st.text_input("Tên đăng nhập", key="auth_login_user")
            login_pass = st.text_input("Mật khẩu", type="password", key="auth_login_pass")

            if st.button("Xác nhận Đăng nhập", use_container_width=True, key="auth_login_btn"):
                if login_user and login_pass:
                    payload = {"username": login_user, "password": login_pass}
                    try:
                        res = requests.post(f"{BACKEND_URL}/api/login/", json=payload)
                        if res.status_code == 200:
                            data = res.json()

                            #Kiểm tra quyền
                            if data.get("is_admin", False):
                                st.success(
                                    "👨‍💼 Tài khoản Admin chính xác! Đang chuyển hướng sang hệ thống Django Admin...")

                                django_admin_url = f"{BACKEND_URL}/admin/"
                                js_redirect = f"""
                                <script>
                                    window.open("{django_admin_url}", "_blank"); // Mở trang Django Admin ở một tab mới
                                </script>
                                """
                                st.components.v1.html(js_redirect, height=0)
                            else:
                                st.session_state.logged_in = True
                                st.session_state.user_id = data["user_id"]
                                st.session_state.username = data["username"]
                                st.success("🎉 Đăng nhập thành công!")
                                st.rerun()
                        else:
                            st.error(res.json().get("error", "Sai tài khoản hoặc mật khẩu."))
                    except Exception:
                        st.error("Không thể kết nối đến Backend Django server.")
                else:
                    st.warning("Vui lòng điền đầy đủ thông tin.")

        with tab2:
            st.write("Tạo tài khoản học viên mới tại đây.")
            reg_user = st.text_input("Tên tài khoản mong muốn", key="auth_reg_user")
            reg_email = st.text_input("Địa chỉ Email", key="auth_reg_email")
            reg_pass = st.text_input("Mật khẩu", type="password", key="auth_reg_pass")

            if st.button("Xác nhận Đăng ký", use_container_width=True, key="auth_reg_btn"):
                if reg_user and reg_pass:
                    payload = {"username": reg_user, "password": reg_pass, "email": reg_email}
                    try:
                        res = requests.post(f"{BACKEND_URL}/api/signup/", json=payload)
                        if res.status_code == 200:
                            st.success("🚀 Đăng ký thành công! Mời bạn chuyển qua Tab Đăng nhập.")
                        else:
                            st.error(res.json().get("error", "Tên đăng nhập đã tồn tại."))
                    except Exception:
                        st.error("Không thể kết nối đến Backend Django server.")
                else:
                    st.warning("Vui lòng nhập tên tài khoản và mật khẩu.")