from django.contrib import admin

from .models import Team,Contest,Run,Competition,Result

#admin.site.register(Team)

#class TeamContestInline(admin.TabularInline):
#    model = Team
#    show_change_link = True
#    extra = 3

#class ContestAdmin(admin.ModelAdmin):
#    inlines = [TeamContestInline]

#admin.site.register(Contest,ContestAdmin)
admin.site.register(Contest)
admin.site.register(Result)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(Run)

# Register your models here.
