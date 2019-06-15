from django.shortcuts import render, redirect
from .models import ArticlePost
import markdown
from django.http import HttpResponse
from .form import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def article_list(request):
    articles = ArticlePost.objects.all()
    context = { 'articles': articles }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])

    context = { 'article': article }
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        artcle_post_form = ArticlePostForm(data=request.POST)
        if artcle_post_form.is_valid():
            new_article = artcle_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        artcle_post_form = ArticlePostForm()
        context = {'article_post_form': artcle_post_form}
        return render(request, 'article/create.html', context)


def article_delete(author, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = {'article':article, 'article_post_form':article_post_form}
        return render(request, 'article/update.html', context)


def article_list(request):
    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list, 1)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles':articles}
    return render(request, 'article/list.html', context)
