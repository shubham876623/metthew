from django.contrib import admin
from app.models import FinalData


def download_csv(modelsadmin, request, queryset):
    import csv
    f = open('some.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(["address", "zip_code", "fire_depart", "police_depart", "gun_range", "food_near", "dollar_stor_near", "pawn_shop", "homeless_shleter", "bike_path", "army_recruiter", "chinese_restaurant", "equestrian_path", "golf_course", "country_club", "starbucks"])
    for s in queryset:
        writer.writerow([s.address, s.zip_code, s.fire_depart, s.police_depart, s.gun_range, s.food_near, s.dollar_stor_near, s.pawn_shop, s.homeless_shleter, s.bike_path, s.army_recruiter, s.chinese_restaurant, s.equestrian_path, s.golf_course, s.country_club, s.starbucks])

class FinalDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'zip_code')
    actions = [download_csv]

admin.site.register(FinalData, FinalDataAdmin)