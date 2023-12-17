from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task
from .forms import CreateUserForm,LoginForm,TaskForm
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
   
    return render(request, "index.html")


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    tasks = []
    
    
    tasks = Task.objects.filter(user=user)

    if tasks is not None:
    
        task_events = [{'title': task.title, 'completed': 1 if task.completed else 0, 'start': task.scheduled_date.strftime('%Y-%m-%d')} for task in tasks]

    else:
        task_events = []

    context = {
        
        'tasks': tasks,
        'task_events': task_events,
    }

    return render(request, "dashboard.html", context=context)



from django.contrib import messages
import random
from django.core.mail import send_mail

@csrf_exempt
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until verification
            user.save()

            # Generate a random 6-digit OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Send OTP to the user's email
            subject = 'Account Verification OTP'
            message = f'Your OTP for account verification is: {otp}'
            recipient_email = user.email
            send_mail(subject, message, from_email=None, recipient_list=[recipient_email])

            messages.success(request, 'Account created successfully. Check your email for OTP.')
            return redirect(verify_otp, username=user.username, otp=otp)

    context = {'form': form}
    return render(request, "register.html", context=context)


@csrf_exempt
def verify_otp(request, username, otp):
    if request.method == 'POST':
        entered_otp = request.POST['otp']

        # Check if entered OTP matches
        if entered_otp == otp:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return redirect('login')  # Redirect to login page after successful verification

    return render(request, 'verify_otp.html', {'username': username})




@csrf_exempt
def login(request):

    form = LoginForm

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user  is not None:
                auth.login(request, user)

                return redirect(dashboard)
            
    context = {'form':form}
    return render(request, "login.html",context=context)

def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required(login_url='login')
def createTask(request):

        form = TaskForm()

        if request.method == 'POST':

            form = TaskForm(request.POST)

            if form.is_valid():

                task = form.save(False)
                task.user = request.user
                
                task.save()

                return redirect(dashboard)
        
        context = {'form':form}

        return render(request, "create-task.html",context=context)
    
@login_required(login_url='login')
def updateTask(request,pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect(dashboard)
    
    context = {'form':form}

    return render(request, 'update-task.html', context=context)


@login_required(login_url='login')
def deleteTask(request,pk):
    task = Task.objects.get(id=pk)

    task.delete()

    return redirect(dashboard)


from django.http import JsonResponse

def update_task_status(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(id=pk)
        task.completed = not task.completed  # Toggle the completed field
        task.save()

        return JsonResponse({'status': 'success', 'completed': task.completed})

    return JsonResponse({'status': 'error'})



