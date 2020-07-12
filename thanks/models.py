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
    giver = models.ForeignKey(User, on_delete=models.CASCADE)           # 感謝をする人
    recipients = models.ManyToManyField(Profile)                        # 感謝される人
    content = models.TextField()                                        # 内容
    good_count = models.IntegerField(default=0)                         # いいね数
    date_posted = models.DateTimeField(default=timezone.now)            # 投稿された時間
    approval = models.IntegerField(choices=EXAMPLE_APPROVAL, default=0) # 承認 (済み/待ち)
    reward_exp = models.IntegerField(default=0)                         # 贈呈されるexp


    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('thanks-detail', kwargs={'pk': self.pk})


# いいね（いいにをされるThanks／いいねを押す人）
class Good_thanks(models.Model):
    good_thanks = models.ForeignKey(Thanks, on_delete=models.CASCADE)
    thanks_good_giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thanks_good_giver')
    