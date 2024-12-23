from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer,  super_admin
from .forms import CustomerForm, SaleForm ,LeadsForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import super_admin
from .models import Lead
from django.utils import timezone


'''======================== Admin and Subadmin login ======================================='''


def super_admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = super_admin.objects.get(email=email)
            if admin.password == password:
                request.session['super_admin_id'] = admin.super_admin_id
                request.session['welcome_message'] = True  # Set flag for welcome message
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, 'Invalid password.')
        except super_admin.DoesNotExist:
            messages.error(request, 'Admin not found.')

    return render(request, 'login.html')
'''======================== Admin and Subadmin logout ======================================='''


def suparadmin_logout(request):
    if 'super_admin_id' in request.session:
        subadmin_id = request.session.get('super_admin_id')
        del request.session['super_admin_id']
        # request.session['bye_message'] = True  # Set flag for goodbye message
    elif 'sub_admin_id' in request.session: 
        subadmin_id = request.session.get('sub_admin_id')
        del request.session['sub_admin_id']   
        # request.session['bye_message'] = True  # Set flag for goodbye message
    return redirect('super_admin_login')

'''======================== dashboard ======================================='''


from datetime import date, timedelta
# @login_required
def dashboard(request):
    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
        leads = Lead.objects.all()  # Ensure this variable is used consistently
        total_lead = leads.count()
        tage_lead = leads.filter(form__isnull=False).count()
        untage_lead = leads.filter(form__isnull=True).count()

        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        first_day_of_month = today.replace(day=1)
        if today.month == 12:
            last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        # Newleads_today = leads.filter(created_time__date=timezone.now().date()).count()
        Newleads_today = leads.filter(created_time__date=today).count()
        last_week = leads.filter(created_time__date__gte=seven_days_ago).count()
        this_month = leads.filter(created_time__date__range=(first_day_of_month, last_day_of_month)).count()

        source_fb = leads.filter(form__name='Facebook').count()
        source_self = leads.filter(form__name='Self').count()
        # Fetch the latest lead
        latest_lead = leads.order_by('-created_time').first()

        return render(request, 'dashboard.html', {
            'leads': leads,  # Ensure this matches the variable defined above
            'total_lead': total_lead,
            'tage_lead': tage_lead,
            'untage_lead': untage_lead,
            'Newleads_today': Newleads_today,
            'last_week': last_week,
            'this_month': this_month,
            'source_fb': source_fb,
            'source_self': source_self,
            'latest_lead': latest_lead, 
        })

    elif 'sub_admin_id' in request.session:
        subadmin_id = request.session.get('sub_admin_id')
        leads = Lead.objects.filter(form__admin_id=subadmin_id)
        total_lead = leads.count()
        tage_lead = leads.filter(form__isnull=False).count()
        untage_lead = leads.filter(form__isnull=True).count()

        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        first_day_of_month = today.replace(day=1)
        if today.month == 12:
            last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        Newleads_today = leads.filter(created_time__date=today).count()
        last_week = leads.filter(created_time_date_gte=seven_days_ago).count()
        this_month = leads.filter(created_time_date_range=(first_day_of_month, last_day_of_month)).count()

        source_fb = leads.filter(form__name='Facebook').count()
        source_self = leads.filter(form__name='Self').count()
        # Fetch the latest lead
        latest_lead = leads.order_by('-created_time').first()
        return render(request, 'dashboard.html', {
            'leads': leads,
            'total_lead': total_lead,
            'tage_lead': tage_lead,
            'untage_lead': untage_lead,
            'Newleads_today': Newleads_today,
            'last_week': last_week,
            'this_month': this_month,
            'source_fb': source_fb,
            'source_self': source_self,
            'latest_lead': latest_lead,
        })

    else:
        messages.error(request, 'Login Required.')
        return redirect('/')
'''======================== Add Leads ======================================='''


from django.contrib.auth.models import User
def add_customer(request):
    if 'super_admin_id' in request.session or 'sub_admin_id' in request.session:
        if 'super_admin_id' in request.session:
            suparadmin_id = request.session.get('super_admin_id')
        else:
            suparadmin_id = request.session.get('sub_admin_id')
       
        supaeradmin = super_admin.objects.get(super_admin_id = suparadmin_id)
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                print(supaeradmin.super_admin_id)
                customer.created_by = supaeradmin.super_admin_id
                customer.admin_id = supaeradmin.super_admin_id
                customer.save()
                return redirect('dashboard')
        else:
            form = CustomerForm()
        return render(request, 'add_customer.html', {'form': form})
    else:
        messages.error(request, 'Login Required.')
        return redirect('/')
    
