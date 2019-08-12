from django.db import models

# Create your models here.
class Magazine(models.Model):
    """Docstring for Magazine. """
    title = models.CharField(max_length=50)
    issue = models.IntegerField()
    url = models.URLField()
    img_url = models.URLField()

    def __str__(self):
        return "{} (Issue {})".format(self.title, self.issue)
