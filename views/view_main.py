
from django.views.generic import TemplateView
from datetime import date, datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect

# class MainView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    
#     def test_func(self):
#         user = self.request.user
#         return user.is_superuser or user.groups.filter(name='g_front')

class MainView(TemplateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='g_front')