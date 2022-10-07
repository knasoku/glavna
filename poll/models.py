from django.db import models
from django.contrib.auth.models import User
from upravitel.models import Upravitel




class Stanar(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return self.name


class Zgrada(models.Model):
	citys = (
			('Битола', 'Битола'),
			('Прилеп', 'Прилеп'),
		)

	adresa = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=100, null=True, choices=citys) 
	brojStanovi = models.PositiveIntegerField()
	rezerven_fond=models.IntegerField(default=0, blank=True, null=True)
	Stanar = models.ManyToManyField(Stanar)
	last_updated = models.DateTimeField(auto_now=True, null=True)
	upravitel = models.ForeignKey(Upravitel, on_delete=models.CASCADE, blank= True, null= True)
	
	def __str__(self):
		return self.adresa

class Poll(models.Model):
	question = models.TextField()
	option_one = models.CharField(max_length=30)
	option_two = models.CharField(max_length=30)
	option_one_count = models.IntegerField(default=0)
	option_two_count = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	Zgrada = models.ForeignKey(Zgrada, on_delete=models.CASCADE, blank= True, null= True)


	def total(self):
		return self.option_one_count + self.option_two_count

	def __str__(self):
		return self.question

class CastVote(models.Model):
	pollVoted = models.IntegerField(default=0, blank=True, null=True)
	userVoted = models.CharField(max_length=200, null=True)
	userImePrezime = models.CharField(max_length=200, null=True)
	option= models.CharField(max_length=30, null=True)


class Announcement(models.Model):
	announcementHedline = models.CharField(max_length=100, null=True)
	announcementText = models.TextField()
	announcementDate = models.DateTimeField(auto_now_add = True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	Zgrada = models.ForeignKey(Zgrada, on_delete=models.CASCADE, blank= True, null= True)

	def __str__(self):
		return self.announcementHedline


