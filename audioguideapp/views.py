import random2
import random
from django.core.exceptions import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user,monument,feedback,city,audio,contact,monument_photos,category,payment
from gmail import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# Create your views here.


def index(request):
    getmonument = monument.objects.all().order_by('id')[16:24]
    # getmonument = monument.objects.all()
    uid = request.session.get('logid',None)
    getguide = payment.objects.filter(user_name=uid)
    total_amount = 0
    for i in getguide:
        total_amount += i.charges
    getcity = city.objects.all()
    context = {
        "monuments" : getmonument,
        "cities" : getcity,
        "guide" : getguide,
        "total": total_amount
    }
    return render(request,'index.html',context)


def about(request):
    getdetails = monument.objects.all()
    context = {
        "places" : getdetails
    }
    return render(request,'about.html',context)

def faq(request):
    return render(request,'faq.html')

def guide_book(request,name,id,price):
    getdetail = monument.objects.get(id=id)
    context = {
        "monument" : getdetail,
        "name" : name,
        "price" : price
    }
    return render(request,'guide-book-form.html',context)

def guide_booked(request,name,id,userid):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        book_date = request.POST.get('book_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        card_name = request.POST.get('card-name')
        card_no = request.POST.get('card-no')
        ex_month = request.POST.get('ex-month')
        ex_year = request.POST.get('ex-year')
        cvv = request.POST.get('cvv')
        price = request.POST.get('total')
        total = int(price)


        otp = random2.randint(111111, 999999)
        print(otp)
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['book_date'] = book_date
        request.session['start_time'] = start_time
        request.session['end_time'] = end_time
        request.session['price'] = price
        request.session['name'] = name
        request.session['monument'] = id
        request.session.save()

        # CLIENT_SECRET_FILE = 'client_secret.json'
        # API_NAME = 'gmail'
        # API_VERSION = 'v1'
        # SCOPES = ['https://mail.google.com/']
        #
        # service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        #
        # emailMsg = "Thank you for choosing Traveler's Bible To Booking Guide, we have sent you a One-Time Password (OTP) to your registered email address Thank you for using our services, and we look forward to providing you with a seamless and enjoyable travel experience.\n Your One-Time Password (OTP) Is :- <b>"+str(otp)+"</b>"
        # mimeMessage = MIMEMultipart()
        # mimeMessage['to'] = email
        # mimeMessage['subject'] = 'Testing OTP'
        # mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        # raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        #
        # message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        # print(message)

        from django.core.mail import send_mail

        send_mail(
            'Your OTP',
            "Thank you for choosing Traveler's Bible,\n Your One-Time Password (OTP) Is :- <b>"+str(otp)+"</b>",
            'kaushalpanchal612@gmail.com',
            [email],
            fail_silently=False,
        )

        getdetail = monument.objects.get(id=id)
        context = {
                    "monument": getdetail,
                    "name": name
                }
    return render(request,'OTP-Verification.html',context)

def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        otp_generate = request.session.get('otp')
        print(otp_generate)

        if str(otp) == str(otp_generate):
            phone = request.session['phone']
            book_date = request.session['book_date']
            start_time = request.session['start_time']
            end_time = request.session['end_time']
            total = request.session['price']
            email = request.session['email']
            username = request.session['logid']
            client = request.session['logname']
            name = request.session['name']
            monumentname = request.session['monument']


            print(name)


            from django.core.mail import send_mail

            send_mail(
                'Your Guide is successfully Booked',
                "Dear "+str(client)+", We are thrilled to confirm your booking for a guided tour with us. "
                "Our team is excited to take you on a journey through "+str(monumentname)+" and share our knowledge and passion for this incredible place."
                "Your tour is scheduled for date is "+str(book_date)+" time is "+str(start_time)+" to "+str(end_time)+" and will last approximately 2 Hours. Please arrive at least 10 minutes before the start time to ensure a timely departure."
                "To make the most of your experience, we recommend wearing comfortable clothing and shoes, and bringing a water bottle, sunscreen, and a hat."
                "If you have any special requests or needs, please don't hesitate to let us know. Our team is dedicated to ensuring your comfort and satisfaction."
                "Thank you for choosing us as your guide. We can't wait to show you around."
                "Best regards,"
                "<b>Traveler's Bible</b>",
                'krushanuinfolabz@gmail.com',
                [email],
                fail_silently=False,
            )


            insertdata = payment(user_name=user(id=username), monument_name=monument(id=monumentname), guide_name=name, email=email,
                                 phone=phone, total=total, payment_type='debit card',charges=total, guide_date=book_date, start_time=start_time,
                                end_time=end_time)
            insertdata.save()

            # CLIENT_SECRET_FILE = 'client_secret.json'
            # API_NAME = 'gmail'
            # API_VERSION = 'v1'
            # SCOPES = ['https://mail.google.com/']
            #
            # service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            # email = request.session['email']
            # emailMsg = 'You have successfully completed guide booking <b>'+request.session['logname']+'</b>'
            # mimeMessage = MIMEMultipart()
            # mimeMessage['to'] = request.session['email']
            # mimeMessage['subject'] = 'Guide Booked Successfully'
            # mimeMessage.attach(MIMEText(emailMsg, 'html'))
            # raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            # message = service.users().messages().send(userId='me',body={'raw': raw_string}).execute()
            # print(message)

            del request.session['phone']
            del request.session['book_date']
            del request.session['start_time']
            del request.session['end_time']
            del request.session['price']
            del request.session['email']
            del request.session['otp']
            del request.session['name']
            del request.session['monument']
            return redirect(index)
        else:
            messages.error(request,'OTP Verification Failed,please enter right otp.')
    return render(request,'OTP-Verification.html')

def single_guide(request,id):
    getguide = payment.objects.get(id=id)
    context = {
        "guide" : getguide
    }
    return render(request,'guide-book-single.html',context)

def delete_guide(request,id):
    del_guide = payment.objects.get(id=id)
    del_guide.delete()

    return redirect(index)

def tour(request):
    monuments = monument.objects.all()
    getcity = city.objects.all()
    
    context = {
        "monuments":monuments,
        "getcity":getcity,
    }
    return render(request,'tour.html',context)

def listen_audio(request,id):
    getmonument = monument.objects.get(id=id)
    try:
        getaudio = audio.objects.get(monument_name=id)
    except ObjectDoesNotExist:
        return render(request,'audio.html')
    context = {
        "audio" : getaudio,
        "monument" : getmonument,
    }
    return render(request,'audio.html',context)

def listen_guj_audio(request,id):
    getmonument = monument.objects.get(id=id)
    getaudio = audio.objects.get(monument_name=id)
    context = {
        "audio": getaudio,
        "monument": getmonument,
    }
    return render(request,'audio_guj.html',context)

def listen_hindi_audio(request,id):
    getmonument = monument.objects.get(id=id)
    getaudio = audio.objects.get(monument_name=id)
    context = {
        "audio": getaudio,
        "monument": getmonument,
    }
    return render(request, 'audio_hindi.html', context)


def tour_list(request,cityid):
    getmonument = monument.objects.filter(city_name=cityid)
    getcities = city.objects.all().exclude(city_name=id)
    getcategory = category.objects.all()
    context = {
        "monuments" : getmonument,
        "cities": getcities,
        "categories": getcategory
    }
    return render(request,'tour-list.html',context)

def tour_details(request,id):
    getdetails = monument.objects.get(id=id)
    getfeedback = feedback.objects.filter(monument_name=id)
    getimages = monument_photos.objects.filter(monument=id)
    getmonuments = monument.objects.filter(city_name=getdetails.city_name).exclude(id=id)
    getcities = city.objects.all()

    context = {
        "monument" : getdetails,
        "feedbacks" : getfeedback,
        "images" : getimages,
        "places":getmonuments,
        "cities": getcities
    }
    return render(request,'tour-detail.html',context)

def tour_detail_guj(request,id):
    getdetails = monument.objects.get(id=id)
    getfeedback = feedback.objects.filter(monument_name=id)
    getimages = monument_photos.objects.filter(monument=id)
    getmonuments = monument.objects.filter(city_name=getdetails.city_name).exclude(id=id)
    getcities = city.objects.all()
    context = {
        "monument" : getdetails,
        "feedbacks" : getfeedback,
        "images": getimages,
        "places": getmonuments,
        "cities": getcities
    }
    return render(request,'tour-detail2.html',context)

def tour_detail_hindi(request,id):
    getdetails = monument.objects.get(id=id)
    getfeedback = feedback.objects.filter(monument_name=id)
    getimages = monument_photos.objects.filter(monument=id)
    getmonuments = monument.objects.filter(city_name=getdetails.city_name).exclude(id=id)
    getcities = city.objects.all()
    context = {
        "monument": getdetails,
        "feedbacks": getfeedback,
        "images": getimages,
        "places": getmonuments,
        "cities": getcities
    }
    return render(request, 'tour-detail3.html', context)

def tour_detail_log(request,id,logid):
    if request.method == 'POST':
        message = request.POST.get('message')

        try:
            checkdata = user.objects.get(id=logid)
            monumentdata = monument.objects.get(id=id)
        except:
            checkdata = None

        insert = feedback(user_name=checkdata, monument_name=monumentdata, comment=message, rating=5,photo=checkdata.propic)
        insert.save()
    getdetails = monument.objects.get(id=id)
    getfeedback = feedback.objects.filter(monument_name=id)
    getimages = monument_photos.objects.filter(monument=id)

    context = {
        "monument": getdetails,
        "feedbacks": getfeedback,
        "images": getimages
    }
    return render(request, 'tour-detail.html', context)

def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        insert_contact = contact(name=name,phone=phone,email=email,message=message)
        insert_contact.save()

        if contact:
            messages.success(request,'Your Message is Successfully sent to our community!')
        else:
            messages.error(request,'Something Went Wrong')
    return render(request,'contact.html')

def registration(request):
    return render(request,'Registration.html')

def fetchregister(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('uemail')
        mobile = request.POST.get('uphone')
        citys = request.POST.get('ucity')
        propic = request.FILES.get('propic')
        password = request.POST.get('upassword')

        try:
            checkdata = user.objects.get(email_id=email)
            if checkdata is not None:
                messages.error(request,'User already exists, please choose another email!')
        except:
            checkdata = None

        digitcount = 0
        capitalcount = 0
        specialcount = 0

        if checkdata is None:
            if len(password) >= 8:
                for i in range(0,len(password)):
                    if ord(password[i]) >= 48 and ord(password[i]) <= 57:
                        digitcount = digitcount + 1
                    if ord(password[i]) >= 65 and ord(password[i]) <= 90:
                        capitalcount = capitalcount + 1
                    if ord(password[i]) == 35 or ord(password[i]) == 64 or ord(password[i]) == 36:
                        specialcount = specialcount + 1

                if digitcount >= 1 and specialcount >= 1 and capitalcount >= 1:
                    password_check = True
                else:
                    messages.error(request, 'Please enter at least one digit,capital,small,special characters')
                    password_check = False
                if password_check is True:
                    if propic is not None:
                        insertdetails = user(name=username, email_id=email, mobile_no=mobile,citys=citys, propic=propic, password=password)
                        insertdetails.save()
                    else:
                        insertdetails = user(name=username, email_id=email, mobile_no=mobile, citys=citys, propic='media/photos/1.jpg',password=password)
                        insertdetails.save()
                        messages.success(request, "Sign Up is Successfully Completed, Now you can Sing In!")
                        return redirect(login)
            else:
                messages.error(request,'Password must be 8 characters long!')
        else:
            messages.error(request,'Something went wrong!')
    return render(request,'Registration.html')

def login(request):
    return render(request,'Login.html')

def fetchlogin(request):
    if request.method == 'POST':
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')

        try:
            checkdata = user.objects.get(email_id=email,password=password)
            request.session['logname'] = checkdata.name
            request.session['logid'] = checkdata.id
            request.session.save()
        except:
            checkdata = None

        if checkdata is not None:
            return redirect(index)
        else:
            messages.error(request,'User Not Found, Please Enter Right Email and Password!')

    return render(request,'login.html')

def logout(request):
    try:
        del request.session['logname']
    except:
        pass
    return render(request, 'login.html')

def forgot(request):
    return render(request,'reset_password.html')


# def userprofile(request):
#     logname = request.session.get('logname')
#     logid = request.session.get('logid')
#     email = request.session.get('email')
#     return render(request, 'userprofile.html', {'logname': logname, 'logid': logid, 'email':email})
def userprofile(request):
    # Retrieve user data from the session
    user_id = request.session.get('logid')
    if user_id:
        try:
            user_data = user.objects.get(id=user_id)
            context = {
                'propic': user_data.propic,
                'name': user_data.name,
                'email_id': user_data.email_id,
                'mobile_no': user_data.mobile_no,
                'citys':user_data.citys
            }
            return render(request, 'userprofile.html', context)
        except user.DoesNotExist:
            pass
    return render(request, 'userprofile.html', {})


def forgotpassword(request):
    if request.method == 'POST':
        usernamee = request.POST['email']
        print(usernamee)
        try:
            username = user.objects.get(email_id=usernamee)

        except user.DoesNotExist:
            username = None

        print(username)
        #if user exist then only below condition will run otherwise it will give error as described in else condition.
        if username is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  #we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################


            msg = "hello here it is your new password  "+password   #this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'kaushalpanchal612@gmail.com',
                [usernamee],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            #now update the password in model
            cuser = user.objects.get(email_id=usernamee)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
    return redirect(index)




