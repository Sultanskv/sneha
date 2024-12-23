from django.db import models
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

from crm.models import Customer,UserProfile,Page,Form,Lead


from django.utils import timezone
class head(models.Model):
    #admin_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    admin_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
 #   user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
    admin_name_first = models.CharField(max_length=50, blank=True, null=True)
    admin_name_last = models.CharField(max_length=50, blank=True, null=True)
    admin_email = models.EmailField(blank=True, null=True)
    admin_password = models.CharField(max_length=50,blank=True, null=True)
    admin_phone_number = models.CharField(max_length=15,blank=True, null=True)
    admin_verify_code = models.CharField(max_length=15,blank=True, null=True)

    is_staff= models.BooleanField(default=False)    

    def save(self, *args, **kwargs):
        # Generate a new unique ID if admin_id is not set
        if not self.admin_id:
            self.admin_id = self.generate_unique_id()
        super(head, self).save(*args, **kwargs)
    
    def generate_unique_id(self):
        # Generate and return a unique ID
        new_id = uuid.uuid4().hex[:8]
        # Ensure the ID is unique
        while head.objects.filter(admin_id=new_id).exists():
            new_id = uuid.uuid4().hex[:8]
        return new_id
    def __str__(self):
        return f"{self.admin_name_first} {self.admin_name_last} ({self.admin_id})"


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




# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(head, on_delete=models.CASCADE, related_name='profile')
    facebook_user_id = models.CharField(max_length=255, null=True, blank=True)
    facebook_access_token = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.facebook_user_id}"


from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils import timezone

class Page(models.Model):
    page_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField(default='default_token')

    def __str__(self):
        return self.name
    
class Form(models.Model):
    form_id = models.CharField(max_length=255, unique=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="forms")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, blank=True, null=True, default='INACTIVE')
    def __str__(self):
          return self.name

class Lead(models.Model):
    lead_id = models.CharField(max_length=255, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="leads", null=True)
    full_name = models.CharField(max_length=255, default='Unknown')
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)  # Uncomment if missing
    active = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.full_name