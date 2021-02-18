from django.shortcuts import render, redirect, get_object_or_404
from .models import UserFollow, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


@login_required
def my_profile_view(request):
    profile = UserFollow.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'UserFollows/myprofil.html', context)

@login_required
def invites_received_view(request):
    profile = UserFollow.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'UserFollows/my_invites.html', context)

@login_required
def accept_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = UserFollow.objects.get(pk=pk)
        receiver = UserFollow.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('UserFollows:my-invites-view')

@login_required
def reject_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = UserFollow.objects.get(user=request.user)
        sender = UserFollow.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('UserFollows:my-invites-view')

@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = UserFollow.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'UserFollows/to_invite_list.html', context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = UserFollow.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'UserFollows/profile_list.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserFollow
    template_name = 'UserFollows/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = UserFollow.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = UserFollow.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['Tickets'] = self.get_object().get_all_authors_Ticket()
        context['len_posts'] = True if len(self.get_object().get_all_authors_Ticket()) > 0 else False
        return context

class ProfileListView(LoginRequiredMixin, ListView):

    model = UserFollow
    template_name = 'UserFollows/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = UserFollow.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = UserFollow.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

# @login_required
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = UserFollow.objects.get(user=user)
        receiver = UserFollow.objects.get(pk=pk)
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('profiles:my-profile-view')
    return redirect('UserFollows:my-profile-view')
    
# @login_required
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = UserFollow.objects.get(user=user)
        receiver = UserFollow.objects.get(pk=pk)
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('profiles:my-profile-view')

    return redirect('UserFollows:my-profile-view')

    
    