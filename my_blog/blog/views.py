from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# Create your views here.
def post_list(request):
    posts = Post.published.all()
    #pagination view
    paginator = Paginator(posts, 2) # 8 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    #post = Post.objects.filter(status='published')
    return render (request,'blog/post_list.html', {'posts':posts, page:'pages'}) 
    #return HttpResponse (f'hello')

def post_detail(request, post):
    post =get_object_or_404(Post, slug = post, status = 'published')
    return render(request, 'blog/post_detail.html',{'post':post})
    #return render(request, 'blog/post_detail.html')



def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
 
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html') 
    return render(request, "blog/register.html")