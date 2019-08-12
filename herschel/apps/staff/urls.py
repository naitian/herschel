from django.urls import path, re_path, include

from .views import dashboard, submissions, submission_details

urlpatterns = [
    path('submissions/<int:submission_id>', submission_details, name="submission_detail"),
    path('submissions', submissions, name='submissions_index'),
    re_path('^$', dashboard, name='dashboard'),
]
