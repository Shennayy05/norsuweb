from django.shortcuts import render

def index(request):
    return render(request, 'dashboard/index.html')

def admin_login(request):
    return render(request, 'dashboard/admin-login.html')

def admin_dashboard(request):
    return render(request, 'dashboard/admin-dashboard.html')

def cas_dashboard(request):
    return render(request, 'dashboard/dashbordcas.html')

def cit_dashboard(request):
    return render(request, 'dashboard/dashbordcit.html')

def caf_dashboard(request):
    return render(request, 'dashboard/dashbordcaf.html')

def cted_dashboard(request):
    return render(request, 'dashboard/dashbordcted.html')

def ccje_dashboard(request):
    return render(request, 'dashboard/dashbordccje.html')

def cba_dashboard(request):
    return render(request, 'dashboard/dashbordcba.html')

def news(request):
    return render(request, 'dashboard/newsdashbord.html')

def news1(request):
    return render(request, 'dashboard/news/news1.html')

def programs(request):
    return render(request, 'dashboard/news/programs.html')
