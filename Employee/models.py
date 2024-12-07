from django.db import models
from crm.models import super_admin
import uuid


# Create your models here.
class EmployeeDT(models.Model):
    Employee_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
    Employee_admin_id = models.ForeignKey(super_admin, on_delete=models.CASCADE, related_name='employees')  # Changed to ForeignKey
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50,blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.TextField() 
   
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, blank=True)

    

    def __str__(self):
        return self.name