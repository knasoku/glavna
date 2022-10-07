from django.db import models
from django.contrib.auth.models import User
from poll.models import *



class Upravitel(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	#Zgrada = models.ForeignKey(Zgrada, on_delete=models.CASCADE, blank= True, null= True)
	
	def __str__(self):
		return self.user.username

