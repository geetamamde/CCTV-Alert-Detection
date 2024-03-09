from django.contrib import admin
from .models import Information,Payment


class InformationAdmin(admin.ModelAdmin):
    list_display =("id", "number_of_cctvs","start_time","end_time","total_hours","period","card_choice",'final_price','user')

admin.site.register(Information, InformationAdmin)
admin.site.register(Payment)