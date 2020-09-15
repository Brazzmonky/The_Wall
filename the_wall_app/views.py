from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt


def home(request):
	return render(request, 'home.html')


def newUser(request):
	errors = User.objects.register_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		password=request.POST['password']
		pw_hash= bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		newUser=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash.decode())
		context={
		"users": User.objects.all()	
		}
		messages.success(request, "Congradulations, welcome to The Wall!")
		request.session['loggedinUserID'] = newUser.id
		return redirect('/Success')


def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		loggedinUser = User.objects.get(email=request.POST['email'])
		request.session['loggedinUserID'] = loggedinUser.id
		messages.success(request, "Welcome back to The Wall!")
		print(loggedinUser.first_name)	
		return redirect('/Success')

def logout(request):
	request.session.clear()
	return redirect('/')

def Success(request):
	all_messages= Messages.objects.all()
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])
	context={
	"all_comments": Comment.objects.all().order_by("created_at"),
	"all_messages": Messages.objects.all().order_by("-created_at"),
	"all_users": User.objects.all(),
	"loggedinUser": User.objects.get(id=request.session['loggedinUserID']),
	}
	return render(request, 'the_wall.html', context)

def makeapost(request):
	context={
	"all_users": User.objects.all(),
	"loggedinUser": User.objects.get(id=request.session['loggedinUserID'])
	}
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])
	newpost=Messages.objects.create(Message=request.POST['Message'],user=loggedinUser)
	return redirect('/Success')

def makeacomment(request,messageid):
	context={
	"all_users": User.objects.all(),
	"loggedinUser": User.objects.get(id=request.session['loggedinUserID']),
	"all_Comments": Comment.objects.all()
	}
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])
	message=Messages.objects.get(id=messageid)
	newcomment=Comment.objects.create(comment=request.POST['comment'], message=message, user=loggedinUser)	
	return redirect('/Success')

def deletepost(request,messageid):
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])	
	post_to_delete=Messages.objects.get(id=messageid)
	post_to_delete.delete()
	return redirect('/Success')

def deletecomment(request,commentid):
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])
	comment_to_delete=Comment.objects.get(id=commentid)
	comment_to_delete.delete()
	return redirect('/Success')