from django.contrib import admin
from .models import User, Bike, Issue, Borrowing

# Register your models here.

admin.site.register(User)
admin.site.register(Bike)
admin.site.register(Issue)
admin.site.register(Borrowing)

filter_horizontal = ('groups', 'user_permissions',)