from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.urls import path, include

from config import settings
from monitoring.forms import InglizchaErrorChiqarmaslik
from monitoring.views import register_view, LogOut

urlpatterns = [] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    # path('', HomePageView.as_view(), name='home'),
    # path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
    path('', include('monitoring.urls')),
    path('logout/', LogOut.as_view(), name='logout'),
    path('login/', LoginView.as_view(authentication_form=InglizchaErrorChiqarmaslik, redirect_authenticated_user=True),
         name='login'),
    # path('login/', PasswordResetConfirmView.as_view(help_text=None), name='login'),
    path('', include("django.contrib.auth.urls")),
    path('register/', register_view, name='register'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
