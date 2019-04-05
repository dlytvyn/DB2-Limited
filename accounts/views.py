from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.forms import UserRegistrationForm, UserLoginForm
from accounts.models import User
from content.models import Posts, Likes
from accounts.tokens import account_activation_token


def home_view(request):
    if request.session.session_key:
        return redirect('/account_page')
    return render(request, 'accounts/home.html')


def login_view(request):
    if request.session.session_key:
        return redirect('/account_page')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/account_page')
    return render(request, 'accounts/login_form.html', {'form': form})


def registration_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        if request.FILES:
            user.avatar = request.FILES['avatar']
        user.is_active = False
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('accounts/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return redirect('login')
    return render(request, 'accounts/signup_form.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/login')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def account_view(request):
    search_by = request.POST.get("search_by")
    if search_by and not search_by == 'nothing':
        posts_list = Posts.objects.filter(**{'user__' + search_by: request.POST.get('search')})
    else:
        posts_list = Posts.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'accounts/account_page.html', {'posts': posts})


def logout_view(request):
    logout(request)
    return render(request, "accounts/home.html")
