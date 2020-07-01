from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, UserCreateForm
from .models import Profile
from exp.views import total_exp
from mission.models import Mission

def expmain(request):

    if request.user.is_authenticated:
        # profile = Profile.objects.get(user=request.user)
        
        profiles = Profile.objects.filter(user__username=request.user.username)
        profile = profiles[0]
        
        my_missions = Mission.objects.filter(author=request.user)   # 自分が作成したミッション
        join_missions = profile.mission_set.all                     # 自分が参加したミッション
        # all_profile = Profile.objects.all()

        contents = {
            "profile": profile,
            "total_exp": total_exp,
            "my_missions": my_missions,
            "join_missions": join_missions,
            # "all_profile": all_profile,
        }
    else:
        contents = {}
    return render(request, 'user/expmain.html', contents)

    


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

def management(request):
    all_profile = Profile.objects.all()
    # for item in all_profile:
    #     my_mission = Mission.objects.filter(author=item.user)  # 作成したミッション
        # join_missions = item.mission_set.all.count()                   # 参加したミッション
    
    contents = {
        'all_profile': all_profile,
        'name': 'a',
        'exp': 'b',
        # 'my_mission': my_mission,
        'success': 'd',
    }
    return render(request, 'user/management.html', contents)