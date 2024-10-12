from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('blog-single/',views.blog_single,name='blog-single'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('new-password/',views.new_password,name='new-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('doctor-detail/',views.doctor_detail,name='doctor-detail'),
    path('doctors/',views.doctors,name='doctors'),
    path('details/<int:pk>/',views.details,name='details'),
    path('book-appointment/<int:pk>/',views.book_appointment,name='book-appointment'),
    path('patient-appointment/',views.patient_appointment,name='patient-appointment'),
    path('doctor-appointment/',views.doctor_appointment,name='doctor-appointment'),
    path('cancel-appointment/<int:pk>/',views.cancel_appointment,name='cancel-appointment'),
    path('cancel-appointment-1/<int:pk>/',views.cancel_appointment_1,name='cancel-appointment-1'),
]   