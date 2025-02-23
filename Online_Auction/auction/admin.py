#Online_Auction &gt; auction &gt; admin.py
from django.contrib import admin
from .models import (
    Bidder,
    Result,
    Payment,
    Member_fee,
    Status,
    Send_Feedback,
    Auction_User,
    Category,
    Sub_Category,
    Session_date,
    Session_Time,
    Product,
    Aucted_Product,
    Participant
)

# Register your models here.
admin.site.register(Bidder)
admin.site.register(Result)
admin.site.register(Payment)
admin.site.register(Member_fee)
admin.site.register(Status)
admin.site.register(Send_Feedback)
admin.site.register(Auction_User)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Session_date)
admin.site.register(Session_Time)
admin.site.register(Product)
admin.site.register(Aucted_Product)
admin.site.register(Participant)