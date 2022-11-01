import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from datetime import date


# # libraries for email with html_template

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


def home(request):
    title = "Job Portal"
    verifed_user = reversed(Profile.objects.all())
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
    user_object = UserDetails.objects.all()
    job_order = reversed(Job.objects.all())
    if job_order is not None:
        count = 0
        job_append = []
        for i in job_order:
            print(i)
            job_add = job_append.append(i)
            count = count + 1
            if count == 3:
                break
        # job_append.reverse()
    return render(request, 'home.html', {'user_obj': user_object, "job_order": job_append, 'title': title})
    # else:
    #     return render(request, 'home.html', {'user_obj': user_object})


def register(request):
    title = "Register"
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

        # Delete the user that are not verified
    # allUser = User.objects.all()
    # for a in allUser :
    #     print(allUser.cre)

    else:
        return render(request, 'register.html', {'title': title})


def login(request):
    title = "Login"
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
        return render(request, 'login.html', {'title': title})


def logout(request):
    auth.logout(request)
    return redirect('home')


def about(request):
    title = "About Us"
    return render(request, 'about.html', {'title': title})


def blog_content(request):
    title = 'Blog'
    return render(request, 'blog_content.html', {'title': title})


def email_verify(request):
    title = "Email Verification"
    return render(request, 'email_verify.html', {'title': title})


@csrf_exempt
def contact(request):
    title = "Contact Us"
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
    return render(request, 'contact.html', {'user': user_obj, 'title': title})


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
    n1 = "\n"
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
    title = "Company Profile"
    current_user = request.user
    if current_user:
        company_obj = Company_profile.objects.filter(user=current_user).first()
        pro_job = reversed(Job.objects.filter(jcname=company_obj).all())
        return render(request, 'company_profile.html', {'company': company_obj, "job": pro_job, 'title': title})
    else:
        return render(request, 'company_profile.html', {'title': title})


def company_registration(request):
    title = "Company Registeration"
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
            cimage = request.FILES['pro_img']
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
            return redirect('home', {'title': title})
        else:
            print("Registration failed")
            return render(request, 'company_registration.html', {'title': title})


def company_view(request, cname):
    comp_obj = Company_profile.objects.filter(cname=cname).first()
    title = cname
    ident = comp_obj.id
    job_obj = reversed(Job.objects.filter(jcname=ident).all())
    count = 0
    job_app = []
    i = 0
    for i in job_obj:
        ad = job_app.append(i)
        count = count + 1
        if count == 3:
            break
    return render(request, 'company_view.html', {"company": comp_obj, "job": job_app, "title": title})


# def job_view(request):
#     comp_obj = Company_profile.objects.filter(cname=cname).first()
#     ident = comp_obj.id
#     job_obj = reversed(Job.objects.filter(jcname=ident).all())
#     count = 0
#     job_app = []
#     # i = id
#     for i in job_obj:
#         ad = job_app.append(i)
#         count = count + 1
#         if count == 3:
#             break
#     return render(request, 'company_view.html', {"company": comp_obj, "job": job_app})
#     pass


def edit_company(request, company_obj):
    user_obj = request.user
    company_obj = Company_profile.objects.filter(user=user_obj).first()
    title = company_obj.cname
    if request.method == "POST" and company_obj:
        cname = request.POST.get('cname')
        cimage = request.FILES['pro_img']
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        clocation = request.POST.get('clocation')
        cdescription = request.POST.get('cdescription')
        created_at = company_obj.created_at

        if len(cimage) > 0:
            os.remove(company_obj.cimage.path)
            print("Image Removed")

        user_obj = request.user
        find_user = User.objects.filter(username=user_obj).first()
        company_profile_obj = Company_profile(id=company_obj.id,
                                              user=find_user, cname=cname, cimage=cimage, cemail=cemail, clocation=clocation, cphone=cphone, cdescription=cdescription,
                                              created_at=created_at)
        company_profile_obj.save()
        return redirect('company_profile')
    else:
        return render(request, 'edit_company.html', {'company': company_obj, 'title': title})


