import requests
from celery import shared_task
from .models import Lead, Form
from datetime import datetime

ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"  # Replace with your access token

@shared_task
def fetch_leads_task():
    """
    Task to fetch leads from Meta Graph API and save them to the database.
    """
    forms = Form.objects.all()  # Fetch all forms from the database
    for form in forms:
        url = f"https://graph.facebook.com/v17.0/{form.form_id}/leads?access_token={ACCESS_TOKEN}"
        response = requests.get(url)

        if response.status_code == 200:
            leads_data = response.json().get('data', [])
            for lead_data in leads_data:
                field_data = {field['name']: field['values'][0] for field in lead_data.get('field_data', [])}
                Lead.objects.update_or_create(
                    lead_id=lead_data['id'],
                    form=form,
                    defaults={
                        'full_name': field_data.get('full_name', 'Unknown'),
                        'email': field_data.get('email'),
                        'phone_number': field_data.get('phone_number'),
                        'created_time': datetime.strptime(lead_data['created_time'], '%Y-%m-%dT%H:%M:%S%z'),
                        'city': field_data.get('city', 'N/A'),
                    }
                )
        else:
            print(f"Error fetching leads for form {form.form_id}: {response.json()}")

    return "Lead fetching task completed."


# from celery import Celery
# from django_celery_beat.models import PeriodicTask, IntervalSchedule


# # Create an interval schedule for 10-second intervals
# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=10,
#     period=IntervalSchedule.SECONDS,
# )

# # Create the periodic task
# PeriodicTask.objects.get_or_create(
#     interval=schedule,
#     name='Fetch Meta Leads Every 10 Seconds',
#     task='crn.tasks.fetch_leads_task',
# )
