from django.contrib import admin

# Register your models here.

from users.models import Participant
# from django.contrib.auth.admin import UserAdmin


# admin.site.register(Participant)

# @admin.register(Participant)
# class CustomizeAdminPanel(UserAdmin):
#     model = Participant
#     fieldsets = (
#         (None,{"fields": ("username", "password")}),
#         ("Personal Info",{"fields": ("first_name","last_name","email","phone_number","participantPhoto")}),
#         ("Permissions",{"fields":("is_active","is_staff","is_superuser","groups","user_permissions")}),
#         ("Important Date",{"fields": ("last_login","date_joined")})
#     )



#chat gpt style:
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    # Columns to show in the admin list view
    list_display = (
        'get_username', 
        'get_email', 
        'get_first_name', 
        'get_last_name', 
        'phone_number',
        'is_active',
        'is_staff'
    )
    
    # Fields you can search by
    search_fields = ('user__username',)

    # Filters on the right sidebar
    list_filter = ('user__is_staff', 'user__is_superuser', 'user__is_active')

    # Make fields clickable for editing
    readonly_fields = ('user',)

    # Fieldsets when editing an object
    fieldsets = (
        ("Participant Info", {"fields": ("user", "participantPhoto", "phone_number")}),
    )

    # --- Helper methods to access related User fields ---
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"
    get_username.admin_order_field = 'user__username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
    get_email.admin_order_field = 'user__email'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "First Name"
    get_first_name.admin_order_field = 'user__first_name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = "Last Name"
    get_last_name.admin_order_field = 'user__last_name'

    def is_active(self, obj):
        return obj.user.is_active
    is_active.boolean = True
    is_active.admin_order_field = 'user__is_active'

    def is_staff(self, obj):
        return obj.user.is_staff
    is_staff.boolean = True
    is_staff.admin_order_field = 'user__is_staff'







