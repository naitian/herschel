from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from ..submissions.models import Submission


class Review(models.Model):
    """ Review model"""

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} - {} ({})".format(self.submission, self.reviewer, self.rating)
