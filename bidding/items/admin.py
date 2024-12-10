from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
   
    list_display = ['name', 'starting_bid', 'auction_end_time', 'highest_bidder', 'sold_status']
    
    list_filter = ['sold_status', 'auction_end_time']
    
    search_fields = ['name']
    
    fields = ['name', 'description', 'starting_bid', 'auction_end_time', 'highest_bidder', 'sold_status']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.sold_status:
            return ['auction_end_time', 'highest_bidder']
        return super().get_readonly_fields(request, obj)
