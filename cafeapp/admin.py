from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from cafeapp.models import Item, Order, OrderItem, Table

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['phone', 'fullname','is_staff']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('fullname',)}),
        ('Permissions', {'fields': ('staff','admin','is_active','trustworthy')}),
        ('Images', {'fields': ('image',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )
    search_fields = ['phone']
    ordering = ['phone']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)

class TableAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Table._meta.fields]

admin.site.register(Table, TableAdmin)