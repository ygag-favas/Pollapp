"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
#from polls.views import change_language

from polls import views

urlpatterns = [
    path('change_language/',    views.LanguageView.as_view(),
         name='change_language')
    #path('i18n/', include('django.conf.urls.i18n')),
]
    # path('account/', include('users.urls')),
    # path('', include('polls.urls')),
    # path('admin/', admin.site.urls),
    # path('account/', include('users.urls')),

urlpatterns += i18n_patterns(
    path('', include('polls.urls')),
    path('account/', include('users.urls')),
    path(_('admin/'), admin.site.urls),
    prefix_default_language=False,
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path('rosetta/', include('rosetta.urls'))
    ]