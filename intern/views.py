from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail


# # libraries for email with html_template

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        try:

            if User.objects.filter(username=uname).first():
                messages.success(request, 'Username Already Taken.')
                return redirect(register)
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email Already Taken.')
                return redirect(register)

            if password == password2:
                new_user = User.objects.create_user(
                    username=uname, first_name=fname, last_name=lname, email=email, password=password)
                new_user.save()

                auth_token = str(uuid.uuid4())
                profile_obj = Profile(user=new_user, auth_token=auth_token)
                profile_obj.save()
                send_email_after_registration(email, auth_token)
                return redirect('token')
        except Exception as e:
            print("Daily Limit Excced")
            return redirect('register')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        user_obj = User.objects.filter(username=username).first()
        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.add_message(request, messages.INFO,
                                 "Profile Not Verified check your mail")
            return redirect('login')

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.INFO, "Login Successfull")
            return render(request, 'home.html', {'username': username})
        else:
            messages.add_message(request, messages.WARNING, "Wrong Password")
            # currentuser = request.user
            # print(currentuser)
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def contact(request):
    # models already made
    return render(request, 'contact.html')


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj.is_verified:
            messages.add_message(request, messages.INFO,
                                 "E-mail is already Verified!")
            return redirect('login')
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.add_message(request, messages.INFO,
                                 "E-mail Verified Successfull")
            return redirect('success')
        else:
            return redirect('error')

    except Exception as e:
        print(e)


def error(request):
    print('ERROR')
    return render(request, 'contact.html')


def email_template(request, token):
    return render(request, 'email.html', {'token': token})


def send_email_after_registration(email, token):
    subject = "Your accounts need to be verified!!"
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

    # # html template in email
    # html_content = render_to_string('email.html')
    # text_content = strip_tags(html_content)
    # message = text_content
    # email_html = EmailMultiAlternatives(
    #     subject, message, email_from, recipient_list)
    # email_html.attach_alternative(html_content, "text/html")
    # email_html.send()

# Company Profile


def company_profile(request):
    return render(request, 'company_profile.html')


def company_registration(request):
    user_obj = request.user
    print(user_obj)
    if request.method == "POST":
        cname = request.POST.get('cname')
        cimage = request.POST.get('pro_img')
        print(cimage)
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        clocation = request.POST.get('clocation')
        cdescription = request.POST.get('cdescription')

        user_obj = request.user
        find_user = User.objects.filter(username=user_obj).first()
        company_profile_obj = Company_profile(
            user=find_user, cname=cname, cimage=cimage, cemail=cemail, clocation=clocation, cphone=cphone, cdescription=cdescription)
        company_profile_obj.save()
        return redirect('home')
    else:
        print("Registration failed")
        return render(request, 'company_registration.html')
