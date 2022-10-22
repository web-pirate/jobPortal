from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

# # libraries for email with html_template

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


def home(request):
    user_object = User.objects.all()
    # try:
    #     if request.method == 'POST':
    #         nemail = request.POST.get('news_email')
    #         print(nemail)
    #         new_obj = Newsletters(nemail=nemail)
    #         new_obj.save()
    #         return redirect('home')
    #     else:
    #         return render(request, 'home.html')

    # except Exception as e:
    #     print(e)
    #     return redirect('home')
    print(user_object)
    job_order = Job.objects.all()
    if job_order is not None:
        count = 0
        job_append = []
        for i in job_order:
            print(i)
            job_add = job_append.append(i)
            count = count + 1
            if count == 3:
                break
        job_append.reverse()
    return render(request, 'home.html', {'user_obj': user_object, "job_order": job_append})
    # else:
    #     return render(request, 'home.html', {'user_obj': user_object})


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
        if user_obj:
            profile_obj = Profile.objects.filter(user=user_obj).first()
            print(profile_obj)
            if not profile_obj.is_verified:
                messages.add_message(request, messages.INFO,
                                     "Profile Not Verified check your mail")
                return redirect('login')
            else:
                if user is not None:
                    auth.login(request, user)
                    messages.add_message(
                        request, messages.INFO, "Login Successfull 1234")
                    return render(request, 'home.html', {'username': username})
                else:
                    messages.add_message(
                        request, messages.WARNING, "Wrong Password")
                    return redirect('login')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Please Register on Website.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def about(request):
    return render(request, 'about.html')


def blog_content(request):
    return render(request, 'blog_content.html')


def email_verify(request):
    return render(request, 'email_verify.html')


@csrf_exempt
def contact(request):
    current_obj = request.user
    user_obj = User.objects.filter(username=current_obj).first()
    try:
        if request.method == 'POST':
            name = request.POST.get('uname')
            email = request.POST.get('uemail')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            contact_obj = Contact(name=name, email=email,
                                  subject=subject, message=message)
            contact_obj.save()
            print('contant send')
            messages.add_message(
                request, messages.SUCCESS, "Your message is recieved successfull!!")
            print("message")
            return redirect('contact')

    except Exception as e:
        print(e)
    # models already made
    return render(request, 'contact.html', {'user': user_obj})


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
            return redirect('email_verify')
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
    message = f'Hi click the link to verify your account https://jobwebportal.herokuapp.com/verify/{token}'
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


# @login_required(login_url="login")
def company_profile(request):
    current_user = request.user
    if current_user:
        company_obj = Company_profile.objects.filter(user=current_user).first()
        pro_job = Job.objects.filter(jcname=company_obj).all()
        return render(request, 'company_profile.html', {'company': company_obj, "job": pro_job})
    else:
        return render(request, 'company_profile.html')


def company_registration(request):
    user_obj = request.user
    company_profile_obj = Company_profile.objects.filter(user=user_obj).first()
    if company_profile_obj:
        messages.add_message(request, messages.INFO,
                             f"{user_obj}, your Company is already exist.")
        return redirect('company_profile')
    else:
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


def edit_company(request, company_obj):
    user_obj = request.user
    company_obj = Company_profile.objects.filter(user=user_obj).first()
    if request.method == "POST" and company_obj:
        cname = request.POST.get('cname')
        cimage = request.POST.get('pro_img')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        clocation = request.POST.get('clocation')
        cdescription = request.POST.get('cdescription')
        created_at = company_obj.created_at

        user_obj = request.user
        find_user = User.objects.filter(username=user_obj).first()
        company_profile_obj = Company_profile(id=company_obj.id,
                                              user=find_user, cname=cname, cimage=cimage, cemail=cemail, clocation=clocation, cphone=cphone, cdescription=cdescription,
                                              created_at=created_at)
        company_profile_obj.save()
        return redirect('company_profile')
    else:
        return render(request, 'edit_company.html', {'company': company_obj})


# def job_details(company_obj):
#     job_obj = Job.objects.filter(cname=company_obj).all()

def user_list(request):
    user_obj = User.objects.all()
    return render(request, 'user_list.html', {"user_obj": user_obj})


def user_view(request, pk):
    user_obj = User.objects.filter(username=pk).first()
    return render(request, 'user_view.html', {"user_obj": user_obj})


def remove_job(request, job_id):
    owner = request.user
    com_detail = Company_profile.objects.filter(user=owner).first()
    print(com_detail)
    job_obj = Job.objects.filter(id=job_id).first()
    if com_detail:
        print('if')
        job_obj.delete()
        return redirect('home')
    else:
        print(f'{job_obj.job_position} is not deleted!!!')
        return redirect('company_profile')
