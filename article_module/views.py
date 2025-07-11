from logging import raiseExceptions

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .models import Article


# دکوریتور ها
def is_login(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return wrapper


@method_decorator(is_login, name='dispatch')
class SubmitArticle(View):

    def get(self, request, *args, **kwargs):
        return render(request, "article_moddule/article.html", context={})

    def post(self, request, *args, **kwargs):
        form = request.POST
        authors_info = {}
        # برای تشخیص نویسنده مسئول
        corresponding_index = int(form.get('correspondingAuthor', 0))
        for i in range(int(form['authorCount'])):
            authour = {
                "fist_name": form.get(f'authorFirstName{i}'),
                "last_name": form.get(f'authorLastName{i}'),
                "email": form.get(f'authorEmail{i}'),
                # "ORCID": form.get[f'authorORCID${i}', ""],
                "main_author": (i == corresponding_index),
            }
            authors_info[i] = authour

        new_article = Article.objects.create(
            user=request.user,
            authors_numbers=form['authorCount'],
            main_goal=form['articleMainGoal'],
            language=form['articleLang'],
            persian_subject=form['articlePersianTitle'],
            english_subject=form['articleEnglishTitle'],
            article_abstract=form['articleAbstract'],
            file=request.FILES.get('articleFile'),
            authors_info=authors_info,

        )
        return render(request, "index_module/index.html", context={})


class UserArticleEdit(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/user_profile.html', context)

    def post(self, request):
        form = request.POST
        try:
            article: Article = Article.objects.filter(user_id=request.user.id, id=form.get('articleId')).first()
            if request.FILES.get('newFile'):
                article.file = request.FILES.get('newFile')

            article.persian_subject = form.get('editPersianTitle')
            article.english_subject = form.get('editEnglishTitle')
            article.main_goal = form.get('editMainGoal')
            article.language = form.get('editLanguage')
            article.article_abstract = form.get('editAbstract')

            article.save()
            return JsonResponse({
                'status': 'success',
                'message': 'مقاله شما با موفقیت ویرایش شد'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'fail',
                'message': str(e)
            })
