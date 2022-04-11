from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_check, login as login_checks, get_user_model
from django.contrib import messages
import json

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            p1 = User.objects.filter(position_id=1)
            return render(request, 'vote/admin_position1.html', {'np': p1})
        p1 = User.objects.filter(position_id=1)
        return render(request, 'vote/position1.html', {'np': p1})
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def position2(request):
    p2 = User.objects.filter(position_id=2)
    return render(request, 'vote/position2.html', {'np': p2})


@login_required(login_url='login')
def position3(request):
    p3 = User.objects.filter(position_id=3)
    return render(request, 'vote/position3.html', {'np': p3})


@login_required(login_url='login')
def position4(request):
    p4 = User.objects.filter(position_id=4)
    return render(request, 'vote/position4.html', {'np': p4})


@login_required(login_url='login')
def position5(request):
    p5 = User.objects.filter(position_id=5)
    return render(request, 'vote/position5.html', {'np': p5})


@login_required(login_url='login')
def summary(request):
    qrt = Vote.objects.filter(voter_id=request.user.pk)
    print(len(qrt))
    for i in qrt:
        i.updated_at = User.objects.get(pk=i.contestant).image.url
        i.created_at = User.objects.get(pk=i.contestant)
        i.contestant = str(i.position.pk)
    return render(request, 'vote/summary.html', {'np': qrt})


def logout(request):
    u = request.user
    logout_check(request)
    messages.warning(request, f'Thanks for voting {u.first_name} {u.last_name}.')
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid:
            n = request.POST['name'].upper()
            name = n.replace(" ", "")
            password = 'JULIUS'
            user = authenticate(username=name, password=password)
            if user is None:
                messages.warning(request, 'Sorry, you have not been authorized to vote!')
                return render(request, 'login.html')
            else:
                if user.is_active:
                    login_checks(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, 'Invalid credentials')
                    return render(request, 'login.html')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid:
            fn = request.POST['first_name'].upper()
            mn = request.POST['middle_name'].upper()
            ln = request.POST['last_name'].upper()
            position = request.POST['position']
            image = request.FILES.get('image')
            name = f'{fn} {mn} {ln}'

            if mn == ' ':
                username = fn + ln
            else:
                username = fn + mn + ln

            try:
                existing_user = User.objects.get(username=username, is_active=True)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                existing_user = None

            if existing_user:
                messages.warning(request, f'{name} has already been authorized')
                return redirect('register')
            else:
                print(name, position, image)
                user = User.objects.create_user(username=username.replace(" ", ""), password='JULIUS',
                                                position_id=position,
                                                image=image, first_name=fn, last_name=ln)
                user.save()
                messages.success(request, f'{name} has been authorized successfully!')
                return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def vote(request, cid, pid):
    voter = request.user.pk
    existing_vote = Vote.objects.filter(voter_id=voter, position_id=pid)
    nxt_p = int(pid) + 1
    next_position = User.objects.filter(position_id=nxt_p)
    if nxt_p > 5:
        if existing_vote:
            for i in existing_vote:
                i.contestant = cid
                i.save()
            messages.success(request, 'Voting updated successfully')
            return redirect('summary')
        else:
            Vote.objects.create(voter_id=voter, position_id=pid, contestant=cid)
            messages.success(request, 'Voting recorded successfully')
            return redirect('summary')
    elif existing_vote:
        for i in existing_vote:
            i.contestant = cid
            i.save()
        messages.success(request, 'Voting updated successfully')
        return render(request, f'vote/position{nxt_p}.html', {'np': next_position, 'vid': request.user.pk})
    else:
        Vote.objects.create(voter_id=voter, position_id=pid, contestant=cid)
        messages.success(request, 'Voting recorded successfully')
        return render(request, f'vote/position{nxt_p}.html', {'np': next_position, 'vid': request.user.pk})


def options(request):
    return render(request, "vote/options.html")