# def job_details(company_obj):
#     job_obj = Job.objects.filter(cname=company_obj).all()

def user_list(request):
    user_obj = User.objects.all()
    title = "User List"
    return render(request, 'user_list.html', {"user_obj": user_obj, 'title': title})


@csrf_exempt
def user_view(request, pk):
    user_obj = User.objects.filter(username=pk).first()
    title = user_obj.username
    user_detail = UserDetails.objects.filter(username=user_obj).first()
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
    # print(user_detail.username)
    return render(request, 'user_view.html', {"user_obj": user_obj, "userDetail": user_detail, 'title': title})


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


def jobs(request):
    title = "Jobs"
    job_obj = reversed(Job.objects.all())
    count = 0
    job_ap = []
    for i in job_obj:
        ap = job_ap.append(i)
        count = count + 1
        if count > 12:
            break
    return render(request, 'jobsall.html', {"job": job_ap, 'title': title})


def job_create(request):
    current = request.user.is_authenticated
    if current:
        current_user = request.user
        print(current_user)
        user_obj = User.objects.filter(username=current_user).first()
        comp_obj = Company_profile.objects.filter(user=user_obj).first()
        title = comp_obj
        print(comp_obj)
        if request.method == 'POST':
            jposition = request.POST.get('jposition')
            jlocation = request.POST.get('jlocation')
            jdesc = request.POST.get('jdesc')
            jsalary = request.POST.get('jsalary')
            jtype = request.POST.get('jtype')

            job_create = Job(jcname=comp_obj, jposition=jposition, jlocation=jlocation, jdesc=jdesc,
                             jsalary=jsalary, jtype=jtype)
            job_create.save()
            print(job_create)
            return redirect('company_profile')
        else:
            return render(request, 'job_create.html', {'company': comp_obj, 'title': title})

    else:
        return home(request)


def user_details(request):
    current = request.user.is_authenticated
    title = "User Details"
    if current:
        current_user = request.user
        # if UserDetails.objects.filter(username=request.user).first():
        #     return redirect(user_update)
        print(current_user)
        user_obj = User.objects.filter(username=current_user).first()
        title = user_obj
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            print(full_name)
            about = request.POST.get('about')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            category = request.POST.get('category')
            language = request.POST.get('language')
            dob = request.POST.get('dob')

            edu_type_1 = request.POST.get('edu_type_1')
            edu_marks_1 = request.POST.get('edu_marks_1')
            edu_percentage_1 = request.POST.get('edu_percentage_1')
            edu_branch_1 = request.POST.get('edu_branch_1')
            edu_year_1 = request.POST.get('edu_year_1')
            edu_inst_1 = request.POST.get('edu_inst_1')
            print(edu_inst_1)
            edu_location_1 = request.POST.get('edu_location_1')
            edu_about_1 = request.POST.get('edu_about_1')

            edu_type_2 = request.POST.get('edu_type_2')
            edu_marks_2 = request.POST.get('edu_marks_2')
            edu_percentage_2 = request.POST.get('edu_percentage_2')
            edu_branch_2 = request.POST.get('edu_branch_2')
            edu_year_2 = request.POST.get('edu_year_2')
            edu_inst_2 = request.POST.get('edu_inst_2')
            edu_location_2 = request.POST.get('edu_location_2')
            edu_about_2 = request.POST.get('edu_about_2')

            user_img = request.FILES['user_img']
            resume = request.FILES['resume']
            print(resume)

            user_detail = UserDetails(username=user_obj, full_name=full_name, about=about, gender=gender, address=address, phone=phone, category=category, language=language, dob=dob, edu_type_1=edu_type_1,
                                      edu_marks_1=edu_marks_1, edu_percentage_1=edu_percentage_1, edu_branch_1=edu_branch_1, edu_year_1=edu_year_1,
                                      edu_inst_1=edu_inst_1, edu_location_1=edu_location_1, edu_about_1=edu_about_1, edu_type_2=edu_type_2, edu_marks_2=edu_marks_2, edu_percentage_2=edu_percentage_2,
                                      edu_branch_2=edu_branch_2, edu_year_2=edu_year_2, edu_inst_2=edu_inst_2, edu_location_2=edu_location_2, edu_about_2=edu_about_2, resume=resume, user_img=user_img)
            print(user_detail)
            user_detail.save()
            return redirect(experience)

    else:
        return redirect(login)

    detail_obj = UserDetails.objects.filter(username=user_obj).first()
    # print(detail_obj.about)
    return render(request, "user_details.html", {'current': request.user, 'title': title, 'detail': detail_obj})


