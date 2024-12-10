from django.db import models
from django.contrib.auth.models import User 
from django.utils.timezone import now  

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    auction_end_time = models.DateTimeField()  
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_items')  
    sold_status = models.BooleanField(default=False) 
    
    def is_auction_active(self):
        return self.auction_end_time > now()

    def __str__(self):
        return self.name