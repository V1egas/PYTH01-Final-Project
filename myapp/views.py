# myapp/views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

def index(request):
    """Home page view"""
    return render(request, 'myapp/index.html')


def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('myapp:index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'myapp/login.html')
def radar(request):
    return render(request, 'myapp/radar.html')

def darkMode(request):
    return render(request,'myapp/dark.light.Mode.html')


def register(request):
    """Handle user registration with email"""
    if request.method == 'POST':
        # Get data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        #Validate passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('myapp:register')

        #Validate password strength
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('myapp:register')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('myapp:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return redirect('myapp:register')

        try:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            # For additional fields
            user.is_active = True
            user.save()

            # Login
            auth_user = authenticate(username=username, password=password1)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, f"Welcome {username}!")
                return redirect('myapp:index')

        except IntegrityError:
            messages.error(request, "Registration failed. Please try again.")
            return redirect('myapp:register')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('myapp:register')


    return render(request, 'myapp/register.html')

def user_logout(request):
    logout(request)
    return redirect('myapp:index')

@login_required
def profile(request):
    return render(request, 'myapp/profile.html')


@login_required
def settings(request):
    return render(request, 'myapp/settings.html')

"""
@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        confirm_email = request.POST.get('confirm_email')
        password = request.POST.get('password')

        if new_email != confirm_email:
            messages.error(request, "Email addresses don't match")
        elif not request.user.check_password(password):
            messages.error(request, "Incorrect password")
        else:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully")
        return redirect('myapp:settings')
    return redirect('myapp:settings')
"""
@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        confirm_email = request.POST.get('confirm_email')
        password = request.POST.get('password')

        if new_email != confirm_email:
            messages.error(request, "Email addresses don't match")
        elif not request.user.check_password(password):
            messages.error(request, "Incorrect password")
        else:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully")
        return redirect('myapp:settings')
    return redirect('myapp:settings')
"""
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect")
        elif new_password != confirm_password:
            messages.error(request, "New passwords don't match")
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password updated successfully")
        return redirect('myapp:settings')
    return redirect('myapp/settings.html')
"""


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect")
        elif new_password != confirm_password:
            messages.error(request, "New passwords don't match")
        elif len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters")
        else:
            user = request.user
            user.set_password(new_password)
            user.save()

            updated_user = authenticate(username=user.username, password=new_password)
            if updated_user is not None:
                login(request, updated_user)

            messages.success(request, "Password updated successfully")
            return redirect('myapp:settings')  # Redirect back to settings page

    return redirect('myapp:settings')

def is_admin(user):
    return user.is_superuser

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get all users
    user_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(user_list, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    #time ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Get stats
    total_users = User.objects.count()

    # Active today
    active_today = User.objects.filter(
        last_login__date=today
    ).count()

    # New this week
    new_this_week = User.objects.filter(
        date_joined__gte=week_ago
    ).count()

    context = {
        'users': users,
        'total_users': total_users,
        'active_today': active_today,
        'new_this_week': new_this_week
    }
    return render(request, 'myapp/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent editing superusers unless you're the same user or higher privilege
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can access this page")
        return redirect('myapp:admin_dashboard')

    if request.method == 'POST':
        # Update
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.is_active = request.POST.get('is_active') == '1'
        user.is_staff = request.POST.get('is_staff') == '1'
        user.is_superuser = request.POST.get('is_superuser') == '1'


        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        if new_password and confirm_password:
            if new_password == confirm_password:
                if len(new_password) >= 8:
                    user.set_password(new_password)
                    messages.success(request, "Password was successfully updated")
                else:
                    messages.error(request, "Password must be at least 8 characters")
            else:
                messages.error(request, "Passwords did not match - password not updated")

        try:
            user.save()
            messages.success(request,
                             f"Updated {user.username} Admin: "
                             f"{'Superuser' if user.is_superuser else 'Admin user' if user.is_staff else 'Regular user'}"
                             f" Status: {'Active' if user.is_active else 'Inactive '}"
                             )

        except IntegrityError:
            messages.error(request, "Username or email already exists")

        return redirect('myapp:admin_dashboard')

    return render(request, 'myapp/admin_edit_user.html', {'user': user})


@login_required
@user_passes_test(is_admin)
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent editing superusers unless you're the same user or higher privilege
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can access this page")
        return redirect('myapp:admin_dashboard')

    if request.method == 'POST':
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully")
        return redirect('myapp:admin_dashboard')
    return render(request, 'myapp/admin_confirm_delete.html', {'user': user})



