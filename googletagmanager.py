from django.conf import settings

def get_ga(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'GA_TAG': settings.GA_TAG}