from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.contrib.admin import SimpleListFilter

from django.contrib.gis import admin

admin.site.unregister(User)

def verified(modeladmin, request, queryset):
        queryset.update(isverified=True)
verified.short_description = "Verified all selected"
def searchverified(modeladmin, request, queryset):
        return queryset.filter(isverified=True)
searchverified.short_description = "search verified"
def unverified(modeladmin, request, queryset):
        queryset.update(isverified=False)
unverified.short_description = "unerified all selected"

class VerifiedFilter(SimpleListFilter):
    title = 'verified'
    parameter_name = 'isverified'

    def lookups(self, request, model_admin):
        return((2,'All'), (1, 'Yes'), (0, 'No'))
    def queryset(self, request, queryset):
        if self.value() is None:
            self.used_parameters[self.parameter_name] = 0
        else:
            self.used_parameters[self.parameter_name] = int(self.value())
        if self.value() == 2:
            return queryset
        return queryset.filter(isverified=self.value())

class MapActionAdmin(admin.GeoModelAdmin):
    model = MapAction
    search_fields = ['title','content']
    list_display = ['title','content','firstPicture','location']
    #readonly_fields = ['uuid','slug',]

admin.site.register(MapAction, MapActionAdmin)

    
class TitleAdminForm(forms.ModelForm):
    class Meta:
        widgets = { 'title': forms.TextInput(attrs={'size': 80})}

class UserAdminWithEmail(admin.ModelAdmin):
    model = Action
    list_display = ('title','createDate', 'modified','author','isverified')
    #list_filter =('isverified')
    fields = ('title','showimage','firstPicture','content','startDate', 'endDate')
    readonly_fields = ['showimage']
    search_fields = ['title','author__username','isverified']
    actions = [verified, unverified, searchverified]
    list_filter = [VerifiedFilter]
    form = TitleAdminForm
   # inlines = [LocationImages]
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

class UserAdminForUser(UserAdmin):
    model = User
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2')
            },
        ),
    )

admin.site.register(User, UserAdminForUser)
admin.site.register(Action, UserAdminWithEmail)
admin.site.register(CalendarAction)
#admin.site.register(UserProfile)
#admin.site.register(Notification)
#admin.site.register(Comment)
#admin.site.register(Activity)
admin.site.register(ActionRefLink)
admin.site.register(ActionPicture)
#admin.site.register(Invitation)


        