def user_update(request):
    current = request.user.is_authenticated
    title = "User Details"
    if current:
        current_user = request.user
        user_obj = User.objects.filter(username=current_user).first()
        user_detail_obj = UserDetails.objects.filter(username=user_obj).first()
        title = user_obj
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            about = request.POST.get('about')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            category = request.POST.get('category')
            language = request.POST.get('language')
            dob = request.POST.get('dob')

            edu_type_1 = request.POST.get('edu_type_1')
            edu_marks_1 = request.POST.get('edu_marks_1')
            edu_percentage_1 = request.POST.get('edu_percentage_1')
            edu_branch_1 = request.POST.get('edu_branch_1')
            edu_year_1 = request.POST.get('edu_year_1')
            edu_inst_1 = request.POST.get('edu_inst_1')
            edu_location_1 = request.POST.get('edu_location_1')
            edu_about_1 = request.POST.get('edu_about_1')

            edu_type_2 = request.POST.get('edu_type_2')
            edu_marks_2 = request.POST.get('edu_marks_2')
            edu_percentage_2 = request.POST.get('edu_percentage_2')
            edu_branch_2 = request.POST.get('edu_branch_2')
            edu_year_2 = request.POST.get('edu_year_2')
            edu_inst_2 = request.POST.get('edu_inst_2')
            edu_location_2 = request.POST.get('edu_location_2')
            edu_about_2 = request.POST.get('edu_about_2')

            user_img = request.FILES['user_img']
            if len(user_img) > 0:
                os.remove(user_detail_obj.user_img.path)
                print("Profile Image Removed")
            resume = request.FILES['resume']
            if len(user_img) > 0:
                os.remove(user_detail_obj.resume.path)
                print("Profile Resume Removed")

            user_detail = UserDetails(id=user_detail_obj.id, username=user_obj, full_name=full_name, about=about, gender=gender, address=address, phone=phone, category=category, language=language, dob=dob, edu_type_1=edu_type_1,
                                      edu_marks_1=edu_marks_1, edu_percentage_1=edu_percentage_1, edu_branch_1=edu_branch_1, edu_year_1=edu_year_1,
                                      edu_inst_1=edu_inst_1, edu_location_1=edu_location_1, edu_about_1=edu_about_1, edu_type_2=edu_type_2, edu_marks_2=edu_marks_2, edu_percentage_2=edu_percentage_2,
                                      edu_branch_2=edu_branch_2, edu_year_2=edu_year_2, edu_inst_2=edu_inst_2, edu_location_2=edu_location_2, edu_about_2=edu_about_2, resume=resume, user_img=user_img)
            print(user_detail)
            user_detail.save()

            return redirect('profile')
        else:
            detail_obj = UserDetails.objects.filter(username=user_obj).first()
            return render(request, 'user_update.html', {'current': request.user, 'title': title, 'detail': detail_obj})


def profile(request):
    title = (request.user)
    current = request.user.is_authenticated
    if current:
        # if UserDetails.objects.filter(username=request.user).first() is None:
        #     return redirect(user_details)
        detail_obj = UserDetails.objects.filter(username=request.user).first()
        today = date.today()
        birth_year = detail_obj.dob.split("-")
        age = today.year - int(birth_year[0])
        exp_obj = UserExperience.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'details': detail_obj, "experience": exp_obj, "title": title, "age": age})


