#! /usr/bin/python3.6

#activate_this = '/var/www/html/expLoRApi/env/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))
    
import sys
sys.path.append('/var/www/html/expLoRApi')
from explor import app as application
