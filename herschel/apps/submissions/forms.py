from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Artist, Submission


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ["title", "category", "attachment"]


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = [
            "first_name",
            "last_name",
            "pseudonym",
            "email",
            "affiliation",
            "standing",
            "major_field",
        ]

        labels = {
            'pseudonym': _('Pseudonym (Optional)'),
        }
