from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import Profile
from django.utils import timezone

EXAMPLE_APPROVAL = (
    (0, '承認待ち'),
    (1, '承認済み'),
)

class Thanks(models.Model):
    giver = models.ForeignKey(User, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Profile)
    content = models.TextField()
    good_count = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    approval = models.IntegerField(choices=EXAMPLE_APPROVAL, default=0)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('thanks-detail', kwargs={'pk': self.pk})