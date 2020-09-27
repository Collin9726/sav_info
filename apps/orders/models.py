from django.db import models
from django.contrib.auth import get_user_model as user_model
User = user_model()

# Create your models here.
class Order(models.Model):
    posted = models.DateTimeField(auto_now_add=True)
    item = models.CharField(max_length=50)    
    amount = models.IntegerField()    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item 
