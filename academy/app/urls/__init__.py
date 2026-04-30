from .academic_year import urlpatterns as academic_year_urls
from .analytic import urlpatterns as analytic_urls
from .conversation import urlpatterns as conversation_urls
from .course import urlpatterns as course_urls
from .enrollment import urlpatterns as enrollment_urls
from .grade_level import urlpatterns as grade_level_urls
from .message import urlpatterns as message_urls
# from .report import urlpatterns as reports_urls
from .settings import urlpatterns as settings_urls
from .student import urlpatterns as student_urls
from .subject import urlpatterns as subject_urls
from .teacher import urlpatterns as teacher_urls
from .user import urlpatterns as user_urls
from .video import urlpatterns as video_urls

urlpatterns = [
    *academic_year_urls,
    *analytic_urls,
    *course_urls,
    *enrollment_urls,
    *grade_level_urls,
    # *reports_urls,
    *settings_urls,
    *student_urls,
    *subject_urls,
    *teacher_urls,
    *user_urls,
    *conversation_urls,
    *message_urls,
    *video_urls,
]
