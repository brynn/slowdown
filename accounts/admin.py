from django.contrib import admin
from accounts.models import UserProfile, Twitter, Instagram, Item

admin.site.register(UserProfile)
admin.site.register(Twitter)
admin.site.register(Instagram)
admin.site.register(Item)