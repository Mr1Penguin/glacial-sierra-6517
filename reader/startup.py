from django.apps import AppConfig
from .data_base import *
class Configuration(AppConfig):
    name = 'reader'
    def ready(self):
        activate_base()
        add_trigger()
        