@login_required(login_url='login')
def overview(request):
    total_voters = len(User.objects.all().exclude(is_superuser=True))
    qrt = User.objects.exclude(position_id=None).order_by('position')
    p = Position.objects.all()
    p1, p2, p3, p4, p5 = 0, 0, 0, 0, 0
    for i in p:
        total = Vote.objects.filter(position_id=i.pk)
        if i.pk == 1:
            p1 = len(total)
        elif i.pk == 2:
            p2 = len(total)
        elif i.pk == 3:
            p3 = len(total)
        elif i.pk == 4:
            p4 = len(total)
        else:
            p5 = len(total)
    for i in qrt:
        total = Vote.objects.filter(contestant=i.pk, position_id=i.position.pk)
        i.username = len(total)
        if i.position.pk == 1:
            i.password = str((len(total) / total_voters) * 100)[:5] + '%'
        elif i.position.pk == 2:
            i.password = str((len(total) / total_voters) * 100)[:5] + '%'
        elif i.position.pk == 3:
            i.password = str((len(total) / total_voters) * 100)[:5] + '%'
        elif i.position.pk == 4:
            i.password = str((len(total) / total_voters) * 100)[:5] + '%'
        else:
            i.password = str((len(total) / total_voters) * 100)[:5] + '%'

    data = {'votes': qrt,
            'p1': p1,
            'p2': p2,
            'p3': p3,
            'p4': p4,
            'p5': p5,
            'all': total_voters
            }

    return render(request, "overview.html", data)


@login_required(login_url='login')
def final_result(request):
    total_voters = len(User.objects.all().exclude(is_superuser=True))
    qrt = User.objects.exclude(position_id=None).order_by('position')  # get contestant
    p1, p2, p3, p4, p5, final = [], [], [], [], [], []  # holds contestant votes for each position

    if len(Vote.objects.all()) == 0:
        empty = True
        return render(request, "final_result.html", {'empty': empty})

    for i in qrt:
        total = Vote.objects.filter(contestant=i.pk, position_id=i.position.pk)
        i.username = len(total)  # user total votes
        if i.position.pk == 1:
            i.updated_at = str((len(total) / total_voters) * 100)[:5] + '%'
            dict = {k: getattr(i, k) for k in
                    ['username', 'first_name', 'last_name', 'position', 'image', 'updated_at']}  # json object
            p1.append(dict)
        elif i.position.pk == 2:
            i.updated_at = str((len(total) / total_voters) * 100)[:5] + '%'
            dict = {k: getattr(i, k) for k in
                    ['username', 'first_name', 'last_name', 'position', 'image', 'updated_at']}
            p2.append(dict)
        elif i.position.pk == 3:
            i.updated_at = str((len(total) / total_voters) * 100)[:5] + '%'
            dict = {k: getattr(i, k) for k in
                    ['username', 'first_name', 'last_name', 'position', 'image', 'updated_at']}
            p3.append(dict)
        elif i.position.pk == 4:
            i.updated_at = str((len(total) / total_voters) * 100)[:5] + '%'
            dict = {k: getattr(i, k) for k in
                    ['username', 'first_name', 'last_name', 'position', 'image', 'updated_at']}
            p4.append(dict)
        else:
            i.updated_at = str((len(total) / total_voters) * 100)[:5] + '%'
            dict = {k: getattr(i, k) for k in
                    ['username', 'first_name', 'last_name', 'position', 'image', 'updated_at']}
            p5.append(dict)

    all = [p1, p2, p3, p4, p5]  # get contestants with highest votes
    for x in all:
        event = max(x, key=lambda ev: ev['username'])
        final.append(event)

    data = {'votes': final, 'empty': False}
    return render(request, "final_result.html", data)


# users
@login_required(login_url='login')
def users(request):
    queryset = User.objects.all().exclude(is_superuser=True)
    return render(request, "users.html", {'users': queryset})


@login_required(login_url='login')
def remove_user(request, pk):
    admin = request.user
    user = User.objects.get(pk=pk)
    u = user
    if request.method == 'POST':
        if admin.is_superuser or admin.is_staff:
            user.delete()
            messages.success(request, f'{u} removed successfully')
            return redirect('users')
        else:
            messages.warning(request, f"Sorry, you're not authorized to remove users")
            return redirect('users')
    return render(request, 'remove_user_prompt.html', {'item': user})


