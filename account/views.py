from django.shortcuts import redirect, render
from .models import User

# Create your views here.
def login(request):
    if request.method=="POST" and request.POST['username']!="" and request.POST['password']!="":
        user=User.objects.filter(user_name=request.POST['username']).first()
        if user!=None and user.password==request.POST['password']:
            request.session['sessionuser_id']=user.id
            return redirect('todos:home')
    return render(request, 'login.html')

def signup(request):
    if request.method=="POST" and request.POST['name']!="" and request.POST['username']!="" and request.POST['email']!="" and request.POST['password']!="":
        user=User(name=request.POST['name'],user_name=request.POST['username'], email=request.POST['email'], password=request.POST['password'])

        if user!=None:
            user.save()
            request.session['sessionuser_id']=user.id
            return redirect('todos:home')
    return render(request, 'signup.html')
    
def logout(request):
    if 'sessionuser_id' in request.session:
        del request.session['sessionuser_id']
    return render(request,'login.html')