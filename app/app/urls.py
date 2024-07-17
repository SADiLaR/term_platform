"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from . import views

admin.site.index_title = _("SADiLaR Administration")
admin.site.site_title = _("SADiLaR Site Admin Portal")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("_health/", views.health, name="health"),
    path("", views.home, name="home"),
    path("institutions/", views.institutions, name="institutions"),
    path("projects/", views.projects, name="projects"),
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("institution/<int:institution_id>/", views.institution_detail, name="institution_detail"),
    path("documents/<int:document_id>/", views.document_detail, name="document_detail"),
    path("language/<int:pk>/", views.language_detail, name="language_detail"),
    path("subject/<int:pk>/", views.subject_detail, name="subject_detail"),
    path("search/", views.search, name="search"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("accounts.urls"), name="accounts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
