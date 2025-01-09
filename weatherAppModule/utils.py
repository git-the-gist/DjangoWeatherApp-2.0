
from django.urls import reverse

def error_redirect_url(): # redirect to 404 error page
    return reverse('error_404')

def error_location_url(): # redirect to location error page
    return reverse('error_location')

