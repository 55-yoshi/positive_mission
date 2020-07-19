from mission import models
from django.shortcuts import redirect, render
from mission.models import Mission, Good_mission
from thanks.models import Thanks, Good_thanks
from user.models import Profile 
from django.contrib import messages
# from .forms import ApprovalForm
from django.http import HttpResponse
from django.http import Http404
from django.utils import timezone


# expを合計する機能
def total_exp():
    #①「初期値or確定済(exp)」をProfile.exp_totalから取得する。
    #②依頼したミッション（クリアしていない）の「獲得exp（use_exp）」の合計を取得する。
    #　※依頼者は、「獲得exp（use_exp）」をインセンティブとして提供することで良かったでしょうか。
    #③依頼したミッション（クリアしていない）の「いいね（add_exp）」の合計を取得する。
    #④参加したミッション（クリアしていない）の「獲得exp（use_exp）/参加人数」の合計を取得する。
    #　※参加者は、獲得exp（use_exp）を参加人数で山分けで良かったでしょうか。
    #⑤合計計算「①-②+③+④」とする。
    #注意：ミッションがクリアしたときに、Profile.exp_totalを更新する仕様で考えています。
    return


# いいねのexp加算する機能
# ※以下のMissionLike()で行っているので不要かと思います。
def good_count():
    return


# ミッション作成時にuse_expを消費する機能
# ※ミッションがクリアしたときに、Profile.exp_totalを更新する仕様で考えています。
#   need_gain()の「１、依頼者」の処理が該当します。
def need_exp():
    return


# ミッションクリア時にuse_expを配分する機能
def need_gain():
    #１、依頼者
    #  ①依頼者の「初期値or確定済(exp)」をProfile.exp_totalから取得する。
    #  ②ミッションの「獲得exp（use_exp）」を取得する。
    #  ③更新expを算出（①-②）する。
    #  ④依頼者の「初期値or確定済(exp)」を更新expで更新する。
    #２、参加者
    #  ①ミッションの参加者数をProfile.missionから取得する。
    #  ②ミッションの「獲得exp（use_exp）」を取得する。
    #  ③配分expを算出（②/①）する。
    #  ③ミッションの参加者数分以下の処理を繰り返す。
    #    ③.1 参加者の「初期値or確定済(exp)」をProfile.exp_totalから取得する。
    #    ③.2 更新expを算出（③+(③.1)）する。
    #    ③.3 参加者の「初期値or確定済(exp)」を更新expで更新する。
    return


# 投稿されたミッションに対していいねボタンが押されたときの動作
def MissionGood(request, pk):
    try:
        mission = models.Mission.objects.get(pk=pk)
    except Mission.DoesNotExist:
        raise Http404
    
    push_count = Good_mission.objects.filter(mission_good_giver=request.user).filter(good_mission=mission).count()
    profile = Profile.objects.get(user__username=request.user.username)  #いいねを押す人
    author_profile = Profile.objects.get(user=mission.author)  # いいねされるミッション投稿者のプロフィール

    

    if push_count > 0:
        good_on = Good_mission.objects.get(mission_good_giver=request.user, good_mission=mission)
        good_on.delete()
        mission.good_count -= 1
        mission.save()
        profile.exp_total -= 1
        profile.save()
        author_profile.exp_total -= 1
        author_profile.save()
        messages.success(request, f'いいねを取り消しました。{ profile.user }さんと、{ author_profile.user }さんにマイナス１ポイント。')
        return redirect('mission-detail', pk)

    mission.good_count += 1
    mission.save()
    profile.exp_total += 1
    profile.save()
    author_profile.exp_total += 1
    author_profile.save()
    good = Good_mission()
    good.mission_good_giver = request.user
    good.good_mission = mission
    good.save()

    messages.success(request, f'このMissionにいいねしました！{ profile.user }さんと、{ author_profile.user }さんにプラス１ポイント!')
    return redirect('mission-detail', pk)


# 参加するボタンが押されたときの動作(文字列型)

# def MissionJoin(request, pk):
#     try:
#         mission = Mission.objects.get(pk=pk)
#     except Mission.DoesNotExist:
#         raise Http404

#     # profile = Profile.objects.get(user__username=request.user.username)
#     # profile.join_mission.add(mission)
#     # profile.save()

#     participant = request.user.get_username()     # ボタンを押す人
#     s = mission.participants_list_text
#     items = [x.strip() for x in s.split(',') if not s == '']  # 参加者の空白以外の文字列を’,’で分割しリスト化する。

#     if participant in mission.participants_list_text:  # もし保存された参加者の中に本人の名前が含まれていたら
#         mission.participants -= 1
#         for item in items:
#             if item == participant:
#                 items.remove(item)
#                 mission.participants_list_text = ','.join(items)  # リスト型を文字列に戻して保存
#                 mission.save()
#                 messages.success(request, 'このMissionから脱退しました。')
#                 return redirect('mission-detail', pk)
#     else:
#         mission.participants += 1
#         items.append(participant)
#         mission.participants_list_text = ','.join(items)
#         mission.save()
#         messages.success(request, 'このMissionに参加しました！')
#         return redirect('mission-detail', pk)


