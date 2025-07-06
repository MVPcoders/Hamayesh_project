from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .models import Article

# دکوریتور ها
def is_login(func):
    def wrapper(request:HttpRequest, *args, **kwargs):
        if  request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
    return wrapper


@method_decorator(is_login, name='dispatch')
class SubmitArticle(View):

    def get(self, request, *args, **kwargs):
        return render (request,"article_moddule/article.html",context={})


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
            authors_info =authors_info,

        )
        return render(request, "index_module/index.html", context={})






# # کد های کامنت شده
# from .forms import ArticleForm

# def submit_article(request):
#     if request.method == 'POST':
#         article_form = ArticleForm(request.POST, request.FILES)
#         author_form = ArticleAuthorForm(request.POST)
#
#         if article_form.is_valid() and author_form.is_valid():
#             article = article_form.save()
#             author = author_form.save(commit=False)
#             author.article = article
#             author.save()
#             return redirect('index')  # به صفحه موفقیت هدایت کنید
#
#     else:
#         article_form = ArticleForm()
#         author_form = ArticleAuthorForm()
#
#     return render(request, 'article_moddule/article.html', {
#         'article_form': article_form,
#         'author_form': author_form,
#     })
