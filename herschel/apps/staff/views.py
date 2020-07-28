import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..submissions.models import Submission, Artist
from .forms import ReviewForm
from .models import Review


# Create your views here.
@login_required
def dashboard(request):
    """ Staff dashboard

    :request: TODO
    :returns: TODO

    """
    return render(request, "staff/dashboard.html")


@login_required
def submissions(request):
    """ Index for reviewing submissions

    :request: TODO
    :returns: TODO

    """
    reviewed = Submission.objects.filter(review__reviewer=request.user)
    todo = Submission.objects.exclude(review__reviewer=request.user)

    if todo.count() == 0:
        message = "Nice job!"
    elif todo.count() <= 5:
        message = "Let's knock those last few out!"
    else:
        message = "Better get started!"

    context = {
        "reviewed": reviewed,
        "todo": todo,
        "total_reviews": reviewed.count() + todo.count(),
        "num_reviews": reviewed.count(),
        "message": message,
    }

    return render(request, "staff/submissions.html", context)


@login_required
def submission_details(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    embed_url = submission.drive_url[:-4] + "preview"
    try:
        review = Review.objects.get(reviewer=request.user, submission=submission)
    except Review.DoesNotExist:
        review = None
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        review = review_form.save(commit=False)
        review.reviewer = request.user
        review.submission = submission
        review.save()
    else:
        review_form = ReviewForm(instance=review)
    return render(
        request,
        "staff/submission_details.html",
        {
            "submission": submission,
            "embed_url": embed_url,
            "review": review,
            "review_form": review_form,
        },
    )


@staff_member_required
def ratings_csv(request):
    response = HttpResponse(content_type="text/csv")
    reviewers = [u.username for u in User.objects.all()]
    spreadsheet = csv.DictWriter(
        response, ["title", "type", "artist", "drive", "pseudonym", "email"] + reviewers
    )
    spreadsheet.writeheader()
    for s in Submission.objects.all():
        outdict = {
            "title": s.title,
            "type": s.category,
            "artist": str(s.artist),
            "pseudonym": s.artist.pseudonym,
            "drive": s.drive_url,
            "email": s.artist.email,
        }
        for r in s.review_set.all():
            outdict[r.reviewer.username] = r.rating
        spreadsheet.writerow(outdict)
    return response


@staff_member_required
def artists_csv(request):
    response = HttpResponse(content_type="text/csv")
    spreadsheet = csv.DictWriter(
        response,
        ["first_name", "last_name", "pseudonym", "email", "standing", "major_field"],
    )
    spreadsheet.writeheader()
    for a in Artist.objects.all():
        outdict = {
            "first_name": a.first_name,
            "last_name": a.last_name,
            "pseudonym": a.pseudonym,
            "email": a.email,
            "standing": a.email,
            "major_field": a.major_field,
        }
        spreadsheet.writerow(outdict)
    return response


@login_required
def emails(request):
    """ Dashboard for email sending

    :request: TODO
    :returns: TODO

    """
    pass


def login_view(request):
    """ Login view
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("dashboard")
        # Return an 'invalid login' error message.
        return render(request, "submissions/login.html", {"error": "Invalid Login"})
    return render(request, "submissions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")
