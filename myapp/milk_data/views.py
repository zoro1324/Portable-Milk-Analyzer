# In your_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Cow, District, MilkSubmission,Supplier
from .forms import MilkSubmissionFilterForm, SupplierForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
import numpy as np
from .models import MilkSubmission, Supplier
import tensorflow as tf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MilkSubmissionRequestSerializer
from PIL import Image

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


def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST, request.FILES)
        print("Here")
        if form.is_valid():
            form.save()
            return redirect('milk_data:dashboard')  # update with your list page
    else:
        form = SupplierForm()

    return render(request, 'milk_data/new_supplier.html', {'form': form})
# load ML model once

import base64
import numpy as np
import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .models import MilkSubmission
from .ml_model import predict_milk_quality  # your ML classification function


MODEL_PATH = "ML_model/milk_quality_classifier/milk_quality_classifier.keras"
model = tf.keras.models.load_model(MODEL_PATH)

@csrf_exempt
@api_view(['POST'])
def classify_milk(request):
    try:
        data = JSONParser().parse(request)
        rf_no = data.get("rf_no")
        image_array = data.get("image_array")  # Expecting nested list [[...],[...],...]

        if rf_no is None or image_array is None:
            return JsonResponse({"error": "rf_no and image_array are required"}, status=400)

        # Convert to numpy array
        img = np.array(image_array, dtype=np.uint8)

        # If grayscale, convert to RGB
        if len(img.shape) == 2:
            img = np.stack((img,) * 3, axis=-1)

        # Resize to model input
        img = Image.fromarray(img)
        img = img.resize((128, 128))  # assuming model expects 224x224
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        predictions = model.predict(img_array)
        predicted_class = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        supplier   = Supplier.objects.filter(rf_no=rf_no).first()
        if not supplier:
            return JsonResponse({"error": "Supplier with given rf_no not found"}, status=404)
        # Save in DB

        if predicted_class == 2:
            quality = "Bad"
            supplier.warning_count += 1
            supplier.save()
        elif predicted_class == 1:
            quality = "Average"
        else:
            quality = "Good"
        submission = MilkSubmission.objects.create(
            supplier=supplier,
            quality_of_milk=quality,
            timestamp=timezone.now()
        )
        
        submission.save()
        # Response
        return JsonResponse({
            "quality": quality,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)