# Online_Auction &gt; Online_Auction &gt; urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from auction.views import *
from auction.models import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)