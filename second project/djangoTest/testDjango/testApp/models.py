from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from pytils import translit



class Tag(models.Model):

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    brk = models.CharField('Время дня и ночи', max_length=10, null=True)

    def __str__(self):
         return self.brk


class Ing(models.Model):

    class Meta:
        verbose_name = 'Ингридиенты'
        verbose_name_plural = 'Ингридиенты'

    name = models.CharField('Шо', max_length=100, null=True)
    mass = models.PositiveSmallIntegerField('Количество', null=True, blank=True)
    Value = models.CharField('Имя рецепта', max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
         return self.name


class Recipe(models.Model):


    def get_image_path(self, filename):
        path = ''.join(["pictures/", translit.slugify(filename)])
        return path

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="recipes")
    name = models.CharField('Название', null=True, blank=True, max_length=120)
    dis = models.TextField('Desc:', blank=True)
    tag = models.ManyToManyField(Tag, related_name="tag", blank=True)
    time = models.IntegerField('Время', null=True, blank=True)
    image = ResizedImageField(size=[500, 300], quality=100, blank=True, upload_to=get_image_path, verbose_name='Картинка')
    ing = models.ManyToManyField(Ing, related_name="ing", blank=True)

    def bit(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'
        bit.short_description = 'Картинка'
        bit.allow_tags = True
    def __str__(self):
         return self.name



class ShopList(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             related_name='shoplist',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепты',
                               related_name='shoplist',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_shoplist')]
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'

    def __str__(self):
        return self.recipe.name




class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепт в избранном',
                               related_name='favorite_recipes',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             related_name='favorites',
                             on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='UniqueFavorite')]
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self):
        return self.recipe.name


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='подписчик',
                             related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               verbose_name='автор',
                               related_name='following',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_subscription')]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'{self.user} подписан(а) на {self.author}'






