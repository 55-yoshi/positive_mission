from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Mission
from user.models import Profile
from . import models
from django.shortcuts import render


class MissionListView(ListView):
    model = Mission
    template_name = 'mission/home.html'
    context_object_name = 'missions'
    paginate_by = 8
    ordering = ['-date_posted']


class MissionDetailView(DetailView):
    model = Mission
    template_name = 'mission/mission_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(MissionDetailView, self).get_context_data(**kwargs)
        participant = Profile.objects.get(user=self.request.user)  # ボタンを押す人のプロフィール
        context["participant"] = participant
        return context


class MissionCreateView(LoginRequiredMixin, CreateView):
    model = Mission
    fields = ['title', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        profile = Profile.objects.get(user=self.request.user)  # 自分のプロフィール
        # mission = Mission.objects.get(pk=self.pk)
        profile.exp_total -= 3
        # profile.exp_total -= mission.cost_exp
        profile.create_count += 1
        profile.save()
        return super().form_valid(form)

            

class MissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mission
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        mission = self.get_object()
        if self.request.user == mission.author:
            return True
        return False


class MissionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mission
    success_url = '/'

    def test_func(self):
        mission = self.get_object()
        if self.request.user == mission.author:
            return True
        return False