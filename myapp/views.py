from django.shortcuts import render,redirect
from .models import User,Doctor_Profile,Appointment
import requests
import random
# Create your views here.

def index(request):
	return render(request,'index.html')

def contact(request):
	return render(request,'contact.html') 

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'login.html',{"msg":msg}) 
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						usertype=request.POST['usertype'],
						gender=request.POST['gender'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_picture=request.FILES['profile_picture']  	 
					)
				msg="User Sign Up Successfully"
				return render(request,'login.html',{"msg":msg}) 
			else:
				msg="Password And Confirm Password Does Not Matched"
				return render(request,'signup.html',{"msg":msg}) 
	else: 
		return render(request,'signup.html')


def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=='patient':
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_picture']=user.profile_picture.url
					return render(request,'index.html')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['mobile']=user.mobile
					request.session['profile_picture']=user.profile_picture.url
					return render(request,'doctor-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{"msg":msg})
		except:
			msg="Email Not Registered"
			return render(request,'signup.html',{"msg":msg})
	else:
		return render(request,'login.html')

def blog_single(request):
	return render(request,'blog-single.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		return render(request,'login.html') 
	except:
		return render(request,'login.html') 
	
	
def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.gender=request.POST['gender']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		request.session['profile_picture']=user.profile_picture.url
		msg="Profile Updated Successfully"
		if user.usertype=="Patient":
			return render(request,'profile.html',{'msg':msg,'user':user})
		else:
			return render(request,'doctor-profile.html',{'msg':msg,'user':user})
	else:
		if user.usertype=="Patient":
			return render(request,'profile.html',{"user":user})
		else:
   			return render(request,'doctor-profile.html',{'user':user})

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['opassword']:
			if request.POST['npassword']==request.POST['cnpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg="New Password And Confirm New Password Does Not Matched"
				if user.usertype=="Patient":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'doctor-change-password.html',{'msg':msg})
		else:
			msg="Old Password Does Not Matched"
			if user.usertype=="Patient":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'doctor-change-password.html',{'msg':msg})
	else:
		if user.usertype=="Patient":
			return render(request,'change-password.html')
		else:
			return render(request,'doctor-change-password.html')

def forgot_password(request):
	if request.method=='POST':
		try:
			user=usertype.objects.get(mobile=request.POST['mobile'])
			otp=random.randint(1000,9999)
			mobile=request.POST['mobile']
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"l143mQgeBjRSyL6ncX9k0a7wKpWPChzMItfuJFEZx8HvTGUAYOZfcBkvo4du6VY3wQESIig1lspN7axj","variables_values":"str(otp)","route":"otp","numbers":mobile}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			return render(request,'otp.html',{'otp':otp,'mobile':mobile})
		except:
			msg="Mobile Not Registered"
			return render(request,'forgot-password.html','msg',msg)

	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp=int(request.POST['otp'])
	uotp=int(request.POST['uotp'])
	mobile=int(request.POST['mobile'])
	if otp==uotp:
		return render(request,'new-password.html',{'mobile':mobile})
	else:
		msg="Invalid OTP"
		return render(request,"otp.html",{'msg':msg,'mobile':mobile,'otp':otp})

def new_password(request):
	mobile=int(request.POST['mobile'])
	npassword=int(request.POST['npassword'])
	cnpassword=int(request.POST['cnpassword'])
	if npassword==cnpassword:
		user=usertype.objects.get(mobile=mobile)
		user.password==npassword
		user.save()
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password And Confirm New Password Does Not Matched"
		return render(request,'new-password .html',{'msg':msg,'mobile':mobile})

def doctor_detail(request):
	doctor_profile=Doctor_Profile()
	doctor=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		doctor_profile=Doctor_Profile.objects.create(
			doctor=doctor,
			qualification=request.POST['qualification'],
			specialization=request.POST['specialization'],
			experience_in_years=request.POST['experience_in_years'],
			clinic_address=request.POST['clinic_address'],
			time=request.POST['time'],
			)
		msg="Doctor Details Updated Successfully"
		return render(request,'doctor-detail.html',{'doctor_profile':doctor_profile,'msg':msg})
	else:
		try:
			doctor_profile=Doctor_Profile.objects.get(doctor=doctor)
		except:
			pass
		return render(request,'doctor-detail.html',{'doctor_profile':doctor_profile})

def doctors(request):
	doctors=Doctor_Profile.objects.all()
	return render(request,'doctors.html',{'doctors':doctors})

def details(request,pk):
	doctor_profile=Doctor_Profile.objects.get(pk=pk)
	return render(request,'details.html',{'doctor_profile':doctor_profile})

def book_appointment(request,pk):
	doctor_profile=Doctor_Profile.objects.get(pk=pk)
	patient=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		if request.POST['appointment_time']=="---Select Time Slot---":
			time_slots=Appointment.objects.filter(doctor_profile=doctor_profile,appointment_date=request.POST['appointment_date'],appointment_status="Pending")
			l=[]
			for i in time_slots:
				l.append(i.appointment_time)
			return render(request,'book-appointment.html',{'doctor_profile':doctor_profile,'patient':patient,'l':l,'appointment_date':request.POST['appointment_date']})
		else:
			Appointment.objects.create(
				patient=patient,
				doctor_profile=doctor_profile,
				appointment_date=request.POST['appointment_date'],
				appointment_time=request.POST['appointment_time']
				)
		msg="Appointment Booked Successfully"
		return render(request,'book-appointment.html',{'doctor_profile':doctor_profile,'patient':patient,'msg':msg})
	else:
		return render(request,'book-appointment.html',{'doctor_profile':doctor_profile,'patient':patient})

def patient_appointment(request):
	patient=User.objects.get(email=request.session['email'])
	appointments=Appointment.objects.filter(patient=patient)
	return render(request,'patient-appointmnet.html',{'appointments':appointments})

def doctor_appointment(request):
	doctor=User.objects.get(email=request.session['email'])
	doctor_profile=Doctor_Profile.objects.get(doctor=doctor)	
	appointments=Appointment.objects.filter(doctor_profile=doctor_profile)
	return render(request,'doctor-appointmnet.html',{'appointments':appointments})

def cancel_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	appointment.appointment_status="Cancled By Patient"
	appointment.save()
	return redirect("patient-appointment")

def cancel_appointment_1(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	appointment.appointment_status="Cancled By Doctor"
	appointment.save()
	return redirect("doctor-appointment")