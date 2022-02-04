from django import template

from testApp.models import ShopList, Favorite, Subscription



register = template.Library()


@register.filter
def purchased(recipe, user):
    return ShopList.objects.filter(recipe=recipe, user=user).exists()

@register.filter
def favorite(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()

@register.filter
def is_follower(user, profile):
    return Subscription.objects.filter(
        user=user, author=profile).exists()