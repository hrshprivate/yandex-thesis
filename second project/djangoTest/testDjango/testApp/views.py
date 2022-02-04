
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm

from django.shortcuts import render, redirect, get_object_or_404

from .models import Recipe, Tag, Ing, ShopList, Favorite, Subscription
from .forms import Register, PasswordChangingForm, RecipeForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json


from .resources import RecipeResource

JSON_FALSE = JsonResponse({'success': False})
JSON_TRUE = JsonResponse({'success': True})



class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = 'login'


def indexAuth(request):
    count = None
    search_query = request.GET.get('break', '')
    if search_query:
        contact_list = Recipe.objects.filter(tag=search_query).prefetch_related('tag')
    else:
        contact_list = Recipe.objects.order_by('-id')
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    if request.user.is_authenticated:
        count = ShopList.objects.filter(
            user=request.user).select_related('user').count()
    return render(request, 'testApp/indexAuth.html', {'count': count, 'page_obj': page_obj, "tags": tags})

@login_required
@require_http_methods(['POST', 'DELETE'])
def subscriptions(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=recipe_id)
        print(recipe_id)
        if request.user == author:
            return JSON_FALSE
        Subscription.objects.get_or_create(user=request.user, author=author)
        return JSON_TRUE
    elif request.method == 'DELETE':
        author = get_object_or_404(User, id=recipe_id)
        removed = Subscription.objects.filter(user=request.user,
                                              author=author).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE

@login_required
@require_http_methods(['POST', 'DELETE'])
def purchases(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj, created = ShopList.objects.get_or_create(user=request.user,
                                                      recipe=recipe)
        if not created:
            return JSON_FALSE
        return JSON_TRUE
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        removed = ShopList.objects.filter(user=request.user,
                                          recipe=recipe).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE


@login_required
@require_http_methods(['POST', 'DELETE'])
def favorites(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj, created = Favorite.objects.get_or_create(user=request.user,
                                                      recipe=recipe)
        if not created:
            return JSON_FALSE
        return JSON_TRUE
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        removed = Favorite.objects.filter(user=request.user,
                                          recipe=recipe).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE




def myFollow(request):
    count = None
    contact_list = Subscription.objects.filter(user=request.user).select_related('user')
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        count = ShopList.objects.filter(
            user=request.user).select_related('user').count()
    return render(request, 'testApp/myFollow.html', {'count': count, 'page_obj': page_obj})



def favorite(request):
    count = None
    tags = Tag.objects.all()
    search_query = request.GET.get('break', '')
    profile = get_object_or_404(User, id=request.user.id)
    if search_query:
         contact_list = Recipe.objects.filter(favorite_recipes__user=profile, tag=search_query).prefetch_related('tag')
    else:
        contact_list = Recipe.objects.filter(favorite_recipes__user=profile).select_related('author')
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        count = ShopList.objects.filter(
            user=request.user).select_related('user').count()
    context = {'profile': profile,
               'page_obj': page_obj,
               'tags': tags,
               'count': count
               }
    return render(request, 'testApp/favorite.html', context)



def profile_view(request, author_id):
    count = None
    tags = Tag.objects.all()
    profile = get_object_or_404(User, id=author_id)
    search_query = request.GET.get('break', '')
    if search_query:
        contact_list = Recipe.objects.filter(tag=search_query, author=profile).prefetch_related('tag').select_related('author')
    else:
        contact_list = Recipe.objects.filter(author=profile).select_related('author')
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        count = ShopList.objects.filter(
            user=request.user).select_related('user').count()
    context = {'profile': profile,
               'page_obj': page_obj,
               'tags': tags,
               'count': count
               }
    return render(request, 'testApp/authorRecipe.html', context)



@login_required
def send(request):
    if request.method=='POST' and request.is_ajax():
        asd = request.POST.get("asd")
        privet = request.POST.get("privet")
        if not Ing.objects.filter(name=asd, mass=privet, Value="", user=request.user).exists():
            new_room = Ing.objects.create(name=asd, mass=privet, Value="", user=request.user)
            new_room.save()
            return JsonResponse({"asd": asd, "privet": privet}, status=200)
        else:
            new_room = Ing.objects.get(name=asd, mass=privet, Value="", user=request.user)
            new_room.save()
            return JsonResponse({"asd": asd, "privet": privet}, status=200)

@login_required
def formRecipe(request):
    ing = None
    name = request.POST.get("name")
    time = request.POST.get("time")
    dis = request.POST.get("dis")
    test = request.POST.getlist("test")
    error = ''
    if Ing.objects.filter(user=request.user, Value="").select_related('user').exists():
        ing = Ing.objects.filter(user=request.user, Value="")
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.name = name
            instance.time = time
            instance.dis = dis
            instance.save()
            if ing:
                instance.ing.add(*ing)
                Ing.objects.filter(user=request.user, Value="").update(Value=name)
            instance.tag.add(*test)
            return redirect('home')
        else:
            error = 'Форма была неверной'
    form = RecipeForm()
    tags = Tag.objects.all()
    ALL = Ing.objects.filter(Value="")
    context = {
        'form': form,
        'error': error,
        'tags': tags,
        "ALL": ALL
    }
    return render(request, 'testApp/formRecipe.html', context)

@login_required
@require_http_methods(['POST', 'GET'])
def edit_recipe(request, recipe_id):
    ing = None
    if Ing.objects.filter(user=request.user, Value="").select_related('user').exists():
        ing = Ing.objects.filter(user=request.user, Value="")
    test = request.POST.getlist("tags")
    name = request.POST.get("name")
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    tags = Tag.objects.all()
    if request.user != recipe.author:
        return redirect('mono', recipe_id=recipe.id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        user = form.save(commit=False)
        if user.tag:
            user.tag.clear()
            user.tag.add(*test)
        if ing:
            user.ing.add(*ing)
            Ing.objects.filter(user=request.user, Value="").update(Value=name)
        user.save()
        return redirect('mono', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    context = {
        "tags": tags,
        "form": form,
        "recipe": recipe,
    }
    return render(request, 'testApp/formChangeRecipe.html', context)


class RegisterFormView(FormView):
    form_class = Register

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = 'login'

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "testApp/reg.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "testApp/authForm.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


def mono(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    profile = recipe.author
    ing = Ing.objects.all()
    return render(request, 'testApp/singlePage.html', {'recipe': recipe, 'ing': ing, 'profile': profile})


def delete_task(request, recipe_id):
    recipe = Ing.objects.get(id=recipe_id)
    if recipe:
            recipe.delete()
            return JsonResponse({'message': 'Good'})
    return render(request, 'testApp/formChangeRecipe.html', {'recipe': recipe})



def indexNotAuth(request):
    search_query = request.GET.get('break', '')
    if search_query:
        contact_list = Recipe.objects.filter(tag=search_query).prefetch_related('tag')
    else:
        contact_list = Recipe.objects.order_by('-id')
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, 'testApp/indexNotAuth.html', {'page_obj': page_obj, 'tags': tags})


@login_required
@require_http_methods(['GET'])
def shopList(request):
    recipes = Recipe.objects.filter(shoplist__user=request.user)
    if request.method == 'GET':
        count = ShopList.objects.filter(
            user=request.user).select_related('user').count()
        context = {'recipes': recipes, 'count': count}
        return render(request, 'testApp/shopList.html', context)

def DeleteChatUser(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        test = Ing.objects.filter(Value=recipe.name, user=request.user).delete()
        if recipe:
            recipe.delete()
            return redirect('home')
        return render(request, 'testApp/indexAuth.html', {'test': test})


def export_data(request):
    if request.method == 'POST':
        file_format = 'JSON'
        employee_resource = RecipeResource()
        queryset = Recipe.objects.filter(shoplist__user=request.user)
        dataset = employee_resource.export(queryset)
        if file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="ing.json"'
            return response
    return render(request, 'testApp/shopList.html')