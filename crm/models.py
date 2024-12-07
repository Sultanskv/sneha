from django.db import models
from django.contrib.auth.models import User
import uuid

class super_admin(models.Model):
    super_admin_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
    sub_admin = models.BooleanField(default=True,blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50,blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.TextField() 
   
    created_at = models.DateTimeField(auto_now_add=True)

    facebook_app_id = models.CharField(max_length=555, null=True, blank=True)
    facebook_app_secret = models.CharField(max_length=555, null=True, blank=True)
    

    def __str__(self):
        return self.super_admin_id


class Customer(models.Model):
    admin_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_by = models.CharField(max_length=100,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    LEAD_SOURCES = (
        ('organic_search', 'Organic Search'),
        ('google_ad', 'Google Ad'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('Self', 'Self'),
    )

    MEDIA_CHOICES = (
        ('sms', 'SMS'),
        ('facebook', 'Facebook'),
        ('phone_call', 'Phone call')
    )

    # first_name = models.CharField(max_length=25, blank=True)
    # last_name = models.CharField(max_length=25, blank=True)
    age = models.IntegerField(default=0,blank=True, null=True)

    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    source = models.CharField(
        choices=LEAD_SOURCES, 
        max_length=50,
        blank=True,
        help_text="Where Lead found us",
        default=LEAD_SOURCES[3][0]
    )
    preferred_medium = models.CharField(
        choices=MEDIA_CHOICES, 
        max_length=50,
        default=MEDIA_CHOICES[1][0],
        help_text="Lead's preferred social media for communication"
    )

    active = models.BooleanField(default=False, blank=True)
    status_CHOICES = [
        ('NEW', 'New Lead'),          # New Lead
        ('APPROVED', 'Approved'),    # Approved Lead
        ('REJECTED', 'Rejected'),    # Rejected Lead
        ('PENDING', 'Pending'),      # Pending Review
        ('FOLLOWUP', 'Follow-Up')    # Follow-Up Required
    ]
    
    # Create the status field
    status = models.CharField(
        choices=status_CHOICES,        # Add the choices here
        max_length=50,                # Maximum length of the field
        default='NEW',                # Default value
        help_text="Lead's status for tracking and communication"
    )

    profile_picture = models.ImageField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    admin_id = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return f"{self.product} - {self.amount}"


# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(super_admin, on_delete=models.CASCADE, related_name='profile')
    facebook_user_id = models.CharField(max_length=255, null=True, blank=True)
    facebook_access_token = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.facebook_user_id}"


