"""Submissions application views"""

from django.shortcuts import render, redirect
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from .utils import send_email
from .models import Artist
from .forms import ArtistForm, SubmissionForm

# Create your views here.
def submission_page(request):
    """TODO: Docstring for submission_page.

    :request: TODO
    :returns: TODO

    """
    if request.method == "POST":
        artist_form = ArtistForm(request.POST)
        submission_form = SubmissionForm(request.POST, request.FILES)
        if submission_form.is_valid() and artist_form.is_valid():
            # TODO: make a better way of combining the same author
            temp_artist = artist_form.save(commit=False)
            artist, _ = Artist.objects.get_or_create(email=temp_artist.email)
            artist_form = ArtistForm(request.POST, instance=artist)
            artist = artist_form.save()
            submission = submission_form.save(commit=False)
            submission.artist = artist
            submission.save()
            submission.sync_to_drive()
            send_email(
                "emails/received_submission.txt",
                "emails/received_submission.html",
                {"artist": artist, "submission": submission},
                "Thanks for Submitting to Blueprint!",
                [artist.email],
            )
            return render(request, "submissions/received.html")
    else:
        submission_form = SubmissionForm()
        artist_form = ArtistForm()
    return render(
        request,
        "submissions/submit.html",
        {"artist_form": artist_form, "submission_form": submission_form},
    )
