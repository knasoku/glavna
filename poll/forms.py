from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Poll, Stanar, Zgrada, Announcement

class CreatePollForm(ModelForm):
	temp_id = forms.IntegerField()
	class Meta:
		model = Poll
		fields= ['question', 'option_one', 'option_two', 'temp_id']

	def save(self, commit = True):
		m = super(CreatePollForm, self).save(commit=False)
		m.question = self.cleaned_data['question']
		m.option_one = self.cleaned_data['option_one']
		m.option_two = self.cleaned_data['option_two']
		m.Zgrada = Zgrada.objects.get(pk=self.cleaned_data['temp_id'])
		if commit:
 			m.save()
		return m

class announcementForm(ModelForm):
	temp_id = forms.IntegerField()
	class Meta:
		model = Announcement
		fields= ['announcementHedline', 'announcementText', 'temp_id' ]

	def save(self, commit = True):
		m = super(announcementForm, self).save(commit=False)
		m.announcementHedline = self.cleaned_data['announcementHedline']
		m.announcementText = self.cleaned_data['announcementText']
		m.Zgrada = Zgrada.objects.get(pk=self.cleaned_data['temp_id'])
		if commit:
 			m.save()
		return m


class  CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name', 'last_name' ,'email', 'password1', 'password2']

class StanarForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = [ 'email', 'password1', 'password2']

class UpdateStanarForm(ModelForm):
	class Meta:
		model = Stanar
		fields = [ 'name', 'email', 'phone']

class UpdateZgradaForm(ModelForm):
	class Meta:
		model = Zgrada
		fields= ['adresa', 'brojStanovi', 'rezerven_fond']



class AddStanarForm(ModelForm):
	
	stanar = forms.CharField(label="StanarUname", max_length=200, widget=forms.TextInput())
	
	class Meta:
		model = Zgrada
		fields= ['adresa', 'stanar']

