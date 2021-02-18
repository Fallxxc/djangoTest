from django.shortcuts import render
from django.urls import reverse_lazy
from .models import UserFollow
from Tickets.models import Ticket
from .form import TicketModelForm, ReviewModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def ticket_review_create_and_list_view(request):
    qs = Ticket.objects.all()
    userfollow = UserFollow.objects.get(user=request.user)
    t_form = TicketModelForm()
    r_form = ReviewModelForm()
    ticket_added = False
    # userfollow = UserFollow.objects.get(user=request.user)

    if 'submit_t_form' in request.POST:
        # print(request.POST)
        t_form = TicketModelForm(request.POST, request.FILES)
        if t_form.is_valid():
            instance = t_form.save(commit=False)
            instance.author = userfollow
            instance.save()
            t_form = TicketModelForm()
            ticket_added = True

    if 'submit_r_form' in request.POST:
        r_form = ReviewModelForm(request.POST)
        if r_form.is_valid():
            instance = r_form.save(commit=False)
            instance.user = userfollow
            instance.ticket = Ticket.objects.get(id=request.POST.get('ticket_id'))
            instance.save()
            r_form = ReviewModelForm()

    context = {
        'qs': qs,
        'userfollow': userfollow,
        't_form': t_form,
        'r_form': r_form,
        'ticket_added': ticket_added,
    }
    return render(request, 'Tickets/main.html', context)
 
class TicketDeleteView(LoginRequiredMixin, DeleteView): 
    model = Ticket
    template_name = 'Tickets/confirm_del.html'
    success_url = '/Tickets/'
    
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Ticket.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TicketModelForm
    model = Ticket
    template_name = 'Tickets/update.html'
    success_url = '/Tickets/'


    def form_valid(self, form):
        profile = UserFollow.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)