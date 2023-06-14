from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _
class CenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'center'
    verbose_name= _("Center and Staff")
