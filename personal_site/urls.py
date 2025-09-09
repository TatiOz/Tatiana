"""
URL configuration for personal_site project.

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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static

custom_admin_path = 'secure-panel/'  # change this to any custom path you prefer

urlpatterns = [
    path(custom_admin_path, admin.site.urls),
    # Redirect default /admin/ to home
    re_path(r'^admin/?$', RedirectView.as_view(url='/', permanent=False)),
    path('', include(('main.urls', 'main'), namespace='main')),
]

# Simple robots.txt and sitemap.xml
urlpatterns += [
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /secure-panel/\nSitemap: /sitemap.xml\n", content_type="text/plain")),
    path('sitemap.xml', lambda r: HttpResponse((
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        f"  <url><loc>{r.build_absolute_uri('/')[:-1]}/</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        f"  <url><loc>{r.build_absolute_uri('/about/')}</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        f"  <url><loc>{r.build_absolute_uri('/skills/')}</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        f"  <url><loc>{r.build_absolute_uri('/contact/')}</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        f"  <url><loc>{r.build_absolute_uri('/privacy/')}</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        f"  <url><loc>{r.build_absolute_uri('/impressum/')}</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        f"  <url><loc>{r.build_absolute_uri('/cookies/')}</loc><lastmod>{timezone.now().date()}</lastmod></url>\n"
        "</urlset>\n"
    ), content_type="application/xml")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
