from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def index(request):
	return render(request,"index.html")

@login_required
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

@login_required
def guest_manage(request):
	username = request.session.get('user','')
	guest_list = Guest.objects.all()
	paginator = Paginator(guest_list,5)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	return render(request,"guest_manage.html",{"user":username,"guests":contacts})

@login_required
def sign_index(request,event_id):
	print(event_id)
	event = get_object_or_404(Event,id=event_id)
	return render(request,'sign_index.html',{'event':event})

@login_required
def sign_index_action(request,event_id):
	print(event_id)
	event = get_object_or_404(Event,id=event_id)
	phone = request.POST.get('phone','')
	result = Guest.objects.filter(phone = phone)
	if not result:
		return render(request,'sign_index.html',{'event':event,'hint':'phone error.'})
	result = Guest.objects.filter(phone=phone,event_id=event_id)
	if not result:
		return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error.'})
	result = Guest.objects.get(phone=phone,event_id=event_id)
	if result.sign:
		return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.'})
	else:
		Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
		return render(request,'sign_index.html',{'event':event,'hint':'sign in success','guest':result})
