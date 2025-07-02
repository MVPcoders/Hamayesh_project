from django.shortcuts import render, redirect
from .forms import ArticleForm, ArticleAuthorForm


def submit_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        author_form = ArticleAuthorForm(request.POST)

        if article_form.is_valid() and author_form.is_valid():
            article = article_form.save()
            author = author_form.save(commit=False)
            author.article = article
            author.save()
            return redirect('success_page')  # به صفحه موفقیت هدایت کنید

    else:
        article_form = ArticleForm()
        author_form = ArticleAuthorForm()

    return render(request, 'article_moddule/article.html', {
        'article_form': article_form,
        'author_form': author_form,
    })
