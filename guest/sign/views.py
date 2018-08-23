from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
# Create your views here.
def index(request):
	return render(request,"index.html")

def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user) #登录
			response = HttpResponseRedirect('/event_manage/')
			# response.set_cookie('user',username,3600) # 添加浏览器 cookie
			request.session['user'] = username
			return response
		else:
			return render(request,'index.html',{'error':'username or password error!'})

@login_required
def event_manage(request):
	# username = request.COOKIES.get('user','') # 读取cookie
	event_list = Event.objects.all()
	username = request.session.get('user','')
	return render(request,"event_manage.html",{"user":username,"events":event_list})

@login_required
def search_name(request):
	username = request.session.get('user','')
	if request.method == "GET":
		event_name = request.GET.get("name", "")
		print(event_name)
		event_list = Event.objects.filter(name__contains=event_name)
		print(event_list)
		return render(request, "event_manage.html", {"user":username,"events":event_list})
	else:
		return render(request, "index.html")
	# search_name = request.GET.get("name","") 
	# print(search_name)
	# event_list = Event.objects.filter(name__contains=search_name)
	# print(event_list)
	# return render(request,"event_manage.html",{"user":username,"events":event_list})

def guest_manage(request):
	username = request.session.get('user','')
	guest_list = Guest.objects.all()
	return render(request,"guest_manage.html",{"user":username,"guests":guest_list})