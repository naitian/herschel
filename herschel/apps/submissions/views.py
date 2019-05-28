from django.shortcuts import render


from .models import Artist
from .forms import ArtistForm, SubmissionForm

# Create your views here.
def submission_page(request):
    """TODO: Docstring for submission_page.

    :request: TODO
    :returns: TODO

    """
    if request.method == 'POST':
        artist_form = ArtistForm(request.POST)
        submission_form = SubmissionForm(request.POST, request.FILES)
        if submission_form.is_valid() and artist_form.is_valid():
            # TODO: make a better way of combining the same author
            a = artist_form.save(commit=False)
            artist, _ = Artist.objects.get_or_create(email=a.email)
            artist_form = ArtistForm(request.POST, instance=artist)
            artist = artist_form.save()
            submission = submission_form.save(commit=False)
            submission.artist = artist
            submission.save()
            return render(request, 'submissions/accept.html')
    else:
        submission_form = SubmissionForm()
        artist_form = ArtistForm()
    return render(request, 'submissions/submit.html', {'artist_form':
        artist_form, 'submission_form': submission_form})
