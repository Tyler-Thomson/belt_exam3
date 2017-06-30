from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from django.db.models import Count


def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def getCurrentUser(request):
    user_id = request.session['user_id']
    return User.objects.get(id = user_id)

def index(request):
    print "Inside the index method"
    return render(request, 'belt_exam_app/index.html')

def createUser(request):
    if request.method == 'POST':
        form_data = request.POST
        check = User.objects.validate(form_data)
        if check != []:
            flashErrors(request, check)
            return redirect('/')

        user = User.objects.createUser(form_data)
        request.session['user_id'] = user.id

        print "Inside the create method"
    return redirect('/success')

def success(request):
    print "Inside the success method"
    if 'user_id' in request.session:
        current_user = getCurrentUser(request)
        users = User.objects.all().exclude(id = current_user.id)
        friends_ids = []

        for friend in current_user.friends.all():
            friends_ids.append(friend.id)

        context = {
            'current_user': current_user,
            'users': users,
            'friends_ids': friends_ids,
        }

        return render(request, 'belt_exam_app/success.html', context)
    return redirect('/')

def addFriend(request, id):
    print "Inside the addFriend method"
    if request.method == "POST":
        current_user = getCurrentUser(request)
        friend = User.objects.get(id=id)

        current_user.friends.add(friend)

    return redirect('/success')

def removeFriend(request, id):
    print "Inside the removeFriend method"
    if request.method == "POST":
        current_user = getCurrentUser(request)
        friend = User.objects.get(id=id)

        current_user.friends.remove(friend)

    return redirect('/success')

def viewUser(request, id):
    print "Inside the viewFriend method"
    if request.method == 'POST':
        current_user = getCurrentUser(request)
        user = User.objects.get(id=id)

        context = {
            'user': user,
        }
    return render(request, 'belt_exam_app/friend.html', context)

def login(request):
    print "Inside the login method"
    if request.method == "POST":
        form_data = request.POST
        check = User.objects.login(form_data)

        if type(check) == type(User()):
            request.session['user_id'] = check.id
            return redirect('/success')
        flashErrors(request, check)
    return redirect('/')

def logout(request):
    request.session.pop('user_id')
    return redirect('/')
