from django.contrib import admin
from .models import Dealer, Review


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'zip_code')
    search_fields = ('name', 'city', 'state')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'dealer', 'user', 'sentiment', 'created_at')
    search_fields = ('dealer__name', 'user__username', 'review')
    list_filter = ('sentiment',)