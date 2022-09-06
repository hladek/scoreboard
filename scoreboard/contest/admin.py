from django.contrib import admin

from .models import Team,Contest,Run,Competition

admin.site.register(Team)
admin.site.register(Contest)
admin.site.register(Competition)
admin.site.register(Run)

# Register your models here.
