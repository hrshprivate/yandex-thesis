from django.contrib import admin
from .models import Recipe, Tag, Ing, ShopList, Favorite, Subscription

admin.site.register(Tag)
admin.site.register(Ing)

class RecipeAdmin(admin.ModelAdmin):

    list_display = ["name", "dis", "image", "bit", "author", "time"]


class ShopListAdmin(admin.ModelAdmin):

    list_display = ["user", "recipe"]


class FavoriteAdmin(admin.ModelAdmin):

    list_display = ["recipe", "user"]


class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ["user", "author"]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShopList, ShopListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

