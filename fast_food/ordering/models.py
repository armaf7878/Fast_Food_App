from django.db import models
from accounts.models import User
from restaurants.models import Restaurant

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Chờ duyệt',
        COOKING = 'cooking', 'Đang chuẩn bị',
        DELIVERING= 'delivering', 'Đang giaoo',
        FINISH = 'finish', 'Hoàn tất'
    order_id = models.AutoField(primary_key= True)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, related_name="order_user")
    restaurant = models.ForeignKey(Restaurant, on_delete= models.SET_NULL, related_name="order_restaurant")
    staff = models.ForeignKey(User, on_delete= models.SET_NULL, related_name="order_userStaff")
    shipper = models.ForeignKey(User, on_delete= models.SET_NULL, related_name="order_userShipper")
    voucher = models.ForeignKey(User, on_delete= models.SET_NULL, related_name="order_voucher") #Nhớ đổi thành voucher ở khóa ngoại
    order_lat = models.FloatField(null= False)
    order_long = models.FloatField(null= False)
    order_phone = models.CharField(max_length=15, null= False)
    order_date = models.DateTimeField(auto_now_add = True)
    subtotal = models.DecimalField(max_digits = 12, decimal_places =2)
    discount_amount = models.DecimalField(max_digits = 12, decimal_places =2)
    total = models.DecimalField(max_digits = 12, decimal_places =2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    def __str__(self):
        return self.order_id