# 参加するボタンが押されたときの動作
def MissionJoin(request, pk):
    try:
        mission = Mission.objects.get(pk=pk)
    except Mission.DoesNotExist:
        raise Http404

    participant = Profile.objects.get(user=request.user)    # ボタンを押す人のプロフィール
    items = mission.participants_list.all()                 # 全ての参加者のプロフィールのリスト

    # もし保存された参加者の中に本人の名前が含まれていたら
    if participant in items:  
        mission.participants -= 1
        participant.join_count -= 1
        participant.save()
        for item in items:
            if item == participant:
                mission.participants_list.remove(participant)
                mission.save()
                messages.success(request, 'このMissionから脱退しました。')
                return redirect('mission-detail', pk)
    elif mission.participants >= mission.participants_limit:
        messages.success(request, 'このミッションは既に定員に達しています。')
        return redirect('mission-detail', pk)
    else:
        mission.participants += 1
        mission.save()
        mission.participants_list.add(participant)
        participant.join_count += 1
        participant.save()
        messages.success(request, 'このMissionに参加しました！')
        return redirect('mission-detail', pk)





#  ミッションクリアボタンが押されたときの動作
def MissionSuccess(request, pk):
    try:
        mission = Mission.objects.get(pk=pk)
    except Mission.DoesNotExist:
        raise Http404
    mission.mission_flg = 1
    mission.save()
    # ミッション作成者
    author_profile = Profile.objects.get(user=mission.author) 
    author_profile.exp_total += mission.success_exp + mission.participants
    author_profile.my_success_count += 1
    author_profile.save()
    # ミッション参加者
    items = mission.participants_list.all()
    for item in items:
        item.exp_total += mission.success_exp
        item.team_success_count += 1
        item.save()
    return redirect('mission-detail', pk)

    # 文字列型
    # s = mission.participants_list_text
    # items = [x.strip() for x in s.split(',') if not s == '']  # 参加者の空白以外の文字列を’,’で分割しリスト化する。

    # for item in items:
    #     participant_profile = Profile.objects.get(user__username=item)   #参加者のプロファイル
    #     participant_profile.exp_total += mission.success_exp
    #     participant_profile.save()
    # return redirect('mission-detail', pk)



# ミッション承認ボタン
def MissionApproval(request, pk):
    try:
        mission = Mission.objects.get(pk=pk)
    except Mission.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        mission.success_exp = request.POST['success_exp']
        mission.approval = 1
        mission.date_posted = timezone.now()
        mission.save()
        messages.success(request, 'このミッションを承認しました！')
        return redirect('mission-detail', pk)







# ___________________THANKS_____________________



# 投稿されたTHANKSに対していいねボタンが押されたときの動作
def ThanksGood(request, pk):
    try:
        thanks = Thanks.objects.get(pk=pk)
    except Thanks.DoesNotExist:
        raise Http404
    
    push_count = Good_thanks.objects.filter(thanks_good_giver=request.user).filter(good_thanks=thanks).count()
    profile = Profile.objects.get(user__username=request.user.username)    # いいねを押す人
    giver_profile = Profile.objects.get(user=thanks.giver)                 # いいねされるサンクスの投稿者のプロファイル
    # recipient_profile =      # 感謝される人のプロファイル
    

    if push_count > 0:
        good_on = Good_thanks.objects.get(thanks_good_giver=request.user, good_thanks=thanks)
        good_on.delete()
        thanks.good_count -= 1
        thanks.save()
        profile.exp_total -= 1
        profile.save()
        giver_profile.exp_total -= 1
        giver_profile.save()
        messages.success(request, f'いいねを取り消しました。{ profile.user }さんと、{ giver_profile.user }さんにマイナス１ポイント。')
        return redirect('thanks-detail', pk)

    thanks.good_count += 1
    thanks.save()
    profile.exp_total += 1
    profile.save()
    giver_profile.exp_total += 1
    giver_profile.save()
    good = Good_thanks()
    good.thanks_good_giver = request.user
    good.good_thanks = thanks
    good.save()

    messages.success(request, f'このThanksにいいねしました！{ profile.user }さんと、{ giver_profile.user }さんにプラス１ポイント!')
    return redirect('thanks-detail', pk)
  

# Thanks承認ボタン
def ThanksApproval(request, pk):
    try:
        thanks = Thanks.objects.get(pk=pk)
    except Thanks.DoesNotExist:
        raise Http404

    giver = Profile.objects.get(user=thanks.giver)   # 感謝する人（投稿者）
    recipient_list = thanks.recipients.all()         # 感謝される人達のプロファイルリスト

    if request.method == 'POST':
        thanks.reward_exp = request.POST['reward_exp']
        # 「承認待ち」から「承認済み」に変更。
        thanks.approval = 1
        # post時間を承認された時間に変更する。
        thanks.date_posted = timezone.now()
        thanks.save()
        # フォームで設定された’贈呈exp’を感謝される人達全員に配当し、「感謝された回数」プラス１。
        for recipient in recipient_list:
            recipient.exp_total += int(thanks.reward_exp)
            recipient.thanked_count += 1
            recipient.save()
        # 感謝する人（投稿者）に３expを与える。
        giver.exp_total += 3
        # 投稿者の「感謝回数」プラス１。
        giver.thanks_count += 1
        giver.save()
        messages.success(request, 'この投稿を承認しました！')
        messages.success(request, f'{ thanks.reward_exp }expが贈呈されました。')
        return redirect('thanks-detail', pk)