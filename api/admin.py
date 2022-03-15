from django.contrib import admin
from django.utils.html import  mark_safe
from .models import TypeHouse, House, Service, User, Comment, Action, Rating, RentManage, Message, Blog


class HouseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type_house", "delete_flag", "updated_date"]
    search_fields = ["name", "type_house__name", "updated_date"]
    list_filter = ["name", "type_house__name", "updated_date"]
    readonly_fields = ["avatar"]

    def avatar(self, house):
        return mark_safe("<img src='/static/{img_url}' width='360px'/>".format(img_url=house.image.name, alt=house.name))


admin.site.register(User)
admin.site.register(TypeHouse)
admin.site.register(House, HouseAdmin)
admin.site.register(Service)
admin.site.register(Comment)
admin.site.register(Action)
admin.site.register(Rating)
admin.site.register(RentManage)
admin.site.register(Message)
admin.site.register(Blog)
