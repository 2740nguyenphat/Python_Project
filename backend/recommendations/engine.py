import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from courses.models import Course


def calculate_course_recommendations(target_course_id, top_n=5):
    """
    Thuật toán Lọc dựa trên nội dung Content-Based Filtering
    Sử dụng TF-IDF Vectorizer và Cosine Similarity để tìm khóa học liên quan.
    """
    all_courses = Course.objects.all()
    if not all_courses.exists():
        return []

    corpus = []
    for course in all_courses:
        about_text = getattr(course, 'about', '')

        desc_text = getattr(course, 'description', '')

        combined_text = (
            f"{course.name} {course.university} "
            f"{about_text if about_text else ''} "
            f"{desc_text if desc_text else ''} "
            f"{course.difficulty_level}"
        )
        corpus.append({
            'id': course.id,
            'text': combined_text
        })

    df = pd.DataFrame(corpus)

    try:
        target_idx = df[df['id'] == target_course_id].index[0]
    except IndexError:
        return []

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['text'])
    cosine_sim = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[-(top_n + 1):-1][::-1]
    recommended_ids = [int(df.iloc[idx]['id']) for idx in similar_indices]
    return recommended_ids