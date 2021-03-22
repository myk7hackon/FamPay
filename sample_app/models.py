from django.db import models

# Create your models here.


class VideoDetails(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000000)
    publishedAt = models.DateTimeField()
    videoId = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=["title"]), models.Index(fields=["description"])]
