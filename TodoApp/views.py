from django.shortcuts import redirect, render


# Create your views here.
def homeredirect(request):
    if 'sessionuser_id' in request.session:
        return redirect('/todos/',permanent=True)
    return render(request,'loginsignup.html')
def contact_us(request):
    return render(request, 'contact_us.html',{})
def about_us(request):
    return render(request, 'about_us.html',{})
