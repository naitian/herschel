""" Models for submissions application """
import os.path

from django.db import models
from django.conf import settings

from ._drive_utils import authenticate, upload_to_team_drive

# Create your models here.
class Artist(models.Model):
    """ Artist model """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pseudonym = models.CharField(max_length=50, blank=True)
    email = models.EmailField()

    SCHOOL_AFFILIATIONS = [
        ("", "N/A"),
        ("ARCH", "Architecture & Urban Planning"),
        ("STAMPS", "Art & Design"),
        ("ROSS", "Business"),
        ("DENT", "Dentistry"),
        ("EDU", "Education"),
        ("ENGR", "Engineering"),
        ("ENVR", "Environment and Sustainability"),
        ("INFO", "Information"),
        ("KINES", "Kinesiology"),
        ("LAW", "Law"),
        ("LSA", "Literature, Science, and the Arts"),
        ("MED", "Medicine"),
        ("SMTD", "Music, Theatre & Dance"),
        ("NURSE", "Nursing"),
        ("PHARM", "Pharmacy"),
        ("SPH", "Public Health"),
        ("FORD", "Public Policy"),
        ("GRAD", "Rackham School of Graduate Studies"),
        ("SOCW", "Social Work"),
    ]
    affiliation = models.CharField(
        max_length=6, choices=SCHOOL_AFFILIATIONS, blank=True
    )

    YEAR_STANDING = [
        ("", "N/A"),
        ("FRESHMAN", "Freshman"),
        ("SOPHOMORE", "Sophomore"),
        ("JUNIOR", "Junior"),
        ("SENIOR", "Senior"),
        ("GRADUATE", "Graduate"),
        ("STAFF", "Staff"),
        ("FACULTY", "Faculty"),
        ("ALUMNUS", "Alumnus"),
    ]
    standing = models.CharField(max_length=10, choices=YEAR_STANDING, blank=True)
    major_field = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


def _get_submission_path(instance, filename):
    return "submissions/{}/{}".format(instance.category, filename)


class Submission(models.Model):
    """ Submissions model"""

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    CATEGORIES = [
        ("POETRY", "Poetry"),
        ("PROSE", "Prose"),
        ("PHOTO", "Photography"),
        ("VIS", "Visual Art"),
        ("OTHER", "Other"),
    ]
    category = models.CharField(max_length=10, choices=CATEGORIES)

    attachment = models.FileField(upload_to=_get_submission_path)
    drive_id = models.CharField(max_length=44, blank=True, null=True)
    drive_url = models.URLField(blank=True, null=True)

    def sync_to_drive(self):
        """
        Uploads file to Google Drive and sets the `drive_url`
        """
        service = authenticate()
        metadata = {
            "name": os.path.basename(self.attachment.name),
            "parents": [settings.GOOGLE_DRIVE_FOLDER_IDS[self.category]],
        }
        self.drive_id = upload_to_team_drive(service, metadata, self.attachment.path)
        self.drive_url = "https://drive.google.com/file/d/{}/view".format(self.drive_id)
        self.save(update_fields=['drive_id', 'drive_url'])

    def __str__(self):
        return '"{}" by {}'.format(self.title, self.artist)
