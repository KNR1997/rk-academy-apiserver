from .settings import urlpatterns as settings_urls
from .subject import urlpatterns as subject_urls

urlpatterns = [
    *settings_urls,
    *subject_urls,
]
