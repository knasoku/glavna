from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from poll.models import *
from poll.forms import *
from poll.decorators import *



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def upravitel_home(request):
	current_upravitel = Upravitel.objects.get(user = request.user)
	zgrada = Zgrada.objects.filter(upravitel = current_upravitel)

	context = {
		'zgrada': zgrada
	}
	return render (request, 'upravitel/upravitel_home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def zgrada_home(request, zgrada_id):
	zgrada = Zgrada.objects.get(pk=zgrada_id)

	context = {
		'zgrada': zgrada
	}
	return render (request, 'upravitel/zgrada_home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def zgrada_update(request, zgrada_id):

	zgrada = Zgrada.objects.get(id=zgrada_id)
	form = UpdateZgradaForm(instance=zgrada)

	if request.method == 'POST':
		form = UpdateZgradaForm(request.POST, instance=zgrada)
		if form.is_valid():
			form.save()
			messages.info(request, 'Податоците се ажурирани')

	context={
		'form' : form
	}
	return render (request, 'upravitel/zgrada_update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def dodadi_stanar(request, zgrada_id):
	zgrada = Zgrada.objects.get(id=zgrada_id)
	form = AddStanarForm(instance=zgrada)

	if request.method == 'POST':
		x = request.POST.get('stanar')
		user_add = get_object_or_404(User, username = x)
		stanar_add = get_object_or_404(Stanar, user = user_add)
		zgrada.Stanar.add(stanar_add)

	context={
		'form' : form
	}
	return render (request, 'upravitel/dodadi_stanar.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def izbrisi_stanar(request, zgrada_id):
	zgrada = Zgrada.objects.get(id=zgrada_id)
	form = AddStanarForm(instance=zgrada)

	if request.method == 'POST':
		x = request.POST.get('stanar')
		user_add = get_object_or_404(User, username = x)
		stanar_add = get_object_or_404(Stanar, user = user_add)
		zgrada.Stanar.remove(stanar_add)

	context={
		'form' : form
	}
	return render (request, 'upravitel/izbrisi_stanar.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def announcement(request):
	current_user = request.user
	current_stanar = Stanar.objects.get(user = current_user)
	if request.method == 'POST':
		form = announcementForm(request.POST)
		x = form['temp_id'].value()
		if Zgrada.objects.filter(pk=x).exists():
			current_zgrada=Zgrada.objects.get(pk=x)
		else:
			return HttpResponse('Грешен број на зграда или зградата не постои')
		t1 = str(current_zgrada.upravitel)
		t2 = str(current_user)
		if form.is_valid() and t1 == t2:
			form.save()
			return redirect('home')
	else:
		form = announcementForm()
	
	context={
		'form' : form
	}
	return render (request, 'upravitel/announcement.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'upravitel'])
def create(request):
	current_user = request.user
	current_stanar = Stanar.objects.get(user = current_user)
	if request.method == 'POST':
		form = CreatePollForm(request.POST)
		x = form['temp_id'].value()
		if Zgrada.objects.filter(pk=x).exists():
			current_zgrada=Zgrada.objects.get(pk=x)
		else:
			return HttpResponse('Грешен број на зграда или зградата не постои')
		t1 = str(current_zgrada.upravitel)
		t2 = str(current_user)
		if form.is_valid() and t1 == t2:
			form.save()
			return redirect('home')
		else:
			return HttpResponse('Грешен број на зграда или зградата не постои')
	else:
		form = CreatePollForm()
	
	context={
		'form' : form
	}
	return render (request, 'upravitel/create.html', context)