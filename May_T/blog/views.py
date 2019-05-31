from django.shortcuts import render, redirect
from .models import Blog
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    posts = Blog.objects.all()
    paginator = Paginator(posts,3)
    now_page = request.GET.get('page')
    posts = paginator.get_page(now_page)
    context= {
        "posts":posts
    }    

    return render(request,'index.html',context)

def read(request,post_id):
    post = Blog.objects.get(id=post_id)
    context = {
        "post":post
    }

    return render(request,'read.html',context)

def create(request): 
    if request.method == "GET":
        return render(request,'create.html')

    elif request.method == "POST":
        post = Blog()

        post.user = request.user

        post.title = request.POST['title']
        post.category = request.POST['category']
        post.content = request.POST['content'] 

        try:
            post.pic = request.FILES['pic']
        except:
            pass
        
        post.save()

        return redirect(index)

def update(request,post_id):
    if request.method == "GET":
        post = Blog.objects.get(id=post_id)
        context={
            "post":post
        }
        return render(request,'update.html',context)
    
    elif request.method == "POST":  
        post = Blog.objects.get(id=post_id)
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save() 
        return redirect(index)

def delete(request,post_id):
    post = Blog.objects.get(id = post_id)
    post.delete()
    return redirect(index)
# Create your views here.

def search(request):
    search_title = request.GET['search']
    search_filter = request.GET['search_filter']
    if search_filter == "제목":
        posts = Blog.objects.filter(title__icontains=search_title)
    elif search_filter == "내용":
        posts = Blog.objects.filter(content_icontains=search_title)
    
    elif search_filter == "제목+내용":
        posts = Blog.objects.all().filter(Q(title__icontains=search_title) | Q(content_icontains=search_title))
    context={   
       "posts":posts
    }
    return render(request,"search.html",context)

def category(request):
    search_category = request.GET['category']
    posts = Blog.objects.filter(category=search_category)
    context={
        "posts":posts
    }
    return render(request,"category.html",context)

