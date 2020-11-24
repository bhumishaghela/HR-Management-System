from django.shortcuts import render,HttpResponse,redirect
from .models import Login
from .models import Fact
from .models import Daily
from .models import Feedback
from .models import Notification
from .models import Achievement
from datetime import datetime


import os
# Create your views here.


# Create your views here.
from .models import Teach


def View(request):
    if request.method == 'POST':
        title1=request.POST.get("title")
        message1=request.POST.get("description")
        timer=request.POST.get('timer')


        e=Teach(Title=title1,description=message1,time=timer)
        e.save()
        print(title1,message1,timer)

    return render(request, 'entry.html')




def EntryShow(request):
    all= Teach.objects.all()
    return render(request,"entryshow.html",{'bell':all})

def index(request):
	context={"variable":"Invalid Username or Password!"}
	fact=Fact()
	f1=fact.get_fact(request)
	f2=fact.get_fact(request)
	f3=fact.get_fact(request)
	a=Achievement.objects.all()

	
	l=Login.objects.filter(is_new=True)
	i=0
	profile={}
	l1=l.values()

	for i in range(0,len(l1)):
		l2=l1[i]
		profile[i+1]={"img":l2['image'],"name":l2['first_name']+" "+l2['last_name'],"department":l2['department'],"designation":l2['designation']}
	
	data={"v1":f1,"v2":f2,"v3":f3,"v4":profile,"v6":a}
	if request.session.get('id')!=None:
		return render(request,'index.html',data)
	
	if request.method=='POST':
		username1=request.POST['username']
		password1=request.POST['pass']
		choice=request.POST['accounttype']
		
		is_superuser=False
		print(choice)
		try:
			if choice=='employee':
				e=Login()
				l=e.user_authenticate(request,username1,password1,is_superuser)
				print(l)
				if l is True:
					a=e.user_login(request,username1)
					
					return render(request,'index.html',data)
				else:
					return render(request,'login.html',context)


			elif choice=='hr':
				is_superuser=True
				e=Login()
				l=e.user_authenticate(request,username1,password1,is_superuser)

				if l is True:
					c=e.user_login(request,username1)
					print(c)
					return render(request,'index.html',data)
				else:
					return render(request,'login.html',context)
			else:
				return render(request,'login.html',context)
		    
		except:
			
			return render(request,'login.html',context)

		
		
	else:
		return render(request,'login.html')
def reset(request):
	context={"variable":"Password Didnot Match!"}
	if request.method=='POST':
		username1=request.POST['username']
		password1=request.POST['pass']
		confirm=request.POST['confpass']
		if password1==confirm:
			login=Login.objects.get(user_name=username1)
			login.password=confirm
			login.save()
			c=request.session.get('id')
			if c!=None:
				return redirect('profile')
			else:
				return redirect('/')
		else:
			return render(request,'reset_password.html',context)

	else:
		return render(request,'reset_password.html')
		

def home(request):
	context={"variable":"this is sent"}
	fact=Fact()
	
	f1=fact.get_fact(request)
			
	f2=fact.get_fact(request)
	
	f3=fact.get_fact(request)
	n=Notification()
	notifications=n.get_notification(request)
	notify={}
	i=0
	for n1 in notifications.values():
		if n1['user_id']==request.session['id']:
			i=i+1
			notify[i]=n1['notification']
		
	l=Login.objects.filter(is_new=True)
	i=0
	profile={}
	l1=l.values()

	for i in range(0,len(l1)):
		l2=l1[i]
		profile[i+1]={"img":l2['image'],"name":l2['first_name']+" "+l2['last_name'],"department":l2['department'],"designation":l2['designation']}
	
	all= Teach.objects.all()
	data={"v1":f1,"v2":f2,"v3":f3,"v4":profile,"v5":notify}
	print(data)
	return render(request,'index.html',data)

def milestones(request):
	n=Notification()
	notifications=n.get_notification(request)
	notify={}
	i=0
	for n1 in notifications.values():
		if n1['user_id']==request.session['id']:
			i=i+1
			notify[i]=n1['notification']
	data={"v5":notify}
	return render(request,'milestones.html',data)

