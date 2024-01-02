from django.db import models

# Create your models here.
class UploadedVideo(models.Model):
    video = models.FileField(upload_to='uploads/')

class Subs(models.Model):
    subtitles = models.FileField(upload_to='subs/', blank=True)
    video = models.ForeignKey(UploadedVideo, on_delete=models.CASCADE)

