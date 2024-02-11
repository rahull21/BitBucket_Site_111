from django.apps import AppConfig




class BitBucketsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BitBucket_site'

   
    def ready(self):
        import BitBucket_site.signals 
