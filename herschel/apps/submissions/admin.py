from django.contrib import admin
from .models import Artist, Submission

# Register your models here.
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass
