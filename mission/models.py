from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from user.models import Profile

EXAMPLE_FLG = (
    (0, '実践中'),
    (1, '達成')
)
class Mission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    mission_flg = models.IntegerField(choices=EXAMPLE_FLG, default=0)  # 達成状況(0:実践中 / 1:達成)
    cost_exp = models.IntegerField(default=3)                          # 作成時に消費されるポイント(使えていない)
    success_exp = models.IntegerField(default=10)                      # クリア報酬ポイント
    good_count = models.IntegerField(default=0)                        # いいね数
    participants = models.IntegerField(default=0)                      # 参加者数
    participants_list_text = models.CharField(max_length=200, default='')          # 参加者リスト(文字列で保存)
    participants_list = models.ManyToManyField(Profile)                # 参加者リスト(他対他)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mission-detail', kwargs={'pk': self.pk})
    

# いいねを押す人 / いいねを押されるMission
class Good(models.Model):
    good_mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    good_giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_giver')
