from django.db import models


class Post(models.Model):
    topic = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic + self.text
