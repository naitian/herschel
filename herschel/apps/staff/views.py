from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import ReviewForm
from .models import Review
from ..submissions.models import Submission

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
