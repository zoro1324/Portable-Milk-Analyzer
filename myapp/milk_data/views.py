# In your_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Cow, MilkSubmission,Supplier
from .forms import MilkSubmissionFilterForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
def dashboard(request):
    """
    Displays the home page with a list of milk submissions
    and a form to filter them.
    """
    # Instantiate the form, populating it with GET data if available
    form = MilkSubmissionFilterForm(request.GET or None)
    
    # Start with all milk submissions
    submissions = MilkSubmission.objects.select_related('supplier', 'supplier__district').all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        district = form.cleaned_data.get('district')
        date = form.cleaned_data.get('date')

        # Apply search filter if a query is provided
        if search_query:
            submissions = submissions.filter(
                Q(supplier__name__icontains=search_query) |
                Q(supplier__rf_no__icontains=search_query)
            )

        # Apply district filter
        if district:
            submissions = submissions.filter(supplier__district=district)
        
        # Apply date filter
        if date:
            submissions = submissions.filter(timestamp__date=date)
        else:
            # By default, if no date is selected, show today's submissions
            if not request.GET: # Only default to today on initial load
                 submissions = submissions.filter(timestamp__date=timezone.now().date())


    context = {
        'form': form,
        'submissions': submissions
    }
    return render(request, 'milk_data/dashboard.html', context)

def supplier_detail(request, pk):
    
    supplier = get_object_or_404(Supplier, pk=pk)

    cows = supplier.cows.all()

    context = {
        'supplier': supplier,
        'cows': cows 
    }
    
    return render(request, 'milk_data/supplier_detail.html', context)

def cow_detail(request, pk):
    """
    Displays the detail page for a single cow.
    """
    # Get the specific cow object or return a 404 error
    cow = get_object_or_404(Cow, pk=pk)

    context = {
        'cow': cow
    }
    
    return render(request, 'milk_data/cow_detail.html', context)

def login_view(request):
    """
    Handles user login manually without AuthenticationForm.
    """
    if request.method == 'POST':
        # Get username and password from the form submission
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')

        try:
            # 1. Find the user by their username
            user = User.objects.get(username=username_from_form)
            
            # 2. Check if the provided password is correct for that user
            if user.check_password(password_from_form):
                # 3. If correct, log them in and create a session
                login(request, user)
                return redirect('milk_data:dashboard')
            else:
                # Password was incorrect
                messages.error(request, "Invalid username or password.")

        except User.DoesNotExist:
            # Username was not found in the database
            messages.error(request, "Invalid username or password.")
            
    # For a GET request, just show the page
    return render(request, 'milk_data/login.html')

def logout_view(request):
    logout(request)
    return redirect('milk_data:login')