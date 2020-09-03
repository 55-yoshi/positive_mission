from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, UserCreateForm
from .models import Profile
from mission.models import Mission

def expmain(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(user__username=request.user.username)
        profile = profiles[0]
        
        my_missions = Mission.objects.filter(author=request.user)   # 自分が作成したミッション
        join_missions = profile.mission_set.all                     # 自分が参加したミッション    

        contents = {
            "profile": profile,
            "my_missions": my_missions,
            "join_missions": join_missions,
        }
    else:
        contents = {}
    return render(request, 'user/expmain.html', contents)

def join_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(user__username=request.user.username)
        profile = profiles[0]
        
        my_missions = Mission.objects.filter(author=request.user)   # 自分が作成したミッション
        join_missions = profile.mission_set.all                     # 自分が参加したミッション    

        contents = {
            "profile": profile,
            "my_missions": my_missions,
            "join_missions": join_missions,
        }
    else:
        contents = {}
    return render(request, 'user/join_list.html', contents)

    


def signup(request):
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid(
    ) and profile_form.is_valid():

        # Userモデルの処理。ログインできるようis_activeをTrueにし保存
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        # Profileモデルの処理。↑のUserモデルと紐づけ
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect("login")

    contents = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'user/signup.html', contents)


# メンバー管理ページ
def management(request):
    all_profile_ = Profile.objects.all()
    all_profile = sorted(all_profile_, key=lambda x: x.exp_total, reverse=True)
    contents = {
        'all_profile': all_profile,
        'profile': Profile.objects.get(user=request.user)
        }

    return render(request, 'user/management.html', contents)

def Reset(request):
    for a in Profile.objects.all():
        a.exp_total = 0
        a.mission_create_count = 0
        a.join_count = 0
        a.my_success_count = 0
        a.team_success_count = 0
        a.thanks_count = 0
        a.thanked_count = 0
        a.save()
    return redirect('management')