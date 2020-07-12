from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Thanks
from user.models import Profile
from .forms import ThanksCreateForm 
from django.views.generic.edit import ModelFormMixin
from exp.forms import ThanksApprovalForm


class ThanksListView(ListView):
    model = Thanks
    template_name = 'thanks/thanks_list.html'
    context_object_name = 'thanks_list'
    ordering = ['-date_posted']
    
    def get_context_data(self, **kwargs):
        context = super(ThanksListView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile 
        return context


class ThanksDetailView(DetailView, ModelFormMixin):
    model = Thanks
    template_name = 'thanks/thanks_detail.html'
    fields = ()

    def get_context_data(self, **kwargs):
        context = super(ThanksDetailView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile 
        context.update({
            'form': ThanksApprovalForm(**self.get_form_kwargs()),
        })
        return context    

class ThanksCreateView(CreateView, ModelFormMixin):
    model = Thanks
    form_class = ThanksCreateForm
    template_name = 'thanks/thanks_form.html'

    def form_valid(self, form):
        form.instance.giver = self.request.user

        if self.request.method == 'POST':
            obj = Thanks()
            form = ThanksCreateForm(self.request.POST or None, instance=obj)
           
            thanks = form.save(commit=False)
            thanks.giver = self.request.user
            thanks.some_field = 'some_value'
            thanks.save()
            form.save_m2m()
            return redirect('thanks-detail', pk=thanks.pk)
        else:
            form = ThanksCreateForm()
        return render(self.request, 'thanks/thanks_form.html', {'form':form})


class ThanksUpdateView(UpdateView, ModelFormMixin):
    model = Thanks
    # fields = ['content', 'recipients']
    form_class = ThanksCreateForm
    template_name = 'thanks/thanks_form.html'


    def form_valid(self, form):
        form.instance.giver = self.request.user

        if self.request.method == 'POST':
            obj = Thanks()
            form = ThanksCreateForm(self.request.POST or None, instance=obj)
            
            thanks = form.save(commit=False)
            thanks.giver = self.request.user
            thanks.some_field = 'some_value'
            thanks.save()
            form.save_m2m()
            return redirect('thanks-detail', pk=thanks.pk)
        else:
            form = ThanksCreateForm(self.request.POST)
        return render(self.request, 'thanks/thanks_form.html', {'form':form})


class ThanksWaitingListView(ListView):
    model = Thanks
    template_name = 'thanks/thanks_waiting.html'
    context_object_name = 'thanks_list'
    # paginate_by = 9
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(ThanksWaitingListView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  
        context["profile"] = profile
        return context



    # def form_valid(self, form):
    #     form.instance.giver = self.request.user
    #     return super().form_valid(form)

    # def test_func(self):
    #     thanks = self.get_object()
    #     if self.request.user == thanks.giver:
    #         return True
    #     return False

# def ThanksCreate(request):
#     if request.method == 'POST':
#         obj = Thanks()
#         form = ThanksCreateForm(request.POST or None, instance=obj)
#         if form.is_valid():
#             thanks = form.save(commit=False)
#             thanks.giver = request.user
#             thanks.some_field = 'some_value'
#             thanks.save()
#             form.save_m2m()
#             return redirect('thanks-detail', pk=thanks.pk)
#     else:
#         form = ThanksCreateForm()
#     return render(request, 'thanks/thanks_form.html', {'form':form})



