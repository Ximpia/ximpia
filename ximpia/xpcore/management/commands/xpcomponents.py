# Python

# django
from django.core.management.base import BaseCommand, CommandError

# ximpia
from ximpia.xpcore.util import get_class

class Command(BaseCommand):
    
    """
    
    Import Ximpia Components for Application
    
    ** Example **
    python manage.py xpcomponents myproject.myapp
    
    * ``app``:string : Application full path
    
    """
    
    args = '<app>'
    help = 'Imports ximpia components for application'    

    def handle(self, *args, **options):
        
        if len(args) != 1:
            raise CommandError("""You must include the full application path, like myproject.myapp
            
    python manage.py xpcomponents myproject.myapp
    
    * ``app``:string : Application full path""")
        app_path = args[0]
        get_class(app_path + '.components.AppReg')()
        get_class(app_path + '.components.SiteServiceReg')()
