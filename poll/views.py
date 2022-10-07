from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

from .forms import *
from .models import *
from .decorators import *
from upravitel.models import *


@login_required(login_url='login')
def announcementView(request, announcement_id):
	announcement = Announcement.objects.get(pk=announcement_id)
	context = {
		'announcement' : announcement
	}
	return render (request, 'poll/announcement_view.html', context)


@login_required(login_url='login')
def home(request):
	current_stanar = Stanar.objects.filter(user = request.user)
	current_zgradas = Zgrada.objects.filter(Stanar__in = current_stanar)
	polls = Poll.objects.filter(Zgrada__in = current_zgradas).order_by('-id')[:5]
	announcements = Announcement.objects.filter(Zgrada__in = current_zgradas).order_by('-id')[:5]

	context = {
		'polls': polls,
		'current_zgradas': current_zgradas,
		'announcements': announcements

	}
	return render (request, 'poll/home.html', context)

@poll_allowed
@login_required(login_url='login')
def result(request, poll_id):
	poll = Poll.objects.get (pk=poll_id)
	glasalList = CastVote.objects.filter(pollVoted=poll_id)
	context = {
		'glasalList' : glasalList,
		'poll' : poll
	}
	return render (request, 'poll/results.html', context)


@poll_allowed
@login_required(login_url='login')
def vote(request, poll_id):
	poll = Poll.objects.get (pk=poll_id)
	current_user = request.user
	current_user_fullname = request.user.get_full_name()
	glasal = CastVote()
	glasal.pollVoted = poll.id
	glasal.userVoted = request.user
	glasal.userImePrezime = current_user_fullname
	y = CastVote.objects.filter(userVoted__exact = glasal.userVoted, pollVoted__exact = glasal.pollVoted).count() 
	if y == 0: # y e test dali current user veke glasal
		if request.method == 'POST':
			selected_option = request.POST['poll']
			if selected_option == 'option1':
				poll.option_one_count += 1
				glasal.option = poll.option_one
				poll.save()
				glasal.save()
			elif selected_option == 'option2':
				glasal.option = poll.option_two
				poll.option_two_count += 1
				poll.save()
				glasal.save()
			else:
				return HttpResponse (400, 'Invalid Form')
			return redirect('result', poll_id)
	else:	
		messages.info(request, ' Веќе сте гласале на оваа анкета!')

	context = {
	'poll' : poll
	}
	return render (request, 'poll/vote.html', context)

@unathenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user= form.save()
			Stanar.objects.create( user=user, name= user.first_name+" "+user.last_name, email=user.email)
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='stanar')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)
			return redirect ('login')

	context = {'form':form}
	return render(request, 'poll/register.html', context)

@unathenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate (request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Погрешно корисничко име или лозинка')

	context = {}

	return render(request, 'poll/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def userPage(request):
	context = {}
	return render(request, 'poll/user.html', context)

@login_required(login_url='login')
def accountSettings(request):
	stanar = Stanar.objects.get(user = request.user)
	form = UpdateStanarForm(instance=stanar)
	if request.method == 'POST':
		form = UpdateStanarForm(request.POST, instance=stanar)
		if form.is_valid():
			form.save() 
			messages.success(request, 'Податоците се ажурирани')
			return redirect ('account')		
		
	context={
		'form': form 
	}
	return render (request, 'poll/account_settings.html', context)


@login_required(login_url='login')
def pollPage(request):
	current_stanar = Stanar.objects.filter(user = request.user)
	current_zgradas = Zgrada.objects.filter(Stanar__in = current_stanar)
	polls = Poll.objects.filter(Zgrada__in = current_zgradas).all().order_by('-id')
	p = Paginator(polls, 10)
	page = request.GET.get('page')
	poll_list = p.get_page(page)
	context = {
		'poll_list' : poll_list
	}
	return render (request, 'poll/poll_page.html', context)


@login_required(login_url='login')
def announcementPage(request):
	current_stanar = Stanar.objects.filter(user = request.user)
	current_zgradas = Zgrada.objects.filter(Stanar__in = current_stanar)
	announcements = Announcement.objects.filter(Zgrada__in = current_zgradas).all().order_by('-id')
	p = Paginator(announcements, 10)
	page = request.GET.get('page')
	announcement_list = p.get_page(page)
	context = {
		'announcement_list' : announcement_list
	}
	return render (request, 'poll/announcement_page.html', context)

@login_required(login_url='login')
def passwordChanged(request):
	context = {

	}
	return render (request, 'poll/password_change_complete.html', context)


def contact(request):
	context = {
	}
	return render (request, 'poll/contact.html', context)
