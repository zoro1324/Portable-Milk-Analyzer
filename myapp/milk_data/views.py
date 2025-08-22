from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier, MilkSubmission, District
from .forms import MilkSubmissionForm
from django.db.models import Q
from django.utils import timezone

def submission_dashboard(request):
    """
    Dashboard to display milk submissions with search and filter functionality.
    """
    # Start with all submissions, ordered by the most recent
    submissions = MilkSubmission.objects.select_related('supplier', 'supplier__district').order_by('-timestamp')
    
    # Get all districts to populate the filter dropdown
    districts = District.objects.all()

    # --- Search and Filter Logic ---

    # 1. Get the search query from the URL (?q=...)
    search_query = request.GET.get('q')
    if search_query:
        # Filter by supplier name OR supplier RF number
        submissions = submissions.filter(
            Q(supplier__name__icontains=search_query) | 
            Q(supplier__rf_no__icontains=search_query)
        )

    # 2. Get the district filter from the URL (?district=...)
    district_filter = request.GET.get('district')
    if district_filter:
        submissions = submissions.filter(supplier__district__id=district_filter)

    # 3. Get the date filter from the URL (?date_filter=...)
    date_filter = request.GET.get('date_filter')
    if date_filter == 'today':
        today = timezone.now().date()
        submissions = submissions.filter(timestamp__date=today)

    context = {
        'submissions': submissions,
        'districts': districts,
        # Pass the current filter values back to the template to keep them selected
        'selected_district': district_filter,
        'search_query': search_query,
    }
    return render(request, 'core/submission_dashboard.html', context)

# --- Keep your other views like supplier_detail here ---

def supplier_detail(request, pk):
    """
    Displays the detailed view for a single supplier.
    """
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = MilkSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.supplier = supplier
            submission.save()
            return redirect('supplier-detail', pk=supplier.pk)
    else:
        form = MilkSubmissionForm()
    submissions = supplier.submissions.all().order_by('-timestamp')
    context = {
        'supplier': supplier,
        'submissions': submissions,
        'form': form
    }
    return render(request, 'core/supplier_detail.html', context)

