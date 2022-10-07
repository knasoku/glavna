from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
import functools

from django.contrib.auth import authenticate, login, logout
from .models import *


def unathenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None

			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Не ви е дозволено да ја гледате оваа страна')
		return wrapper_func
	return decorator

def poll_allowed(view_func):
	@functools.wraps(view_func)
	def wrapper_func(request, poll_id, *args, **kwargs):

		allowed_poll = Poll.objects.filter(pk=poll_id)
		allowed_stanar = Stanar.objects.filter(user = request.user)
		allowed_zgradas = Zgrada.objects.filter(Stanar__in = allowed_stanar)
		y=0
		checkZgrada = allowed_poll[0].Zgrada
		for i in allowed_zgradas.all():
			if i.adresa == checkZgrada.adresa:
				y=1
		if y==1:
			return view_func(request, poll_id, *args, **kwargs)
		else:
			return HttpResponse('Не ви е дозволено да ја гледате оваа страна')

	return wrapper_func
