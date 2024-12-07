from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, Sale , super_admin
from .forms import CustomerForm, SaleForm ,LeadsForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import super_admin


'''======================== Admin and Subadmin login ======================================='''


def super_admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Authentication based on email and custom user model
        try:
            super_admin_instance = super_admin.objects.get(email=email)
            if super_admin_instance.password == password:
                if super_admin_instance.sub_admin == True:
                    request.session['sub_admin_id'] = super_admin_instance.super_admin_id
                else:    
                    request.session['super_admin_id'] = super_admin_instance.super_admin_id
                return redirect('dashboard')  # Redirect to a dashboard or desired page after login
            else:
                messages.error(request, 'Invalid password.')
        except super_admin.DoesNotExist:
            messages.error(request, 'Super Admin not found.')
    return render(request, 'login.html')

'''======================== Admin and Subadmin logout ======================================='''


def suparadmin_logout(request):
    if 'super_admin_id' in request.session:
        subadmin_id = request.session.get('super_admin_id')
        del request.session['super_admin_id']
    elif 'sub_admin_id' in request.session: 
        subadmin_id = request.session.get('sub_admin_id')
        del request.session['sub_admin_id']   
    return redirect('super_admin_login')

'''======================== dashboard ======================================='''


from datetime import date, timedelta
# @login_required
def dashboard(request):
    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
        customers = Customer.objects.all()
        sales = Sale.objects.all()
        total_lead = customers.count()
        tage_lead = Customer.objects.filter(active = True).count()
        untage_lead = Customer.objects.filter(active = False).count()
        untage_lead = Customer.objects.filter(active = False).count()
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        first_day_of_month = today.replace(day=1)
        if today.month == 12:
            last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        Newleads_today = Customer.objects.filter(date_created__date=today).count()

        # 2. Last 7 days ke leads filter karna
        last_week = Customer.objects.filter(date_created__date__gte=seven_days_ago).count()

        # 3. Current month ke leads filter karna
        this_month = Customer.objects.filter(date_created__date__range=(first_day_of_month, last_day_of_month)).count()

        source_fb = Customer.objects.filter(source="Facebook").count()
        source_self = Customer.objects.filter(source="Self").count()

        return render(request, 'dashboard.html', {'customers': customers,
                                                   'sales': sales,
                                                   'total_lead':total_lead,
                                                   'tage_lead':tage_lead,
                                                   'untage_lead':untage_lead,
                                                   'Newleads_today':Newleads_today,
                                                   'last_week':last_week,
                                                   'this_month':this_month,
                                                   'source_fb':source_fb,
                                                   'source_self':source_self
                                                   })
    elif 'sub_admin_id' in request.session: 
        subadmin_id = request.session.get('sub_admin_id')
        customers = Customer.objects.filter(admin_id = subadmin_id)
        sales = Sale.objects.filter(admin_id = subadmin_id)
        total_lead = customers.count()
        tage_lead = Customer.objects.filter(active = True,admin_id = subadmin_id).count()
        untage_lead = Customer.objects.filter(active = False,admin_id = subadmin_id).count()
        untage_lead = Customer.objects.filter(active = False,admin_id = subadmin_id).count()
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        first_day_of_month = today.replace(day=1)
        if today.month == 12:
            last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        Newleads_today = Customer.objects.filter(date_created__date=today,admin_id = subadmin_id).count()

        # 2. Last 7 days ke leads filter karna
        last_week = Customer.objects.filter(date_created__date__gte=seven_days_ago,admin_id = subadmin_id).count()

        # 3. Current month ke leads filter karna
        this_month = Customer.objects.filter(date_created__date__range=(first_day_of_month, last_day_of_month),admin_id = subadmin_id).count()

        source_fb = Customer.objects.filter(source="Facebook",admin_id = subadmin_id).count()
        source_self = Customer.objects.filter(source="Self",admin_id = subadmin_id).count()

        return render(request, 'dashboard.html', {'customers': customers,
                                                   'sales': sales,
                                                   'total_lead':total_lead,
                                                   'tage_lead':tage_lead,
                                                   'untage_lead':untage_lead,
                                                   'Newleads_today':Newleads_today,
                                                   'last_week':last_week,
                                                   'this_month':this_month,
                                                   'source_fb':source_fb,
                                                   'source_self':source_self
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

def all_leads(request):
    # Extract filter and pagination parameters from the request
    filter_query = request.GET.get('filter', '')  # Filtering query
    page_number = request.GET.get('page', 1)  # Current page number

    # Check user session and retrieve leads based on user role
    if 'super_admin_id' in request.session:
        leads_query = Customer.objects.all()
    elif 'sub_admin_id' in request.session:
        subadmin_id = request.session.get('sub_admin_id')
        leads_query = Customer.objects.filter(admin_id=subadmin_id)
    else:
        messages.error(request, 'Login Required.')
        return redirect('/')

    # Apply filtering if a filter query is provided
    if filter_query:
        leads_query = leads_query.filter(name__icontains=filter_query)

    # Paginate the results
    paginator = Paginator(leads_query, 50)  # 50 leads per page
    leads = paginator.get_page(page_number)

    # Render the template with context
    return render(request, 'all_leads.html', {
        'leads': leads,
        'filter_query': filter_query,
    })


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


'''======================== daAll sells to templet ======================================='''



def all_sale(request):
    
    
    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
        sales = Sale.objects.all()
        return render(request, 'all_sale.html', {'sales': sales})
    
    elif 'sub_admin_id' in request.session:
        subadmin_id = request.session.get('sub_admin_id')
       
        sales = Sale.objects.filter(admin_id = subadmin_id)
        return render(request, 'all_sale.html', {'sales': sales})
    else:
        messages.error(request, 'Login Required.')
        return redirect('/') 

'''======================== Add sells ======================================='''


def add_sale(request):
    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
    elif 'sub_admin_id' in request.session:
        suparadmin_id = request.session.get('sub_admin_id')
    else :
        suparadmin_id = None    
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            customer = form.save(commit=False)
           
            customer.admin_id = suparadmin_id
            customer.save()
            messages.success(request, 'Sale record created successfully!')
            return redirect('all_sale')  # Redirect to a list of sales after saving
        else:
            messages.error(request, 'Failed to create sale record. Please check the form.')
    else:
        form = SaleForm()
    
    return render(request, 'add_sale.html', {'form': form})

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
  
    employees = EmployeeDT.objects.filter(Employee_admin_id =admin_instance )
    
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
from social_django.utils import psa
from django.conf import settings
from django.contrib import messages

from django.shortcuts import render, redirect
import requests
from social_django.utils import psa
from django.conf import settings
from django.contrib import messages
from social_django.models import UserSocialAuth



'''this prgent working'''


def facebook_login(request):
    """
    Handle Facebook login and retrieve access token.
    This function ensures that even if the user has already authenticated via Facebook,
    the connection can be re-established and the access token can be stored for future use.
    """
    print("Facebook login initiated")
    try:
     
        # Use filter instead of get to handle multiple records
        user_social_auth = request.user.social_auth.filter(provider='facebook').first()  # get the first one
        if not user_social_auth:
            raise ValueError("No Facebook account linked.")
        
        access_token = user_social_auth.extra_data['access_token']
        print("Access token retrieved:", access_token)

        # Store the access token in session for future API requests
        request.session['facebook_access_token'] = access_token
        print("Access token stored in session.")
    except AttributeError:
        print("No access token found after login")
        messages.error(request, 'Unable to retrieve access token. Please try again.')
        return redirect(settings.LOGIN_URL)
    except ValueError as e:
        print(f"Error: {e}")
        messages.error(request, str(e))
        return redirect(settings.LOGIN_URL)

    # Redirect to Facebook pages view to show pages
    return redirect('facebook_pages')




def facebook_pages(request):
    print("Fetching Facebook pages after login")

    # Fetch the user's Facebook access token from session
    access_token = request.session.get('facebook_access_token')
    
    if not access_token:
        print("No access token provided")
        messages.error(request, "No access token provided")
        return redirect('super_admin_login')

    print("Access token retrieved:", access_token)

    # Fetch the pages the user manages
    response = requests.get(
        'https://graph.facebook.com/me/accounts',
        params={'access_token': access_token}
    )
    
    if response.status_code != 200:
        print("Error fetching pages:", response.text)
        messages.error(request, 'Error fetching Facebook pages.')
        return render(request, 'error.html', {'message': 'Error fetching pages'})

    pages = response.json().get('data', [])
    
    if not pages:
        print("No pages found for this user")
        return render(request, 'error.html', {'message': 'No pages found'})

    # Save page access tokens in session for later use
    pages_with_tokens = []
    for page in pages:
        pages_with_tokens.append({
            'id': page['id'],
            'name': page['name'],
            'access_token': page['access_token']  # This is the Page Access Token
        })
    
    # Store the pages with their access tokens in session
    request.session['facebook_pages'] = pages_with_tokens
    print("Pages fetched and stored in session:", pages_with_tokens)
    
    return render(request, 'select_page.html', {'pages': pages_with_tokens})


def select_form(request, page_id):
    print(f"Fetching forms for page {page_id}")

    # Retrieve the stored pages with their access tokens from session
    pages = request.session.get('facebook_pages', [])
    
    # Find the page access token for the selected page
    page_access_token = None
    for page in pages:
        if page['id'] == page_id:
            page_access_token = page['access_token']
            break
    
    if not page_access_token:
        print("No page access token found for the selected page")
        messages.error(request, 'No access token for the selected page. Please login again.')
        return redirect('facebook_login')

    print("Page access token retrieved:", page_access_token)

    # Fetch the forms from the selected page
    response = requests.get(
        f'https://graph.facebook.com/{page_id}/leadgen_forms',
        params={'access_token': page_access_token}
    )
    
    if response.status_code != 200:
        print("Error fetching forms:", response.text)
        return render(request, 'error.html', {'message': f'Error fetching forms for page {page_id}'})

    forms = response.json().get('data', [])

    if not forms:
        print(f"No forms found for page {page_id}")
        return render(request, 'error.html', {'message': f'No forms found for page {page_id}'})
    
    print("Forms fetched:", forms)
    
    return render(request, 'select_form.html', {'forms': forms, 'page_id': page_id})


def fetch_leads(request, form_id):
    print(f"Fetching leads for form {form_id}")

    access_token = request.session.get('facebook_access_token')

    if not access_token:
        print("No access token provided")
        messages.error(request, 'No access token found. Please login again.')
        return redirect('facebook_login')

    print("Access token retrieved:", access_token)

    # Fetch leads from the selected form
    response = requests.get(
        f'https://graph.facebook.com/{form_id}/leads',
        params={'access_token': access_token}
    )

    if response.status_code != 200:
        print("Error fetching leads:", response.text)
        return render(request, 'error.html', {'message': f'Error fetching leads for form {form_id}'})

    leads = response.json().get('data', [])

    if not leads:
        print(f"No leads found for form {form_id}")
        return render(request, 'error.html', {'message': f'No leads found for form {form_id}'})

    print("Leads fetched:", leads)
  
    # suparadmin_id = request.session.get('super_admin_id')
    # # Process and save leads (using Customer model)
    # for lead in leads:
    #     print(f"Processing lead: {lead}")
    #     try:
    #         full_name = lead['field_data'][0]['values'][0]
    #         email = lead['field_data'][1]['values'][0]
    #         phone_number = lead['field_data'][2]['values'][0]

    #         Customer.objects.update_or_create(
    #             email=email,
    #             defaults={
    #                 'admin_id':suparadmin_id,
    #                 'name': full_name,
    #                 'phone': phone_number,
    #                 'address': '',
    #                 'created_by': 'Facebook',
    #             }
    #         )
    #     except IndexError as e:
    #         print(f"Error processing lead: {lead}, Error: {e}")
    #         continue



    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
    elif 'sub_admin_id' in request.session:
        suparadmin_id = request.session.get('sub_admin_id')
    else:
        suparadmin_id = None
    # Process and save leads (using Customer model)
    for lead in leads:
        print(f"Processing lead: {lead}")
        try:
            # Map field data to a dictionary for easy access
            field_map = {field['name']: field['values'][0] for field in lead['field_data']}
            
            # Get values using keys
            lead_id = lead['id']  # Extract the lead id
            full_name = field_map.get('FULL_NAME', 'Unknown Name')  # Default to 'Unknown Name' if not found
            email = field_map.get('EMAIL', 'unknown@example.com')  # Default to 'unknown@example.com' if not found
            phone_number = field_map.get('PHONE', 'Unknown Phone')  # Default to 'Unknown Phone' if not found
           
            
            # Save or update customer data
            Customer.objects.update_or_create(
                email=email,
                defaults={
                    'admin_id': suparadmin_id,
                    'name': full_name,
                    'phone': phone_number,
                    'facebook_id':lead_id,
                    'address': '',
                    'created_by': 'Facebook',
                }
            )
        except Exception as e:
            print(f"Error processing lead: {lead}, Error: {e}")
            continue


    return render(request, 'leads.html', {'leads': leads})




##############################################################

#################################################################
from django.http import HttpResponseRedirect
from django.conf import settings
import urllib.parse
import uuid

def facebook_login2(request):
    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
        sub_admin = super_admin.objects.get(super_admin_id=suparadmin_id)
    elif 'sub_admin_id' in request.session:
        suparadmin_id = request.session.get('sub_admin_id')
        sub_admin = super_admin.objects.get(super_admin_id=suparadmin_id)
    else:
        sub_admin = None
    # Generate a unique state value
    print(sub_admin.facebook_app_id)
    print(sub_admin.facebook_app_secret)
    state = str(uuid.uuid4())  # Using UUID for better uniqueness
 
    # Save the state in the session
    request.session['state'] = state

    # Facebook OAuth URL
    base_url = 'https://www.facebook.com/v18.0/dialog/oauth'

    # Parameters for Facebook OAuth
    params = {
        'client_id': sub_admin.facebook_app_id,
        'redirect_uri': 'https://crm.joytilingtechnology.com/complete/facebook/',
        'state': state,
        'scope': 'email,public_profile,pages_show_list,pages_read_engagement,leads_retrieval,pages_manage_ads',
    }

    # Generate the OAuth URL with query parameters
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return HttpResponseRedirect(url)



import requests
from django.http import JsonResponse
from .models import UserProfile
from django.shortcuts import redirect
from django.conf import settings

def facebook_complete(request):
    # Retrieve the state from session and request
    session_state = request.session.get('state')
    received_state = request.GET.get('state')
    if 'super_admin_id' in request.session:
        suparadmin_id = request.session.get('super_admin_id')
        sub_admin = super_admin.objects.get(super_admin_id=suparadmin_id)
        print(sub_admin)
    elif 'sub_admin_id' in request.session:
        suparadmin_id = request.session.get('sub_admin_id')
        sub_admin = super_admin.objects.get(super_admin_id=suparadmin_id)
        print(sub_admin)

    else:
        sub_admin = None
 
    if sub_admin == None:
        messages.error(request, 'nor admin')
        return redirect('/')
    # Validate the state to prevent CSRF
    if session_state != received_state:
        return JsonResponse({'error': 'State parameter mismatch'}, status=400)

    # Retrieve the authorization code
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided by Facebook'}, status=400)

    # Step 1: Exchange the code for an access token
    token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
    params = {
        'client_id': sub_admin.facebook_app_id,
        'redirect_uri': 'https://crm.joytilingtechnology.com/complete/facebook/',
        'client_secret': sub_admin.facebook_app_secret,
        'code': code,
    }
    response = requests.get(token_url, params=params)
    token_data = response.json()

    if 'access_token' not in token_data:
        return JsonResponse({'error': 'Unable to retrieve access token'}, status=400)

    access_token = token_data['access_token']

    # Step 2: Fetch Facebook user details using the access token
    user_info_url = 'https://graph.facebook.com/me'
    user_info_params = {
        'access_token': access_token,
        'fields': 'id,email,name',
    }
    user_info_response = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_response.json()
    facebook_user_id = user_info.get('id')
    namme = user_info.get('name')
    email = user_info.get('email')
    access_token = access_token 
    print('facebook_user_id' , facebook_user_id ,f'/n access_token = {access_token}')
    # return JsonResponse({
    #     'id': user_info.get('id'),
    #     'name': user_info.get('name'),
    #     'email': user_info.get('email'),
    #     'access_token': access_token,
    # })
   
    try:
        if 'super_admin_id' in request.session:
            suparadmin_id = request.session.get('super_admin_id')
            first_super_admin = super_admin.objects.get(super_admin_id=suparadmin_id)
            user_to_assign = first_super_admin
        elif 'sub_admin_id' in request.session:
            suparadmin_id = request.session.get('sub_admin_id')
            sub_admin = super_admin.objects.get(super_admin_id=suparadmin_id)
            user_to_assign = sub_admin
        else:
            user_to_assign = None

        if not user_to_assign:
            print("No valid user (super_admin or sub_admin) found in session.")
            raise ValueError("No valid user (super_admin or sub_admin) found in session.")
           
        # Get or create the UserProfile
        profile, created = UserProfile.objects.get_or_create(
            facebook_user_id=facebook_user_id,
            defaults={
                'user': user_to_assign,
                'facebook_access_token': access_token,
            }
        )

        if not created:
            # Update the existing profile with new access token
            profile.facebook_access_token = access_token
            profile.save()

        # Store Facebook details in session
        request.session['facebook_user_id'] = facebook_user_id
        request.session['facebook_access_token'] = access_token

    except ValueError as e:
        print(f"Error: {e}")
        messages.error(request, str(e))
        return redirect(settings.LOGIN_URL)

    # Redirect to another page after successful login
    return redirect('facebook_pages')  # Replace with your desired URL



import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

def upload_customers(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        
        # Get the admin ID from the session
        if 'super_admin_id' in request.session:
            admin_id = request.session.get('super_admin_id')
        elif 'sub_admin_id' in request.session:
            admin_id = request.session.get('sub_admin_id')
        else:
            messages.error(request, "Admin ID not found in session.")
            return redirect('upload_customers')
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Ensure the required columns are present
            required_columns = ['name', 'mobile', 'email', 'address']
            if not all(col in df.columns for col in required_columns):
                messages.error(request, f"Excel file must contain columns: {', '.join(required_columns)}")
                return redirect('upload_customers')

            # Loop through the rows and create Customer objects
            for _, row in df.iterrows():
                Customer.objects.create(
                    admin_id=admin_id,
                    name=row['name'],
                    phone=row['mobile'],
                    email=row['email'],
                    address=row['address'],
                    source = 'self'
                )
            
            messages.success(request, "Customers uploaded successfully!")
        except Exception as e:
            messages.error(request, f"Error processing the file: {e}")
            return redirect('upload_customers')

    return render(request, 'upload_customers.html')
