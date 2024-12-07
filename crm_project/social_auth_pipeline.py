# crm_project/social_auth_pipeline.py
from crm.models import UserProfile  # Make sure this imports your UserProfile model

def save_facebook_data(backend, user, response, *args, **kwargs):
    """
    This function is called during the authentication pipeline to store
    the Facebook user ID and access token into the UserProfile model.
    """
    # Get the Facebook user ID and access token from the response
    facebook_user_id = response.get('id')
    access_token = response.get('access_token')

    if facebook_user_id and access_token:
        # Get or create a UserProfile for the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Save the Facebook user ID and access token in the UserProfile model
        user_profile.facebook_user_id = facebook_user_id
        user_profile.facebook_access_token = access_token
        user_profile.save()

        print(f"Facebook user ID {facebook_user_id} and access token saved.")
    
    return None
