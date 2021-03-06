from django.db import models
from django.contrib.auth.models import User

KUBUN_CHOICES = (
    ('1', '経営者'),
    ('2', '従業員'),
    ('3', '管理者'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kubun = models.CharField(verbose_name='区分',
                             max_length=2,
                             choices=KUBUN_CHOICES,)
    exp_total = models.IntegerField(verbose_name='経験値', default=10)
    mission_create_count = models.IntegerField(default=0)  # ミッション作成回数
    my_success_count = models.IntegerField(default=0)      # 自ら作成したミッションの達成数
    join_count = models.IntegerField(default=0)            # ミッション参加回数
    team_success_count = models.IntegerField(default=0)    # 参加したミッションの達成回数
    thanks_count = models.IntegerField(default=0)          # 感謝した回数
    thanked_count = models.IntegerField(default=0)         # 感謝された回数

    def __str__(self):
        return str(self.user)