'''======================== Add Leads link method ======================================='''


def create_lead(request):
    if request.method == 'POST':
        form = LeadsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead successfully created!')
            return redirect('create_lead')
        else:
            messages.error(request, 'Form is not valid, please check the inputs.')
    else:
        form = LeadsForm()
    return render(request, 'create_lead.html', {'form': form})


from django.http import JsonResponse
from django.utils import timezone
import openpyxl
from django.http import HttpResponse

# def all_leads(request):
        
    
#     if 'super_admin_id' in request.session:
#         suparadmin_id = request.session.get('super_admin_id')
      
#         leads = Customer.objects.all()
#         return render(request, 'all_leads.html', {'leads': leads,})
#     elif 'sub_admin_id' in request.session:
#         subadmin_id = request.session.get('sub_admin_id')
#         leads = Customer.objects.filter(admin_id = subadmin_id)
#         return render(request, 'all_leads.html', {'leads': leads,})
#     else:
        
#         messages.error(request, 'Login Required.')
#         return redirect('/')

'''======================== All Leads to templets ======================================='''


from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

# def all_leads(request):
#     # Extract filter and pagination parameters from the request
#     filter_query = request.GET.get('filter', '')  # Filtering query
#     page_number = request.GET.get('page', 1)  # Current page number

#     # Check user session and retrieve leads based on user role
#     if 'super_admin_id' in request.session:
#         leads_query = Customer.objects.all()
#     elif 'sub_admin_id' in request.session:
#         subadmin_id = request.session.get('sub_admin_id')
#         leads_query = Customer.objects.filter(admin_id=subadmin_id)
#     else:
#         messages.error(request, 'Login Required.')
#         return redirect('/')

#     # Apply filtering if a filter query is provided
#     if filter_query:
#         leads_query = leads_query.filter(name__icontains=filter_query)

#     # Paginate the results
#     paginator = Paginator(leads_query, 50)  # 50 leads per page
#     leads = paginator.get_page(page_number)

#     # Render the template with context
#     return render(request, 'all_leads.html', {
#         'leads': leads,
#         'filter_query': filter_query,
#     })


'''======================== Update Leads starts ======================================='''


# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Customer

