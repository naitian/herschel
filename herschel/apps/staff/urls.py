from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path(
        "submissions/<int:submission_id>", submission_details, name="submission_detail"
    ),
    path("submissions", submissions, name="submissions_index"),
    path("csv/ratings", ratings_csv, name="ratings_csv"),
    path("csv/artists", artists_csv, name="artists_csv"),
    re_path("^$", dashboard, name="dashboard"),
]
