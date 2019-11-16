activator = 'some/path/to/activate_this.py'  # Looted from virtualenv; should not require modification, since it's defined relatively
with open(activator) as f:
    exec(f.read(), {'__file__': activator})
    
import sys
sys.path.insert(0, '/var/www/html/expLoRApi')

from explor import app as application