def update_active_status(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        field = request.POST.get('field')  # 'active' or 'status'
        value = request.POST.get('value')
        
        customer = get_object_or_404(Customer, id=customer_id)
        
        # Update the specific field
        if field == 'active':
            customer.active = (value == 'true')  # Convert string to boolean
        elif field == 'status':
            customer.status = value
        # customer.date_updated = date
        customer.save()
        return JsonResponse({"success": True, "message": "Customer updated successfully."})
    return JsonResponse({"success": False, "message": "Invalid request."})

'''======================== Imports Leads ======================================='''
        
def export_leads_to_excel(request):
    # Create a workbook and an active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Customers'

    # Define the column headers
    columns = [
        'ID', 'Name', 'Email', 'Phone', 'Address', 'Created By', 'Created At',
        'Age', 'Facebook ID', 'Phone Number', 'Source', 'Preferred Medium',
        'Active','status', 'Profile Picture', 'Date Created', 'Date Updated'
    ]
    worksheet.append(columns)

    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
        customers = Customer.objects.all()
    elif 'sub_admin_id' in request.session:
        subadmin_id = request.session.get('sub_admin_id')
        customers = Customer.objects.filter(admin_id = subadmin_id)
    # Fetch all customers and write their data to the worksheet
    

    for customer in customers:
        row = [
            customer.id,
            customer.name,
            customer.email,
            customer.phone,
            customer.address,
            customer.created_by,
            customer.created_at.strftime('%Y-%m-%d %H:%M') if customer.created_at else '',
            customer.age,
            customer.facebook_id,
            customer.phone_number,
            customer.source,
            customer.preferred_medium,
            'Yes' if customer.active else 'No',
            customer.status,
            customer.profile_picture.url if customer.profile_picture else '',
            
            customer.date_created.strftime('%Y-%m-%d %H:%M') if customer.date_created else '',
            customer.date_updated.strftime('%Y-%m-%d %H:%M') if customer.date_updated else ''
        ]
        worksheet.append(row)

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=customers.xlsx'
    workbook.save(response)

    return response

'''======================== Policy & service ======================================='''

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

'''======================== Employe List to templet ======================================='''


from django.shortcuts import render, get_object_or_404, redirect
from Employee.models import EmployeeDT
from Employee.forms import EmployeeForm
import random
import string
from django.core.mail import send_mail

# List Employees
def employee_list(request):
    if 'super_admin_id' in request.session:
        admin_id = request.session.get('super_admin_id')
    elif 'sub_admin_id' in request.session:
        admin_id = request.session.get('sub_admin_id')
    else:
        admin_id = None
    admin_instance = get_object_or_404(super_admin, super_admin_id=admin_id)
  
    employees = EmployeeDT.objects.all()
    
    return render(request, 'employee_list.html', {'employees': employees})

# Add Employee
def generate_random_password(length=8):
    """Generate a random alphanumeric password of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def employee_add(request):
    # Get the admin ID from the session
    if 'super_admin_id' in request.session:
        admin_id = request.session.get('super_admin_id')
    elif 'sub_admin_id' in request.session:
        admin_id = request.session.get('sub_admin_id')
    else:
        admin_id = None

    if not admin_id:
        return redirect('employee_list')

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Check if an employee with the same email already exists
            email = form.cleaned_data.get('email')
            if EmployeeDT.objects.filter(email=email).exists():
                messages.error(request, f"An account with the email {email} already exists.")
            else:
                # Save the form without committing to the database
                employee = form.save(commit=False)
                # Fetch the related super_admin object using the ID
                admin_instance = get_object_or_404(super_admin, super_admin_id=admin_id)
                # Generate a random password
                random_password = generate_random_password()
                # Assign values to the employee
                employee.Employee_admin_id = admin_instance
                employee.password = random_password
                # Save the employee instance
                employee.save()

                # Send an email with the password and website link
                subject = "Welcome to Our Platform"
                message = (
                    f"Hello {employee.name},\n\n"
                    f"Your account has been created successfully.\n\n"
                    f"Login Details:\n"
                    f"Email: {employee.email}\n"
                    f"Password: {random_password}\n\n"
                    f"Please log in at: http://127.0.0.1:8000/employee\n\n"
                    f"Thank you!"
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [employee.email]
                try:
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, f"Employee {employee.name} added successfully and email sent.")
                except Exception as e:
                    messages.warning(request, f"Employee added successfully, but email could not be sent. Error: {e}")

                return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employee_form.html', {'form': form, 'action': 'Add Employee'})

# Edit Employee
def employee_edit(request, pk):
    employee = get_object_or_404(EmployeeDT, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form, 'action': 'Edit Employee'})



#####################################################################################################

'''================================================================================================'''

from django.shortcuts import render, redirect
import requests
# from social_django.utils import psa
from django.conf import settings
from django.contrib import messages
# from social_django.models import UserSocialAuth
from .models import Page,  Lead , Form
from django.shortcuts import  get_object_or_404
from datetime import datetime
# from .models import Page, Lead
import json

ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"



from django.shortcuts import render, redirect, get_object_or_404
from .models import super_admin
from crm.models import Page



def fetch_pages(request):
    """
    Fetch specified pages associated with the user and save them to the database.
    """
    specified_page_names = [
        "Anvestors trading software",
        "Finoways Forex Signals Provider",
        "Finoways Forex Trading signal"
    ]

    # Normalize specified page names
    normalized_page_names = [name.strip().lower() for name in specified_page_names]

    # Fetch all pages from the API
    url = f"https://graph.facebook.com/v17.0/me/accounts?access_token={ACCESS_TOKEN}"
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching pages:", response.json())
            messages.error(request, "Failed to fetch pages. Please check API token and permissions.")
            return render(request, "pages.html", {"pages": []})

        data = response.json()
        for page_data in data.get("data", []):
            page_name = page_data.get("name").strip().lower()  # Normalize fetched name
            if page_name in normalized_page_names:
                Page.objects.update_or_create(
                    page_id=page_data["id"],
                    defaults={
                        "name": page_data.get("name").strip(),  # Save the clean name
                        "category": page_data.get("category", ""),
                        "access_token": page_data.get("access_token", ""),
                    },
                )
                print(f"Saved Page: {page_data.get('name').strip()}")
            else:
                print(f"Page Not Matched: {page_data.get('name').strip()}")

        # Pagination handling
        url = data.get("paging", {}).get("next")

    # Query only the specified pages
    pages = Page.objects.filter(name__in=specified_page_names)
    print(f"Pages for Template: {[page.name for page in pages]}")  # Debug the query result
    return render(request, "pages.html", {"pages": pages})



def fetch_forms_for_page(request, page_id):
    """
    Fetch forms associated with a specific page and save them to the database.
    """
    page = get_object_or_404(Page, page_id=page_id)

    # Fetch forms for the page
    url = f"https://graph.facebook.com/v17.0/{page_id}/leadgen_forms?access_token={page.access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        forms_data = response.json().get('data', [])
        for form_data in forms_data:
            Form.objects.update_or_create(
                form_id=form_data['id'],  # Save the form_id from API
                defaults={
                    'name': form_data.get('name', 'Unnamed Form'),
                    'page': page,
                    'status': form_data.get('status', 'ACTIVE'),
                }
            )
        # Refresh the forms from the database
        forms = Form.objects.filter(page=page)
    else:
        error_message = response.json().get('error', {}).get('message', 'Failed to fetch forms.')
        return render(request, 'error.html', {'message': error_message})

    return render(request, 'forms.html', {'forms': forms, 'page': page})



from django.shortcuts import render, get_object_or_404
from .models import Lead, Form

def fetch_leads_from_db(request, form_id):
    """
    Fetch leads from the MySQL database for the given form ID.
    Replace form names dynamically for the specified forms.
    """
    # Define the form name mappings
    form_name_mapping = {
        "forex11/12/2024, 16:24": "Forex Domestic Ad",
        "Capture basic customer information 10/12/2024": "Malasia/Singapore Ad",
        "Franchise Ad Leads-copy": "Partnership Ad",
        "Forex signal-copy": "Gulf Forex Ad"
    }

    # Fetch the form
    form = get_object_or_404(Form, form_id=form_id)

    # Replace the form name if it exists in the mapping
    original_name = form.name
    form.name = form_name_mapping.get(form.name, form.name)

    # Query the Lead table to fetch leads for the given form
    leads = Lead.objects.filter(form=form).order_by('-created_time')  # Order by latest leads

    # Debugging: Print leads and form name mapping
    print(f"Fetched {len(leads)} leads for form {original_name} renamed to {form.name}")

    # Pass the leads and updated form to the template
    return render(request, 'leads.html', {'leads': leads, 'form': form})

 
def fetch_leads_for_form(request, form_id):
    form = get_object_or_404(Form, form_id=form_id)

    # Fetch leads from Facebook API
    url = f"https://graph.facebook.com/v17.0/{form_id}/leads?access_token={form.page.access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        leads_data = response.json().get('data', [])
        for lead_data in leads_data:
            # Print the raw lead data for debugging
            print("Raw Lead Data:", lead_data)

            field_data = {field['name']: field['values'][0] for field in lead_data.get('field_data', [])}
            print("Field Data Processed:", field_data)  # Debug: Check processed field data

            Lead.objects.update_or_create(
                lead_id=lead_data['id'],
                form=form,
                defaults={
                    'full_name': field_data.get('full_name', 'Unknown'),
                    'email': field_data.get('email', None),
                    'phone_number': field_data.get('phone_number', None),
                    'created_time': lead_data.get('created_time'),
                    'city': field_data.get('city', None),  # Ensure this field is mapped
                }
            )

        leads = Lead.objects.filter(form=form)
        return render(request, 'leads.html', {'leads': leads, 'form': form})
    else:
        error_message = response.json().get('error', {}).get('message', 'Failed to fetch leads.')
        return render(request, 'error.html', {'message': error_message})


from django.http import JsonResponse
from .tasks import fetch_leads_task

def manual_fetch_leads(request):
    """
    Trigger manual fetch of leads.
    """
    fetch_leads_task.delay()  # Run asynchronously
    return JsonResponse({"message": "Lead fetching initiated. Check logs for status."})


from django.utils import timezone
# from django.utils.timezone import localtime

# from django.utils.timezone import localtime, now

def fetch_and_save_all_leads():
    """
    Fetch pages, forms, and leads from Facebook API and save them to the database.
    """
    specified_page_names = [
        "Anvestors trading software",
        "Finoways Forex Signals Provider",
        "Finoways Forex Trading signal"
    ]
    normalized_page_names = [name.strip().lower() for name in specified_page_names]

    # Fetch all pages
    pages_url = f"https://graph.facebook.com/v17.0/me/accounts?access_token={ACCESS_TOKEN}"
    while pages_url:
        pages_response = requests.get(pages_url)
        if pages_response.status_code != 200:
            print("Error fetching pages:", pages_response.json())
            return

        for page_data in pages_response.json().get("data", []):
            page_name = page_data.get("name", "").strip().lower()
            if page_name in normalized_page_names:
                page, _ = Page.objects.update_or_create(
                    page_id=page_data["id"],
                    defaults={
                        "name": page_data["name"].strip(),
                        "category": page_data.get("category", ""),
                        "access_token": page_data.get("access_token", ""),
                    }
                )
                # Fetch forms for the matched page
                forms_url = f"https://graph.facebook.com/v17.0/{page.page_id}/leadgen_forms?access_token={page.access_token}"
                forms_response = requests.get(forms_url)
                for form_data in forms_response.json().get('data', []):
                    form, _ = Form.objects.update_or_create(
                        form_id=form_data['id'],
                        defaults={'name': form_data.get('name', 'Unnamed Form'), 'page': page}
                    )
                    # Fetch leads for the form
                    leads_url = f"https://graph.facebook.com/v17.0/{form.form_id}/leads?access_token={page.access_token}"
                    while leads_url:
                        leads_response = requests.get(leads_url)
                        if leads_response.status_code != 200:
                            print(f"Error fetching leads: {leads_response.json()}")
                            break
                        for lead_data in leads_response.json().get('data', []):
                            field_data = {field['name']: field['values'][0] for field in lead_data.get('field_data', [])}
                            Lead.objects.update_or_create(
                                lead_id=lead_data['id'],
                                form=form,
                                defaults={
                                    'full_name': field_data.get('full_name', 'N/A'),
                                    'email': field_data.get('email', 'N/A'),
                                    'phone_number': field_data.get('phone_number', 'N/A'),
                                    'city': field_data.get('city', 'N/A'),
                                    'created_time': lead_data.get('created_time'),
                                }
                            )
                        leads_url = leads_response.json().get('paging', {}).get('next')

        pages_url = pages_response.json().get("paging", {}).get("next")

from django.shortcuts import render
from crm.models import Lead

def all_leads(request):
    """
    Display all leads from the database, ordered by the latest created_time.
    """
    leads = Lead.objects.all().order_by('-created_time')
    return render(request, 'leads.html', {'leads': leads})



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Lead

@csrf_exempt
def update_lead_status(request, lead_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            status = data.get("status")
            lead = Lead.objects.get(id=lead_id)
            lead.status = status  # Assuming you have a 'status' field in the model
            lead.save()
            return JsonResponse({"success": True})
        except Lead.DoesNotExist:
            return JsonResponse({"error": "Lead not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# # #========================= Notification  ========================================== 
from django.http import JsonResponse
from .models import Lead

def get_latest_lead(request):
    """
    Fetch the latest lead from the Lead model and return it as JSON response.
    """
    try:
        latest_lead = Lead.objects.latest('created_time')  # Fetch the latest lead based on creation time
        data = {
            'full_name': latest_lead.full_name,
            'email': latest_lead.email,
            'phone_number': latest_lead.phone_number,
            'created_time': latest_lead.created_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse(data)
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'No leads found.'}, status=404)




from django.shortcuts import render
from .models import Lead  # Replace with your actual model name

def old_leads(request):
    # Fetch all leads from the database
    leads = Lead.objects.all()
    return render(request, 'old_leads.html', {'leads': leads})

from django.http import JsonResponse
from django.utils.timezone import now
from .models import Lead

def fetch_new_leads(request):
    """
    Return all leads created after the last timestamp sent by the frontend.
    """
    last_fetched = request.GET.get('last_fetched')  # Timestamp sent from frontend

    try:
        if last_fetched:
            new_leads = Lead.objects.filter(created_time__gt=last_fetched).order_by('created_time')
        else:
            new_leads = Lead.objects.all().order_by('created_time')[:10]  # Fetch latest 10 leads initially

        leads_data = [
            {
                'id': lead.id,
                'full_name': lead.full_name or "N/A",
                'email': lead.email or "N/A",
                'phone_number': lead.phone_number or "N/A",
                'city': lead.city or "N/A",
                'created_time': lead.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for lead in new_leads
        ]

        return JsonResponse({'leads': leads_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



from django.core.cache import cache
from django.http import JsonResponse

def test_cache(request):
    # Set a key in Redis
    cache.set('greeting', 'Hello from Redis!', timeout=60)

    # Get the key from Redis
    greeting = cache.get('greeting')

    return JsonResponse({'message': greeting})




from django.http import JsonResponse

def clear_session_flag(request):
    flag = request.GET.get('flag')
    if flag in request.session:
        del request.session[flag]
    return JsonResponse({"status": "success"})



































#  today = timezone.now().date()
#         seven_days_ago = today - timedelta(days=7)
#         first_day_of_month = today.replace(day=1)
#         if today.month == 12:
#             last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
#         else:
#             last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

#         Newleads_today = leads.filter(created_time__date=today).count()
#         last_week = leads.filter(created_time__date__gte=seven_days_ago).count()
#         this_month = leads.filter(created_time__date__range=(first_day_of_month, last_day_of_month)).count()
























# @login_required
# def calls_lead_changelist(request):
#     """
#     Displays a list of leads with pagination and optional filtering.
#     """
#     leads = Lead.objects.all()  # Fetch all leads from the database

#     # Filtering by page (if needed)
#     page_id = request.GET.get('page_id')
#     if page_id:
#         leads = leads.filter(page__page_id=page_id)

#     # Optional date range filtering
#     from_date = request.GET.get('from_date')
#     to_date = request.GET.get('to_date')
#     if from_date:
#         leads = leads.filter(created_time__date__gte=from_date)
#     if to_date:
#         leads = leads.filter(created_time__date__lte=to_date)

#     # Pagination
#     paginator = Paginator(leads, 25)  # Display 25 leads per page
#     page_number = request.GET.get('page')
#     paginated_leads = paginator.get_page(page_number)

#     # Render the template
#     return render(request, 'leads_changelist.html', {
#         'leads': paginated_leads,
#         'page_id': page_id,
#         'from_date': from_date,
#         'to_date': to_date,
#     })
























# def fetch_page_forms(request, page_id):
#     url = f"https://graph.facebook.com/v17.0/{page_id}/leadgen_forms?access_token={ACCESS_TOKEN}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         forms = response.json().get('data', [])
#         print(f"Forms: {forms}")  # Debugging: Print available forms
#         return render(request, 'forms.html', {'forms': forms})

#     error_message = response.json().get('error', {}).get('message', "Unable to fetch forms.")
#     print(f"Error fetching forms: {error_message}")
#     return render(request, 'forms.html', {'error': error_message})

# def fetch_forms(request, page_id):
#     url = f"https://graph.facebook.com/v17.0/{page_id}/leadgen_forms?access_token={ACCESS_TOKEN}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         forms = response.json().get('data', [])
#         return render(request, 'forms.html', {'forms': forms})

#     error_message = response.json().get('error', {}).get('message', "Unable to fetch forms.")
#     return render(request, 'forms.html', {'error': error_message})
























# def fetch_leads(request, form_id):
#     url = f"https://graph.facebook.com/v17.0/{form_id}/leads?access_token={ACCESS_token}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         leads_data = response.json().get('data', [])
#         processed_leads = []

#         for lead in leads_data:
#             # Extract field values from the field_data array
#             field_data = {field['name']: field['values'][0] for field in lead.get('field_data', [])}
#             full_name = field_data.get('full_name', 'N/A')
#             email = field_data.get('email', 'N/A')
#             phone_number = field_data.get('phone_number', 'N/A')
#             city = field_data.get('city', 'N/A')

#             # Save lead to the database
#             Lead.objects.update_or_create(
#                 lead_id=lead['id'],
#                 defaults={
#                     'full_name': full_name,
#                     'email': email,
#                     'phone_number': phone_number,
#                     'city': city,
#                     'created_time': lead['created_time']
#                 }
#             )

#             # Add to processed leads for rendering
#             processed_leads.append({
#                 'lead_id': lead['id'],
#                 'full_name': full_name,
#                 'email': email,
#                 'phone_number': phone_number,
#                 'city': city,
#                 'created_time': lead['created_time']
#             })

#         # Pass the processed leads to the template
#         return render(request, 'leads.html', {'leads': processed_leads})

#     error_message = response.json().get('error', {}).get('message', "Failed to fetch leads.")
#     return render(request, 'leads.html', {'error': error_message})