from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request):
    if request.method == 'POST':
        tache = request.POST.get('tache')
        nouvelle_tache = Todo(user=request.user, todo_name=tache)
        nouvelle_tache.save()

    toutes_taches = Todo.objects.filter(user=request.user)
    context = {
        'toutes_taches': toutes_taches,
    }
    return render(request, 'todo_app/home.html', context)


def login_view(request): 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
    
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide")
            return redirect('login')

    return render(request, 'todo_app/login.html')




def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 6:
            messages.error(request, 'Le mot de passe doit contenir au moins 6 caractères')
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, "Ce nom d'utilisateur existe déjà")
            return redirect('register')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save() 
        messages.success(request, "Votre enregistrement est réussi, veillez vous connecter à présent")
        return redirect('login')
    return render(request, 'todo_app/register.html') 

@login_required
def supprimer(request, name):
    sup_tache = Todo.objects.get(user=request.user, todo_name=name)
    sup_tache.delete()
    return redirect('home') 
@login_required
def update(request,name):
    update_tache = Todo.objects.get(user=request.user, todo_name=name)
    update_tache.status = True
    update_tache.save()
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('login')