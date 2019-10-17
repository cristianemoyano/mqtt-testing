from django.db import models


class Post(models.Model):
    topic = models.CharField(max_length=200, blank=True, null=True)
    payload = models.TextField()
    host = models.CharField(max_length=200, blank=True, null=True)
    qos = models.CharField(max_length=10, blank=True, null=True)
    port = models.CharField(max_length=10, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Topic: {t} - Payload {p}".format(
            t=self.topic,
            p=self.payload,
        )
