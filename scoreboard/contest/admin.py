from django.contrib import admin
from .models import Run, Competition, Contest,Result, Team
from django.forms import TextInput, Textarea, NumberInput
import django.db


#admin.site.register(Team)


class Admin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }

class Inline(admin.TabularInline):
    show_change_link = True
    formfield_overrides = {
        django.db.models.TextField: {'widget': TextInput(attrs={'style':'width: 10em'})},
        django.db.models.CharField: {'widget': TextInput(attrs={'style':'width: 10em'})},
        django.db.models.FloatField: {'widget': NumberInput(attrs={'style':'width: 3em'})},
        django.db.models.IntegerField: {'widget': NumberInput(attrs={'style':'width: 3em'})},
    }
    extra = 1


class ResultInline(Inline):
    model = Result

class RunInline(Inline):
    model = Run

class CompetitionAdmin(Admin):
    inlines = [ResultInline,RunInline]

class TeamInline(Inline):
    model = Team

class ContestAdmin(Admin):
    inlines = [TeamInline]

admin.site.register(Contest,ContestAdmin)
admin.site.register(Competition,CompetitionAdmin)
#admin.site.register(Contest)
#admin.site.register(Team)

# Register your models here.
