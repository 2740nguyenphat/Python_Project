import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def show_ranking_sidebar():
    st.html("""
        <style>
        /* CSS tạo giao diện Card hiện đại, sạch sẽ */
        .ranking-card {
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            background-color: #ffffff;
        }
        .ranking-card:hover {
            border-color: #3b82f6;
            background-color: #f8fafc;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.05);
            transform: translateY(-1px);
        }
        .course-name {
            font-weight: 600;
            font-size: 0.9rem;
            color: #1e293b;
            margin-bottom: 4px;
            /* Giới hạn tên khóa học tối đa 2 dòng */
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .course-meta {
            font-size: 0.75rem;
            color: #64748b;
            display: flex;
            align-items: center;
            gap: 4px;
            /* Đảm bảo dòng meta không bị vỡ bố cục khi text quá dài */
            width: 100%;
            overflow: hidden;
        }
        .uni-name {
            /* Giới hạn tên trường học tối đa 1 dòng */
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex: 1; /* Tự động kéo giãn và chiếm không gian còn lại */
        }
        .meta-stat {
            white-space: nowrap; /* Không cho phép số liệu view/rating bị xuống dòng */
        }
        </style>
    """)

    st.markdown("### 🔥 Top Xu Hướng")

    rank_tab_day, rank_tab_week, rank_tab_month, rank_tab_all = st.tabs([
        "Ngày", "Tuần", "Tháng", "Tất cả"
    ])

    periods_mapping = {
        rank_tab_day: "day",
        rank_tab_week: "week",
        rank_tab_month: "month",
        rank_tab_all: "all"
    }

    for tab_obj, period_code in periods_mapping.items():
        with tab_obj:
            try:
                rank_res = requests.get(f"{BACKEND_URL}/api/courses/ranking/", params={"period": period_code})
                if rank_res.status_code == 200:
                    ranking_list = rank_res.json().get("ranking", [])

                    if not ranking_list:
                        st.caption("ℹ️ Chưa có dữ liệu.")
                    else:
                        for idx, item in enumerate(ranking_list[:5]):
                            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx + 1}"

                            with st.container():
                                st.html(f"""
                                    <div class="ranking-card">
                                        <div class="course-name">{item['name']}</div>
                                        <div class="course-meta">
                                            <span>{medal}</span>
                                            <span class="uni-name">{item['university']}</span>
                                            <span class="meta-stat">📈 {item['unique_users']} view</span>
                                        </div>
                                    </div>
                                """)
                else:
                    st.error("Lỗi tải dữ liệu.")
            except Exception:
                st.error("Lỗi kết nối.")

    st.markdown("### ⭐ Đánh Giá Cao")

    try:
        rating_res = requests.get(f"{BACKEND_URL}/api/courses/rating-ranking/")
        if rating_res.status_code == 200:
            rating_list = rating_res.json().get("ranking", [])

            if not rating_list:
                st.caption("ℹ️ Chưa có nhận xét.")
            else:
                for idx, item in enumerate(rating_list[:5]):
                    medal = "🏆" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx + 1}"

                    with st.container():
                        st.html(f"""
                            <div class="ranking-card">
                                <div class="course-name">{item['name']}</div>
                                <div class="course-meta">
                                    <span>{medal}</span>
                                    <span class="uni-name">{item['university']}</span>
                                    <span class="meta-stat">⭐ {item['avg_rating']}/5.0 ({item['review_count']})</span>
                                </div>
                            </div>
                        """)
        else:
            st.error("Lỗi tải dữ liệu.")
    except Exception:
        st.error("Lỗi kết nối.")
