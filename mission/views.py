from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.views.generic.edit import ModelFormMixin
from .models import Mission
from user.models import Profile
from . import models
from django.shortcuts import render
from exp.forms import MissionApprovalForm
from django.db.models import Q



class MissionListView(ListView):
    model = Mission
    template_name = 'mission/home.html'
    context_object_name = 'missions'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(MissionListView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  
        context["profile"] = profile
        return context

    def get_queryset(self):
        q_word = self.request.GET.get('query')

        if q_word:
            object_list = Mission.objects.filter(
                Q(author__username__icontains=q_word)|Q(participants_list__user__username__icontains=q_word)).order_by('-date_posted')
        else:
            object_list = Mission.objects.all().order_by('-date_posted')
        return object_list


class MissionDetailView(DetailView, ModelFormMixin):
    model = Mission
    template_name = 'mission/mission_detail.html'
    fields = ()

    def get_context_data(self, **kwargs):
        context = super(MissionDetailView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  # ログインユーザーのプロフィール
        context.update({
            'form': MissionApprovalForm(**self.get_form_kwargs()),
            'profile' : profile,
        })
        return context
    

class MissionCreateView(LoginRequiredMixin, CreateView):
    model = Mission
    fields = ['title', 'content', 'participants_limit']

    def form_valid(self, form):
        form.instance.author = self.request.user
        profile = Profile.objects.get(user=self.request.user)  # 自分のプロフィール
        # mission = Mission.objects.get(pk=self.pk)
        profile.exp_total -= 1
        # profile.exp_total -= mission.cost_exp
        profile.mission_create_count += 1
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MissionCreateView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  
        context["profile"] = profile
        return context

            

class MissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mission
    fields = ['title', 'content', 'participants_limit']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        mission = self.get_object()
        if self.request.user == mission.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(MissionUpdateView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  
        context["profile"] = profile
        return context



class MissionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mission
    success_url = '/'

    def test_func(self):
        mission = self.get_object()
        if self.request.user == mission.author:
            return True
        return False

class MissionWaitingListView(ListView):
    model = Mission
    template_name = 'mission/mission_waiting.html'
    context_object_name = 'missions'
    # paginate_by = 9
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(MissionWaitingListView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  
        not_approval = Mission.objects.filter(approval=0) 
        context["profile"] = profile
        context['not_approval'] = not_approval
        return context

