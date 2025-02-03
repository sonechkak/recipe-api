from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls"), name="user"),
    path("api/recipe/", include("recipe.urls"), name="recipe"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
