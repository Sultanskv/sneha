from django.db import models
# from django.contrib.auth.models import User
import uuid
# from django.db import models
# from crm.models import Page  # Import the Page model
# from django.db import models
# from django.contrib.auth.models import User

# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.conf import settings
# from django.utils import timezone


class super_admin(models.Model):

    # ROLE_CHOICES = [
    #     ('subadmin', 'Sub-Admin'),
    #     ('admin', 'Admin'),
    # ]

    # role = models.CharField(choices=ROLE_CHOICES, default='subadmin', max_length=20)
    allowed_pages = models.ManyToManyField('Page', blank=True, related_name='allowed_superadmins')
    super_admin_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
    sub_admin = models.BooleanField(default=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Use a string reference instead of direct import
    # allowed_pages = models.ManyToManyField('crm.Page', blank=True, related_name='allowed_subadmins')

    def __str__(self):
        return f"{self.name} ({self.super_admin_id})"



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


class UserProfile(models.Model):
    user = models.OneToOneField(super_admin, on_delete=models.CASCADE, related_name='profile')
    facebook_user_id = models.CharField(max_length=255, null=True, blank=True)
    facebook_access_token = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.facebook_user_id}"



class Page(models.Model):
    page_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField(default='default_token')
    visible_to = models.ManyToManyField(super_admin, related_name="pages_visible", blank=True)
    
    def __str__(self):
        return self.name

    
class Form(models.Model):
    form_id = models.CharField(max_length=255, unique=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="forms")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, blank=True, null=True, default='INACTIVE')
    def __str__(self):
          return self.name

from django.contrib.auth.models import User

class Lead(models.Model):
    STATUS_CHOICES = [
        ("Not Assigned", "Not Assigned"),
        ("Assigned", "Assigned"),
    ]
    lead_id = models.CharField(max_length=255, unique=True,db_index=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="leads", null=True)
    full_name = models.CharField(max_length=255, default='Unknown')
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    # created_time = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="leads")
    created_time = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        ordering = ['-created_time']  # Default sorting: latest first
        db_table = "crm_lead"