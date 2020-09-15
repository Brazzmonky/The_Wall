from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
	def register_validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors= {}
		validemail=User.objects.filter(email=postData['email'])
		if len(validemail) > 0:
			errors['email']="Email already in use. Please log in or choose another"
		if not EMAIL_REGEX.match(postData['email']):           
			errors['email'] = "Invalid email address!"	
		if len(postData ['first_name']) < 2:
			errors['first_name'] = "Required field, please input a first name of at least 2 letters"
		if len(postData ['last_name']) < 2:
			errors['last_name']= "Required field, please input a last name of at least 2 letter"
		if len(postData ['password']) < 8:
			errors['password']= "Required field, please input a password of at least 8 characters"
		if postData['password']	!= postData['confirmpw']:
			errors['confirmpw']= "Passwords must match"
		return errors


	def login_validator(self,postData):
		useremail=User.objects.filter(email=postData['email'])
		errors= {}
		if len(postData['email']) == 0:
			errors['emaillen']= "Required field please enter a valid email."
		if len(useremail) < 1:
			errors['email']="No Email matching that address, please register or try another Email."
		else:
			print(useremail)
			user=User.objects.get(email=postData['email'])	
			if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				print("password match")
			else:
				errors['passwordfailed']= "Incorrect password, please try again."
				print("failed password")
		return errors	


class User(models.Model):
	first_name=models.CharField(max_length=255)
	last_name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __repr__(self):
		return f"class_name: {self.first_name} {self.last_name} ({self.created_at}) ({self.updated_at})"
	
class Messages(models.Model):
	Message=models.TextField()
	user = models.ForeignKey(User, related_name="message", on_delete=models.CASCADE, default=None, null=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	def __repr__(self):
		return f"Messages:{self.Message} {self.user} {self.id}"

class Comment(models.Model):
	comment=models.TextField()
	message= models.ForeignKey(Messages, related_name="comments", on_delete=models.CASCADE, default=None, null=True)
	user = models.ForeignKey(User, related_name="comment", on_delete=models.CASCADE, default=None, null=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	def __repr__(self):
		return f"class_name: {self.id} ({self.created_at}) ({self.updated_at})"