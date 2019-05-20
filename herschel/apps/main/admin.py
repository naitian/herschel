from django.contrib import admin
from .models import Magazine

# Register your models here.
@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    pass
