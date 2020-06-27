from django.db import models
from django.contrib.auth.models import User

KUBUN_CHOICES = (
    ('1', '経営者'),
    ('2', '従業員'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kubun = models.CharField(verbose_name='区分',
                             max_length=2,
                             choices=KUBUN_CHOICES,
                             blank=True)
    exp_total = models.IntegerField(verbose_name='経験値', default=10)

    def __str__(self):
        return self.user.username