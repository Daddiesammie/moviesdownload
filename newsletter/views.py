from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView
from .models import Subscriber
from .forms import SubscriptionForm

class SubscribeView(CreateView):
    model = Subscriber
    form_class = SubscriptionForm
    template_name = 'newsletter/subscribe.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, 'Successfully subscribed to newsletter!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'This email is already subscribed.')
        return redirect('home')