def workbench(request):
	d=Daily()
	r={}
	uk=""
	rr={}
	re={}
	s=set()
	count=0
	fee={}
	fdh={}
	n=Notification()
	notifications=n.get_notification(request)
	notify={}
	i=0
	for n1 in notifications.values():
		if n1['user_id']==request.session['id']:
			i=i+1
			notify[i]=n1['notification']
	reports=d.get_dailyreport(request)#get dailyreports
	for key,value in reports.items():
		r=reports[key]
		f=Feedback()
		f1=f.get_feedback(request,r['id'])
		if f1!=None:
			fee[r['id']]=f1
	
	try:
		c=request.session['id']
		l=Login.objects.get(id=c,department_head=True)
		d=l.department
		l1=Login.objects.filter(department=d)
		l2=l1.values()
		for i in range(0,len(l2)):
			l3=l2[i]
			if l3['department_head']==False:
				e=Daily.objects.filter(User=l3['id'])
				for e1 in e:
					u=e1.id
					f=Feedback()
					f1=f.get_feedback(request,u)
					if f1!=None:
						for key,value in f1.items():
							
							if f1['sender']==l:
								fdh=f1

					report={"datetime":e1.datetime,"title":e1.title,"dailyreport":e1.dailyreport,"uploadfile":e1.uploadfile,"workhours":e1.workhours,"id":e1.id,"user":e1.User}
					count=count+1
					rr[count]=report
					s.add(str(e1.User))

	except:
		print("You are not Department head")
	
	
	for key,value in reports.items():
		r=reports[key]
		df=r['uploadfile']
		filename = df.file.name.split('/')[-1]
		if request.GET.get('myfile') == str(filename):
			
			response = HttpResponse(df.file, content_type='.docx')
			response['Content-Disposition'] = 'attachment; filename=%s' % filename
			return response


	for key,value in rr.items():
		r=rr[key]
		for key,value in r.items():
			df=r['uploadfile']
			filename = df.file.name.split('/')[-1]
			if request.GET.get('myfile') == str(filename):
				response = HttpResponse(df.file, content_type='.docx')
				response['Content-Disposition'] = 'attachment; filename=%s' % filename
				return response


		#create dailyreports	
	if request.method=='POST':
		title=request.POST['title0']
		report=request.POST['report0']
		
		workhour=request.POST['workhour0']

		d=Daily()
		myfile = request.FILES['myfile'] 
		print(myfile)
		c=d.create_dailyreport(request,title,report,myfile,workhour)
		
		return redirect('workbench')
	for i in range(0,len(reports)+1):
		#edit daily reports	
		if request.GET.get(str(i)) == 'Edit':
		
			for report in reports:
				if report==i:
					r1=reports[report]
					re={"v1":r1,"v2":i}
					return render(request,'edit.html',re)



		elif request.GET.get(str(i)) == 'Delete':
			#delete daily reports
			for report in reports:
				if report==i:
					r1=reports[report]
					title=r1['title']
					dailyreport=r1['dailyreport']
					workhour=r1['workhours']
					dt=r1['datetime']
					upload=r1['uploadfile']
					user=r1['user']
					d1=Daily.objects.get(title=title,dailyreport=dailyreport,uploadfile=upload,User=user,workhours=workhour,datetime=dt)
					d1.delete()
					return redirect('workbench')


	#f=d.get_dailyreport(request)
	for s1 in s:
		if request.GET.get('employee')==s1:
			count=0
			for key,value in rr.items():
				fr=rr[key]
				for key,value in fr.items():
					if str(fr['user'])==s1:
						r4={"datetime":fr['datetime'],"title":fr['title'],"dailyreport":fr['dailyreport'],"uploadfile":fr['uploadfile'],"workhours":fr['workhours'],"id":fr['id'],"user":fr['user']}
						count=count+1
						re[count]=r4
						break

	

	c=request.session['id']
	print(c)
	all= Teach.objects.filter(User=c)
	print(all)
	r1={"v1":reports,"v2":re,"v3":s,"v4":fee,"v5":fdh,"bell":all}
	
	return render(request,'workbench.html',r1)
def feedback(request):
	if request.method=='POST':
		f=request.POST['f0']
		n=request.POST['sr0']
		d=Daily.objects.get(id=n)
		print(d.User)
		l1=Login.objects.get(first_name=d.User)
		c=request.session['id']
		l=Login.objects.get(id=c)
		notification=l.first_name+" "+l.last_name+" sent you feedback on "+d.title+" "+str(d.datetime)
		f0=Feedback.objects.filter(Daily=d,user=l)
		f0.delete()
		f1=Feedback.objects.create(feedback=f,Daily=d,user=l,notification=notification,datetime=datetime.now())
		print(l)
		print(l1.id)
		n=Notification.objects.create(notification=notification,user_id=l1.id,seen=False)
		n.save()
		f1.save()
		
		try:

			df=d.uploadfile
			filename = df.file.name.split('/')[-1]
			if request.POST['myfile'] == str(filename):
				response = HttpResponse(df.file, content_type='.docx')
				response['Content-Disposition'] = 'attachment; filename=%s' % filename
				return response
		except:
			print("File not clicked to download")	


		
		

	return redirect('workbench')

def edit(request):
	if request.method=='POST':
		n=request.POST['sr0']
		n=int(n)
		title=request.POST['t0']
		report=request.POST['r0']
		uploadfile=request.FILES['myfile']
		workhour=request.POST['w0']
		c=request.session['id']
		l=Login.objects.get(id=c)
		d=Daily()
		dr=d.get_dailyreport(request)
		for key,value in dr.items():
			if key==n:
				t=dr[key]
				dt=t['id']
				re=Daily.objects.get(id=dt)
				re.title=title
				re.dailyreport=report
				re.datetime=datetime.now()
				re.uploadfile=uploadfile
				re.workhours=workhour
				re.save()
				return redirect('workbench')
	
def delete(request):
	return  HttpResponse('This is Delete Page')
def profile(request):
	c=request.session.get('id')
	l=Login.objects.get(id=c)
	full_name=l.first_name+" "+l.last_name
	department=l.department
	designation=l.designation
	email_id=l.user_name
	img=l.image
	n=Notification()
	notifications=n.get_notification(request)
	notify={}
	i=0
	for n1 in notifications.values():
		if n1['user_id']==request.session['id']:
			i=i+1
			notify[i]=n1['notification']
	context={"v0":img,"v1":full_name,"v2":department,"v3":designation,"v4":email_id,"v5":notify}
	return render(request,'profile.html',context)
def logout(request):
	e=Login()
	out=e.user_logout(request)
	print(out)
	return redirect('login')

