
#################################################

############################
##############################################################
from django.http import HttpResponseRedirect
from django.conf import settings
import urllib.parse
import uuid

def facebook_login2(request):
    # Generate a unique state value
    state = str(uuid.uuid4())  # Using UUID for better uniqueness

    # Save the state in the session
    request.session['state'] = state

    # Facebook OAuth URL
    base_url = 'https://www.facebook.com/v18.0/dialog/oauth'

    # Parameters for Facebook OAuth
    params = {
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
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
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        'redirect_uri': 'https://crm.joytilingtechnology.com/complete/facebook/',
        'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
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
            sub_admin = sub_admin.objects.get(sub_admin_id=suparadmin_id)
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
