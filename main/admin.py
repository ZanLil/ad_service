from django.contrib import admin

from .models import Ad, MediaFile, Response


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Представление объявления в админке."""
    pass


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """Представление медиа-файла в админке."""
    pass


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """Представление отклика в админке."""
    pass
