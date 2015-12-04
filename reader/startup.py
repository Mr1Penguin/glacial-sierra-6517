from django.apps import AppConfig
from .data_base import *
import sys
class Configuration(AppConfig):
    name = 'reader'
    def ready(self):
    	if sys.argv[1] != 'migrate':
        	activate_base()
        	add_trigger()
        