from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('userprofile',views.userprofile,name="userprofile.html"),
    path('about',views.about,name="about"),
    path('faq',views.faq,name="faq"),
    path('guide/<str:name>/<int:id>/<int:price>',views.guide_book,name="guide-book"),
    path('guide-booked/<str:name>/<int:id>/<int:userid>',views.guide_booked,name="booked"),
    path('otp',views.otp_verify,name="otp-verification"),
    path('guide-single/<int:id>',views.single_guide,name="single-guide"),
    path('delete-guide/<int:id>',views.delete_guide,name="delete-guide"),
    path('tour',views.tour,name="tour"),
    path('tour-list/<int:cityid>',views.tour_list,name="tour-list"),
    path('tour-detail/<int:id>',views.tour_details,name="tour-detail"),
    path('tour-detail-guj/<int:id>',views.tour_detail_guj,name="tour-detail-guj"),
    path('tour-detail-hindi/<int:id>',views.tour_detail_hindi,name="tour-detail-hindi"),
    path('tour-detail/<int:id>/<int:logid>',views.tour_detail_log,name="tourdetail"),
    path('audio/<int:id>',views.listen_audio,name="listen audio"),
    path('audio-guj/<int:id>',views.listen_guj_audio,name="listen guj audio"),
    path('audio-hindi/<int:id>',views.listen_hindi_audio,name="listen hindi audio"),
    path('contact',views.contacts,name="contact"),
    path('register',views.registration,name="register"),
    path('fetchregister',views.fetchregister,name="fetchregister"),
    path('login',views.login,name="login"),
    path('fetchlogin',views.fetchlogin,name="fetchlogindata"),
    path('logout',views.logout,name="logout"),
    path('forgot',views.forgot,name="forgot"),
    path('forgot-password',views.forgotpassword,name="forgot-password")
]