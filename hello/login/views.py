from django.shortcuts import render,HttpResponse,redirect
from .models import Login
from .models import Fact
from .models import Daily
from .models import Feedback
from datetime import datetime
import os
# Create your views here.
def index(request):
	context={"variable":"Invalid Username or Password!"}
	fact=Fact()
	f1=fact.get_fact(request)
	f2=fact.get_fact(request)
	f3=fact.get_fact(request)
	facts={"v1":f1,"v2":f2,"v3":f3}
	if request.session.get('id')!=None:
		return render(request,'index.html',facts)
	
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
					
					return render(request,'index.html',facts)
				else:
					return render(request,'login.html',context)


			elif choice=='hr':
				is_superuser=True
				e=Login()
				l=e.user_authenticate(request,username1,password1,is_superuser)

				if l is True:
					c=e.user_login(request,username1)
					print(c)
					return render(request,'index.html',facts)
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
	facts={"v1":f1,"v2":f2,"v3":f3}
	return render(request,'index.html',facts)

def milestones(request):
	return render(request,'milestones.html')

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

	



	r1={"v1":reports,"v2":re,"v3":s,"v4":fee,"v5":fdh}
	return render(request,'workbench.html',r1)
def feedback(request):
	if request.method=='POST':
		f=request.POST['f0']
		n=request.POST['sr0']
		d=Daily.objects.get(id=n)
		print(d.User)
		c=request.session['id']
		l=Login.objects.get(id=c)
		notification=l.first_name+" "+l.last_name+" sent you feedback on "+d.title+" "+str(d.datetime)
		f0=Feedback.objects.get(Daily=d,user=l)
		f0.delete()
		f1=Feedback.objects.create(feedback=f,Daily=d,user=l,notification=notification,datetime=datetime.now())
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
	context={"v0":img,"v1":full_name,"v2":department,"v3":designation,"v4":email_id}
	return render(request,'profile.html',context)
def logout(request):
	e=Login()
	out=e.user_logout(request)
	print(out)
	return redirect('login')