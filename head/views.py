from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Customer,  Page, Lead, Form ,head
from crm.models import Customer,Page,Form,Lead
from datetime import date, timedelta
from django.utils import timezone

from .models import head

import requests
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomerForm, SaleForm ,LeadsForm
'''======================== Head (Main Admin) Login ======================================='''

def head_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            head_instance = head.objects.get(admin_email=email)  # Updated field name
            if head_instance.admin_password == password:  # Updated field name
                request.session['head_id'] = head_instance.admin_id  # Updated field name
                return redirect('head_dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, 'Invalid password.')
        except head.DoesNotExist:
            messages.error(request, 'Head user not found.')
    return render(request, 'head/login.html')

'''======================== Logout ======================================='''

def head_logout(request):
    if 'head_id' in request.session:
        del request.session['head_id']
    return redirect('head_login')

'''======================== Dashboard ======================================='''

def head_dashboard(request):
    if 'head_id' in request.session:
        head_id = request.session.get('head_id')
        customers = Customer.objects.filter(created_by=head_id)  # Updated field name
        total_lead = customers.count()
        tage_lead = customers.filter(active=True).count()
        untage_lead = customers.filter(active=False).count()
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        first_day_of_month = today.replace(day=1)
        if today.month == 12:
            last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        new_leads_today = customers.filter(date_created__date=today).count()
        last_week = customers.filter(date_created__date__gte=seven_days_ago).count()
        this_month = customers.filter(date_created__date__range=(first_day_of_month, last_day_of_month)).count()

        source_fb = customers.filter(source="Facebook").count()
        source_self = customers.filter(source="Self").count()

        return render(request, 'head/dashboard.html', {
            'customers': customers,
            'total_lead': total_lead,
            'tage_lead': tage_lead,
            'untage_lead': untage_lead,
            'new_leads_today': new_leads_today,
            'last_week': last_week,
            'this_month': this_month,
            'source_fb': source_fb,
            'source_self': source_self
        })
    else:
        messages.error(request, 'Login Required.')
        return redirect('head_login')

'''======================== Add Leads ======================================='''

from .models import head  # Ensure the correct import

def head_add_customer(request):
    if 'head_id' in request.session:
        head_id = request.session.get('head_id')  # Get the head_id from the session
        head_instance = head.objects.get(admin_id=head_id)  # Retrieve the head instance

        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.created_by = head_instance.admin_id  # Use the admin_id of the head instance
                customer.admin_id = head_instance.admin_id
                customer.save()
                return redirect('head_dashboard')
        else:
            form = CustomerForm()

        return render(request, 'head/add_customer.html', {'form': form})

    else:
        messages.error(request, 'Login Required.')
        return redirect('head_login')

'''======================== Add Leads link method  ======================================='''

def head_create_lead(request):
    if request.method == 'POST':
        form = LeadsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead successfully created!')
            return redirect('head_create_lead')
        else:
            messages.error(request, 'Form is not valid, please check the inputs.')
    else:
        form = LeadsForm()
    return render(request, 'head/create_lead.html', {'form': form})


from django.http import JsonResponse
from django.utils import timezone
import openpyxl
from django.http import HttpResponse



'''======================== Update Leads starts ======================================='''


# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Customer

def head_update_active_status(request):
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

def head_export_leads_to_excel(request):
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

    if 'head_id' in request.session:
        head_id = request.session.get('head_id')
        customers = Customer.objects.all()
    elif 'head_id' in request.session:
        head_id = request.session.get('head_id')
        customers = Customer.objects.filter(admin_id = head_id)
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

def head_privacy_policy(request):
    return render(request, 'head/privacy_policy.html')

def head_terms_of_service(request):
    return render(request, 'head/terms_of_service.html')
'''======================== Employe List to templet ======================================='''


from django.shortcuts import render, get_object_or_404, redirect
from Employee.models import EmployeeDT
from Employee.forms import EmployeeForm
import random
import string
from django.core.mail import send_mail

# List Employees
def head_employee_list(request):
    if 'head_id' in request.session:
        head_id = request.session.get('head_id')
    elif 'head_id' in request.session:
        head_id = request.session.get('head_id')
    else:
        admin_id = None
    head_instance = get_object_or_404(head_id, head_id=head_id)
  
    employees = EmployeeDT.objects.filter(Employee_admin_id =head_instance )
    
    return render(request, 'head/employee_list.html', {'employees': employees})

# Add Employee
def head_generate_random_password(length=8):
    """Generate a random alphanumeric password of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def head_employee_add(request):
    # Get the admin ID from the session
    if 'head_id' in request.session:
        head_id = request.session.get('head_id')
    elif 'head_id' in request.session:
        head_id = request.session.get('head_id')
    else:
        head_id = None

    if not head_id:
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
                admin_instance = get_object_or_404(head_id, head_id=head_id)
                # Generate a random password
                random_password = head_generate_random_password()
                # Assign values to the employee
                employee.Employee_head_id = admin_instance
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

                return redirect('head/employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'head/employee_form.html', {'form': form, 'action': 'Add Employee'})

# Edit Employee
def head_employee_edit(request, pk):
    employee = get_object_or_404(EmployeeDT, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('admin/employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'admin/employee_form.html', {'form': form, 'action': 'Edit Employee'})


#########################################################################################################3
'''================================================================================================'''

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Page, Lead, Form
from datetime import datetime
import requests

ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"

def head_fetch_pages(request):
    """
    Fetch all pages for the head admin and save them to the database.
    """
    url = f"https://graph.facebook.com/v17.0/me/accounts?access_token={ACCESS_TOKEN}"
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            messages.error(request, "Failed to fetch pages. Please check your API token and permissions.")
            return render(request, "head/head_pages.html", {"pages": []})

        data = response.json()
        for page_data in data.get("data", []):
            Page.objects.update_or_create(
                page_id=page_data["id"],
                defaults={
                    "name": page_data.get("name", "Unnamed Page"),
                    "category": page_data.get("category", ""),
                    "access_token": page_data.get("access_token", ""),
                }
            )
        url = data.get("paging", {}).get("next")  # Handle pagination

    pages = Page.objects.all()
    return render(request, "head/head_pages.html", {"pages": pages})

def head_fetch_forms_for_page(request, page_id):
    """
    Fetch forms associated with a specific page and save them to the database.
    """
    page = get_object_or_404(Page, page_id=page_id)
    url = f"https://graph.facebook.com/v17.0/{page_id}/leadgen_forms?access_token={page.access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        forms_data = response.json().get('data', [])
        for form_data in forms_data:
            Form.objects.update_or_create(
                form_id=form_data['id'],
                defaults={
                    'name': form_data.get('name', 'Unnamed Form'),
                    'page': page,
                    'status': form_data.get('status', 'ACTIVE'),
                }
            )
        forms = Form.objects.filter(page=page)
    else:
        error_message = response.json().get('error', {}).get('message', 'Failed to fetch forms.')
        messages.error(request, error_message)
        forms = []

    return render(request, 'head/head_forms.html', {'forms': forms, 'page': page})

from django.shortcuts import render
from .models import Lead, Page, Form
from datetime import datetime
from django.utils.timezone import now
import requests

ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"


from django.shortcuts import render
from .models import Lead, Page, Form
from datetime import datetime
from django.utils.timezone import now
import requests

ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"


def fetch_all_leads_from_api():
    """
    Fetch all leads directly from Facebook Graph API for all pages and forms,
    and save them to the database.
    """
    pages_url = f"https://graph.facebook.com/v17.0/me/accounts?access_token={ACCESS_TOKEN}"
    while pages_url:
        response = requests.get(pages_url)
        if response.status_code != 200:
            print("Error fetching pages:", response.json())
            break

        pages_data = response.json()
        for page_data in pages_data.get("data", []):
            page, _ = Page.objects.get_or_create(
                page_id=page_data["id"],
                defaults={
                    "name": page_data.get("name", "Unnamed Page"),
                    "category": page_data.get("category", ""),
                    "access_token": page_data.get("access_token", ""),
                }
            )

            # Fetch forms for the page
            forms_url = f"https://graph.facebook.com/v17.0/{page.page_id}/leadgen_forms?access_token={page.access_token}"
            forms_response = requests.get(forms_url)
            if forms_response.status_code != 200:
                print(f"Error fetching forms for page {page.page_id}: {forms_response.json()}")
                continue

            forms_data = forms_response.json().get('data', [])
            for form_data in forms_data:
                form, created = Form.objects.get_or_create(
                    form_id=form_data['id'],
                    defaults={
                        'name': form_data.get('name', 'Unnamed Form'),
                        'page': page,
                        'status': form_data.get('status', 'ACTIVE'),
                    }
                )
                if not created:
                    form.name = form_data.get('name', 'Unnamed Form')
                    form.status = form_data.get('status', 'ACTIVE')
                    form.save()

                # Fetch leads for the form
                leads_url = f"https://graph.facebook.com/v17.0/{form.form_id}/leads?access_token={page.access_token}"
                while leads_url:
                    leads_response = requests.get(leads_url)
                    if leads_response.status_code != 200:
                        print(f"Error fetching leads for form {form.form_id}: {leads_response.json()}")
                        break

                    leads_data = leads_response.json().get('data', [])
                    for lead_data in leads_data:
                        field_data = {field['name']: field['values'][0] for field in lead_data.get('field_data', [])}
                        lead, created = Lead.objects.get_or_create(
                            lead_id=lead_data['id'],
                            form=form,
                            defaults={
                                'full_name': field_data.get('full_name', 'N/A'),
                                'email': field_data.get('email', 'N/A'),
                                'phone_number': field_data.get('phone_number', 'N/A'),
                                'city': field_data.get('city', None),
                                'created_time': lead_data.get('created_time'),
                            }
                        )
                        if not created:
                            lead.full_name = field_data.get('full_name', 'N/A')
                            lead.email = field_data.get('email', 'N/A')
                            lead.phone_number = field_data.get('phone_number', 'N/A')
                            lead.city = field_data.get('city', None)
                            lead.created_time = lead_data.get('created_time')
                            lead.save()

                    # Handle pagination for leads
                    leads_url = leads_response.json().get('paging', {}).get('next')

        # Handle pagination for pages
        pages_url = pages_data.get("paging", {}).get("next")


def head_all_leads(request):
    """
    Fetch all leads across all forms and pages for the head admin, including today's leads.
    """
    # Automatically fetch all new leads
    fetch_all_leads_from_api()

    # Get filters from the request
    filter_date = request.GET.get('filter_date', '')  # Date filter
    filter_city = request.GET.get('filter_city', '')  # City filter

    # Fetch all leads, ordered by the latest created_time
    leads = Lead.objects.all().order_by('-created_time')

    # Apply filters if provided
    if filter_date:
        try:
            # Parse the date filter into a datetime object
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            leads = leads.filter(created_time__date=filter_date_obj)
        except ValueError:
            pass  # Ignore invalid date formats

    if filter_city:
        leads = leads.filter(city__icontains=filter_city)

    # Get today's date for highlighting today's leads
    today_date = now().date()

    # Pass leads and filters to the template
    return render(request, 'head/head_all_leads.html', {
        'leads': leads,
        'filter_date': filter_date,
        'filter_city': filter_city,
        'today_date': today_date,
    })


# def assign_lead_to_user(request):
#     if request.method == "POST":
#         lead_id = request.POST.get("lead_id")
#         user_id = request.POST.get("user_id")

#         try:
#             lead = Lead.objects.get(id=lead_id)
#             user = User.objects.get(id=user_id)
#             lead.assigned_to = user
#             lead.save()
#             return JsonResponse({"message": f"Lead successfully assigned to {user.username}."})
#         except (Lead.DoesNotExist, User.DoesNotExist):
#             return JsonResponse({"message": "Lead or User not found."}, status=404)

#     return JsonResponse({"message": "Invalid request."}, status=400)


# def auto_assign_leads(request):
#     """
#     Automatically assigns 2 leads for today to each user.
#     """
#     users = User.objects.all()
#     today_leads = Lead.objects.filter(created_time__date=now().date(), assigned_to__isnull=True)

#     for user in users:
#         unassigned_leads = today_leads.filter(assigned_to__isnull=True)[:2]
#         for lead in unassigned_leads:
#             lead.assigned_to = user
#             lead.save()

#     return JsonResponse({"message": "Leads automatically assigned for today."})