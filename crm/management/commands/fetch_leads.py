from celery import shared_task
from crm.models import Page, Form, Lead
import requests
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"

@shared_task
def fetch_leads_task():
    """
    Fetch leads from Facebook API and save them to the database.
    """
    # Fetch pages from the database
    pages = Page.objects.all()
    for page in pages:
        # Fetch forms for the page
        forms_url = f"https://graph.facebook.com/v17.0/{page.page_id}/leadgen_forms?access_token={page.access_token}"
        forms_response = requests.get(forms_url)
        if forms_response.status_code != 200:
            continue

        for form_data in forms_response.json().get("data", []):
            form, _ = Form.objects.update_or_create(
                form_id=form_data["id"],
                defaults={"name": form_data.get("name", "Unnamed Form"), "page": page},
            )

            # Fetch leads for the form
            leads_url = f"https://graph.facebook.com/v17.0/{form.form_id}/leads?access_token={page.access_token}"
            while leads_url:
                leads_response = requests.get(leads_url)
                if leads_response.status_code != 200:
                    break

                for lead_data in leads_response.json().get("data", []):
                    # Parse field data
                    field_data = {field["name"]: field["values"][0] for field in lead_data.get("field_data", [])}

                    # Parse the created time
                    created_time = parse_datetime(lead_data.get("created_time"))

                    # Ensure created_time is timezone-aware
                    if created_time is not None and created_time.tzinfo is None:
                        created_time = make_aware(created_time)

                    # Save or update the lead in the database
                    Lead.objects.update_or_create(
                        lead_id=lead_data["id"],
                        form=form,
                        defaults={
                            'full_name': field_data.get("full_name", "N/A"),
                            'email': field_data.get("email", "N/A"),
                            'phone_number': field_data.get("phone_number", "N/A"),
                            'city': field_data.get("city", "N/A"),
                            'created_time': created_time,
                        }
                    )

                # Get the next page of leads
                leads_url = leads_response.json().get("paging", {}).get("next")




































# from django.core.management.base import BaseCommand
# import requests
# from crm.models import Page, Form, Lead
# import logging
# from django.db import transaction
# from datetime import datetime, timezone
# from datetime import timedelta
# from django.utils.timezone import make_aware
# # Access Token
# ACCESS_TOKEN = "EAAScaXpY5GsBO7mC9bZAYUGD2XQGwiZBiLSxyJZB5Ys881peHlDsSMuFjXC9hRChfMTfqf2Rrzq8hWeaDosHxZAZANONt9xcpJ4vt9JvCaqztDVqdGEX5khjZBPGvBJxqvzQkKzFnZA1wJ3omYH7164FjMP38fpyzdZC7ZBzStNgrSZB0CmWMmienCz0kI"

# # Logging configuration
# logging.basicConfig(
#     filename="fetch_leads.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)

# class Command(BaseCommand):
#     help = "Fetch new leads from Facebook API and save them to the database"

#     def handle(self, *args, **kwargs):
#         logger.info("Starting fetch_leads command...")

#         # List of pages to fetch
#         specified_page_names = [
#             "Anvestors trading software",
#             "Finoways Forex Signals Provider",
#             "Finoways Forex Trading signal"
#         ]
#         normalized_page_names = [name.strip().lower() for name in specified_page_names]

#         # Fetch Pages
#         pages_url = f"https://graph.facebook.com/v17.0/me/accounts?access_token={ACCESS_TOKEN}"
#         while pages_url:
#             try:
#                 pages_response = requests.get(pages_url, timeout=10)
#                 pages_response.raise_for_status()
#                 logger.info("Fetched pages successfully")
#             except Exception as e:
#                 logger.error(f"Error fetching pages: {e}")
#                 break

#             for page_data in pages_response.json().get("data", []):
#                 page_name = page_data.get("name", "").strip().lower()
#                 if page_name in normalized_page_names:
#                     page, _ = Page.objects.update_or_create(
#                         page_id=page_data["id"],
#                         defaults={
#                             "name": page_data.get("name"),
#                             "category": page_data.get("category", ""),
#                             "access_token": page_data.get("access_token", ""),
#                         }
#                     )
#                     logger.info(f"Processing Page: {page.name}")

#                     # Fetch Forms
#                     forms_url = f"https://graph.facebook.com/v17.0/{page.page_id}/leadgen_forms?access_token={page.access_token}"
#                     forms_response = requests.get(forms_url, timeout=10)
#                     for form_data in forms_response.json().get("data", []):
#                         form, _ = Form.objects.update_or_create(
#                             form_id=form_data["id"],
#                             defaults={"name": form_data.get("name", "Unnamed Form"), "page": page},
#                         )
#                         logger.info(f"Processing Form: {form.name}")

#                         # Fetch Leads Incrementally
#                         leads_url = f"https://graph.facebook.com/v17.0/{form.form_id}/leads?access_token={page.access_token}"
#                         leads_to_create = []
#                         last_fetched_time = Lead.objects.filter(form=form).order_by('-created_time').first()

#                         while leads_url:
#                             try:
#                                 leads_response = requests.get(leads_url, timeout=10)
#                                 leads_response.raise_for_status()
#                             except Exception as e:
#                                 logger.error(f"Error fetching leads from URL: {leads_url} | Error: {e}")
#                                 break

#                             for lead_data in leads_response.json().get("data", []):
#                                 # created_time = datetime.fromisoformat(lead_data.get("created_time")).replace(tzinfo=timezone.utc)
#                                 created_time = make_aware(datetime.fromisoformat(lead_data.get("created_time")))
                                
#                                 if last_fetched_time and created_time - timedelta(seconds=1) <= last_fetched_time.created_time:
#                                         continue
#                                 field_data = {field["name"]: field["values"][0] for field in lead_data.get("field_data", [])}
#                                 leads_to_create.append(Lead(
#                                     lead_id=lead_data["id"],
#                                     form=form,
#                                     full_name=field_data.get("full_name", "N/A"),
#                                     email=field_data.get("email", "N/A"),
#                                     phone_number=field_data.get("phone_number", "N/A"),
#                                     city=field_data.get("city", "N/A"),
#                                     created_time=created_time,
#                                 ))
#                             # leads_url = leads_response.json().get("paging", {}).get("next")
#                             leads_url = f"https://graph.facebook.com/v17.0/{form.form_id}/leads?access_token={page.access_token}&limit=100"

#                         # Bulk save leads
#                         if leads_to_create:
#                             logger.info(f"Attempting to save {len(leads_to_create)} leads for form: {form.name}")
#                             for lead in leads_to_create:
#                                 logger.info(f"Lead ID: {lead.lead_id}, Created Time: {lead.created_time}")

#                             for lead in leads_to_create:
#                                 Lead.objects.update_or_create(
#                                     lead_id=lead.lead_id,
#                                     defaults={
#                                         "form": lead.form,
#                                         "full_name": lead.full_name,
#                                         "email": lead.email,
#                                         "phone_number": lead.phone_number,
#                                         "city": lead.city,
#                                         "created_time": lead.created_time,
#                                         "active": True,  # Ensure active status is set
#                                     }
#                                 )
#                             logger.info(f"Processed {len(leads_to_create)} leads (created/updated) for form: {form.name}.")
#             pages_url = pages_response.json().get("paging", {}).get("next")

#         logger.info("Finished fetching and saving all new leads.")
