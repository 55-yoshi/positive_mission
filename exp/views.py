from mission import models
from django.shortcuts import redirect, render
from mission.models import Mission, Good
from user.models import Profile 
from django.contrib import messages

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


# いいねボタンが押されたときの動作
def MissionGood(request, pk):
    try:
        mission = models.Mission.objects.get(pk=pk)
    except Mission.DoesNotExist:
        raise Http404
    
    push_count = Good.objects.filter(good_giver=request.user).filter(good_mission=mission).count()
    profile = Profile.objects.get(user__username=request.user.username)  #いいねを押す人
    author_profile = Profile.objects.get(user=mission.author)  # いいねされるミッション投稿者のプロフィール

    

    if push_count > 0:
        good_on = Good.objects.get(good_giver=request.user, good_mission=mission)
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
    good = Good()
    good.good_giver = request.user
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


    items = mission.participants_list.all()   #全ての参加者のプロフィールのリスト

    if participant in items:  # もし保存された参加者の中に本人の名前が含まれていたら
        mission.participants -= 1
        for item in items:
            if item == participant:
                mission.participants_list.remove(participant)
                mission.save()
                messages.success(request, 'このMissionから脱退しました。')
                return redirect('mission-detail', pk)
    else:
        mission.participants += 1
        mission.save()
        mission.participants_list.add(participant)
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
    author_profile.save()
    items = mission.participants_list.all()
    # ミッション参加者
    for item in items:
        item.exp_total += mission.success_exp
        item.save()
    return redirect('mission-detail', pk)

    # 文字列型
    # s = mission.participants_list_text
    # items = [x.strip() for x in s.split(',') if not s == '']  # 参加者の空白以外の文字列を’,’で分割しリスト化する。

    # for item in items:
    #     participant_profile = Profile.objects.get(user__username=item)   #参加者のプロフィール
    #     participant_profile.exp_total += mission.success_exp
    #     participant_profile.save()
    # return redirect('mission-detail', pk)
