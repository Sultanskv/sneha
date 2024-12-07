from django.shortcuts import render , HttpResponse , redirect
from .models import EmployeeDT
from django.contrib import messages
from crm.models import *
# Create your views here.
def Employee_login(request):
    if 'msg' in request.GET:
        msg = request.GET['msg']
        messages.error(request, msg) 
    else:
        msg = None 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            employee_dt = EmployeeDT.objects.get(email = email)
            if password == employee_dt.password:
                if employee_dt.active == True:
                    request.session['Employee_id'] = employee_dt.Employee_id
                    return redirect('Dashboard')
                else:
                    messages.error(request, 'Employee not active.')  
            else:
                messages.error(request, 'Invalid password.')  
        except:
            messages.error(request, 'Employee not found')    
        
    return render(request ,'Employee/login.html')

def Employee_logout(request):
    if 'Employee_id' in request.session:
        del request.session['Employee_id']
  
    return redirect('employee_login')
    
def Dashboard(request):
 #   return HttpResponse('test')
    if 'Employee_id' not in request.session:
        return redirect('employee_login')
    return render(request, 'Employee/Dashboard.html')

# def employee_leads(request):
#     if 'Employee_id' not in request.session:
#         return redirect('employee_login')
#     # admin_instance = get_object_or_404(super_admin, super_admin_id=admin_id)
#     Employee_id = request.session.get('Employee_id')
#     empdt = EmployeeDT.objects.get(Employee_id =  Employee_id)
#     print(empdt.name,empdt.Employee_admin_id)
#     leads = Customer.objects.filter(admin_id = empdt.Employee_admin_id)
#     return render(request, 'Employee/Employee_leads.html', {'leads': leads,})


from django.core.paginator import Paginator


def employee_leads(request):
    if 'Employee_id' not in request.session:
        return redirect('employee_login')
    Employee_id = request.session.get('Employee_id')
    empdt = EmployeeDT.objects.get(Employee_id =  Employee_id)
    print(empdt.name,empdt.Employee_admin_id)
    leads_query = Customer.objects.filter(admin_id = empdt.Employee_admin_id)
    # Extract filter and pagination parameters from the request
    filter_query = request.GET.get('filter', '')  # Filtering query
    page_number = request.GET.get('page', 1)  # Current page number

   
    # Apply filtering if a filter query is provided
    if filter_query:
        leads_query = leads_query.filter(name__icontains=filter_query)

    # Paginate the results
    paginator = Paginator(leads_query, 50)  # 50 leads per page
    leads = paginator.get_page(page_number)

    # Render the template with context
    return render(request, 'Employee/Employee_leads.html', {
        'leads': leads,
        'filter_query': filter_query,
    })


import openpyxl


def export_leads_to_excel_emp(request):
    if 'Employee_id' not in request.session:
        return redirect('employee_login')
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

    if 'Employee_id' in request.session:
        Employee_id = request.session.get('Employee_id')
        empdt = EmployeeDT.objects.get(Employee_id =  Employee_id)
        customers = Customer.objects.filter(admin_id = empdt.Employee_admin_id)
  
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






import hashlib
import time
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib import messages


'''
path('forgot-password/', views.forgot_password, name='forgot_password'),
path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
'''
# Custom token generate karne ka function
def generate_token(user):
    timestamp = str(int(time.time()))
    unique_string = f"{user.pk}{user.email}{timestamp}"
    token = hashlib.sha256(unique_string.encode()).hexdigest()
    return token, timestamp

# Forgot Password View
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # User ko email ke base par search karein
            user = EmployeeDT.objects.get(email=email)

            # Custom token aur UID generate karein
            token, timestamp = generate_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            # Reset link create karein
            reset_link = request.build_absolute_uri(f"/employee/reset-password/{uid}/{token}/")
            print(reset_link)

            # Email bhejne ka code
            subject = 'Password Reset Request'
            message = f'Click the link below to reset your password:\n\n{reset_link}'
            from_email = 'noreply@example.com'
            send_mail(subject, message, from_email, [email])

            # Success message
       
            return redirect('/employee/?msg=Password reset email sent successfully.')
        except EmployeeDT.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forgot_password')

    return render(request, 'Employee/forgot_password.html')

# Reset Password View
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = EmployeeDT.objects.get(pk=uid)

        # Token ko validate karein (timestamp expire hone ke liye)
        if request.method == "POST":
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'Employee/reset_password.html', {'uidb64': uidb64, 'token': token})

            # Password set karein
            user.password = new_password
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('/employee/')

        return render(request, 'Employee/reset_password.html', {'uidb64': uidb64, 'token': token})
    except EmployeeDT.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect('forgot_password')