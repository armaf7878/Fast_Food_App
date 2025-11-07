from django.db import models

class Restaurant(models.Model):
  
    restaurant_id = models.AutoField(primary_key=True)
    res_name = models.CharField(max_length=100)
    res_address = models.TextField()
    res_phone = models.CharField(max_length=15, null=True, blank=True)
    res_lat = models.FloatField(null=True, blank=True)
    res_long = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.res_name
