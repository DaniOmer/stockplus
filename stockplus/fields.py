from django.conf import settings

def RichTextField(*args, **kwargs):
    if "ckeditor" in settings.INSTALLED_APPS:
        from ckeditor.fields import RichTextField
        return RichTextField(*args, **kwargs)
    elif "django_ckeditor_5" in settings.INSTALLED_APPS:
        from django_ckeditor_5.fields import CKEditor5Field
        return CKEditor5Field(*args, **kwargs)
    else:
        from django.db.models import TextField
        return TextField(*args, **kwargs)