def experience(request):
    current = request.user.is_authenticated
    title = "User Experience"
    if current:
        if request.method == 'POST':
            username = request.user
            experience = request.POST.get('experience')
            print(experience)

            exp_position_1 = request.POST.get('exp_position_1')
            exp_from_1 = request.POST.get('exp_from_1')
            exp_to_1 = request.POST.get('exp_to_1')
            exp_comp_1 = request.POST.get('exp_comp_1')
            exp_location_1 = request.POST.get('exp_location_1')
            exp_about_1 = request.POST.get('exp_about_1')
            print(exp_about_1)

            exp_position_2 = request.POST.get('exp_position_2')
            exp_from_2 = request.POST.get('exp_from_2')
            exp_to_2 = request.POST.get('exp_to_2')
            exp_comp_2 = request.POST.get('exp_comp_2')
            exp_location_2 = request.POST.get('exp_location_2')
            exp_about_2 = request.POST.get('exp_about_2')
            print(exp_about_1)

            print(experience)

            user_experience = UserExperience(user=username, experience=experience, exp_position_1=exp_position_1, exp_from_1=exp_from_1, exp_to_1=exp_to_1, exp_comp_1=exp_comp_1, exp_location_1=exp_location_1,
                                             exp_about_1=exp_about_1, exp_position_2=exp_position_2, exp_from_2=exp_from_2, exp_to_2=exp_to_2, exp_comp_2=exp_comp_2, exp_location_2=exp_location_2, exp_about_2=exp_about_2)
            print(user_experience)
            user_experience.save()
            return redirect(profile)

    else:
        return redirect(login)

    return render(request, 'experience.html', {'title': title})


def exp_update(request, user_obj):
    current = request.user.is_authenticated
    title = "User Experience Update"
    if current:
        if request.method == 'POST':
            username = request.user
            experience = request.POST.get('experience')
            print(experience)

            exp_position_1 = request.POST.get('exp_position_1')
            exp_from_1 = request.POST.get('exp_from_1')
            exp_to_1 = request.POST.get('exp_to_1')
            exp_comp_1 = request.POST.get('exp_comp_1')
            exp_location_1 = request.POST.get('exp_location_1')
            exp_about_1 = request.POST.get('exp_about_1')
            print(exp_about_1)

            exp_position_2 = request.POST.get('exp_position_2')
            exp_from_2 = request.POST.get('exp_from_2')
            exp_to_2 = request.POST.get('exp_to_2')
            exp_comp_2 = request.POST.get('exp_comp_2')
            exp_location_2 = request.POST.get('exp_location_2')
            exp_about_2 = request.POST.get('exp_about_2')
            print(exp_about_1)

            print(experience)
            exp_obj = UserExperience.objects.filter(user=request.user).first()
            user_experience = UserExperience(id=exp_obj.id, user=username, experience=experience, exp_position_1=exp_position_1, exp_from_1=exp_from_1, exp_to_1=exp_to_1, exp_comp_1=exp_comp_1, exp_location_1=exp_location_1,
                                             exp_about_1=exp_about_1, exp_position_2=exp_position_2, exp_from_2=exp_from_2, exp_to_2=exp_to_2, exp_comp_2=exp_comp_2, exp_location_2=exp_location_2, exp_about_2=exp_about_2)
            print(user_experience)
            user_experience.save()
            return redirect(profile)

    else:
        return redirect(login)

    exp_obj = UserExperience.objects.filter(user=request.user).first()
    return render(request, 'experience_update.html', {'title': title, 'exp': exp_obj})


def user_apply_now(request):
    return render(request, 'user_apply_now.html')


def job_apply(request):
    return render(request, 'job_apply.html')
