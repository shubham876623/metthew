from django.db import models

list_of_fields=["fire department","police department",
"gun range","whole foods near",
"dollar store near","pawn shop near",
"homeless shleter near","bike path near","army recruiter near","chinese restaurant near",
"equestrian path near","golf course near","country club near","starbucks near"]

# Create your models here.
class FinalData(models.Model):
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    fire_depart = models.CharField(max_length=100, null=True, blank=True)
    police_depart = models.CharField(max_length=100, null=True, blank=True)
    gun_range = models.CharField(max_length=100, null=True, blank=True)
    food_near = models.CharField(max_length=100, null=True, blank=True)
    dollar_stor_near = models.CharField(max_length=100, null=True, blank=True)
    pawn_shop = models.CharField(max_length=100, null=True, blank=True)
    homeless_shleter = models.CharField(max_length=100, null=True, blank=True)
    bike_path = models.CharField(max_length=100, null=True, blank=True)
    army_recruiter = models.CharField(max_length=100, null=True, blank=True)
    chinese_restaurant = models.CharField(max_length=100, null=True, blank=True)
    equestrian_path = models.CharField(max_length=100, null=True, blank=True)
    golf_course = models.CharField(max_length=100, null=True, blank=True)
    country_club = models.CharField(max_length=100, null=True, blank=True)
    starbucks = models.CharField(max_length=100, null=True, blank=True)
