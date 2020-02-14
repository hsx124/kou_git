from django.conf import settings # import the settings file

def get_env_name(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ENV_NAME': settings.ENV_NAME}
