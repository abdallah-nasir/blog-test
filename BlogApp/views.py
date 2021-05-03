from django.shortcuts import render,redirect
from django.db.models import Count,Q
from django.core.paginator import Paginator
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress 
from django.shortcuts import get_object_or_404
from django.http import Http404,JsonResponse
# from django_ajax.decorators import ajax
from django.contrib.auth import logout
from django.core import serializers  
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from .models import *
from .forms import *
from taggit.models import Tag
from django.contrib import messages
from marketing.models import SignUp

# Create your views here.


def get_category_count():
    qs = Post.objects.values("category__title").annotate(Count("category"))
    return qs


#this view for seach option in Blog
def Base(request):
    post = Post.objects.all()
    comment=Comments.objects.all()
    return render(request,"base.html",{"posts":post,"comments":comment})
def search(request):
    hustle=[]
    posts = Post.objects.filter(approved=True)
    latest = Post.objects.order_by("-timestamp")[0:3]
    category_count = get_category_count()
    qs = request.GET.get("q")
    if qs:
        hustle = posts.filter(Q(title__icontains=qs)|
        Q(tags__name__icontains=qs)|Q(category__title__icontains=qs)
    ).distinct()
    if qs =="" or qs ==" ":
       hustle =[]
    paginator = Paginator(hustle,2)
    page_num =  request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    context = {"qs":hustle,"latest":latest,"category_count":category_count,"pagination":page_obj}

    return render(request,"search.html",context)


def index(request):
    post = Post.objects.filter(approved=True)[0:3]
    latest = Post.objects.filter(approved=True).order_by("-timestamp")[0:3]
    if request.method =="POST":
        email = request.POST["email"]
        send_mail(   
            subject="new Email subscribe",
            message="you will get weekly Emails from our HomeBlog",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
            )
    context={"posts":post,"latest":latest}
    return render(request,"index.html",context)

def post(request,id):
    #post
    post = get_object_or_404(Post,id=id)
    vote =Voter.objects.filter(post_id=post.id,user_id=request.user.id)
    if vote:
        myvote=Voter.objects.get(post_id=post.id,user_id=request.user.id)
    else:
        myvote=[]
    similar_posts= []
    if post.approved == True:
        similar_posts =post.tags.similar_objects()

    # def get_client_ip(request):
    #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if x_forwarded_for:
    #         ip = x_forwarded_for.split(',')[0]
    #     else:
    #         ip = request.META.get('REMOTE_ADDR')
    #     return ip
   
    #     PostViews.objects.get_or_create(user=request.user, post=post)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user,post=post)

    latest = Post.objects.filter(approved=True).order_by("-timestamp")[0:3]
    category_count = get_category_count()
    #comments
    comment = Comments.objects.filter(post=post,reply=None).order_by("-timestamp")
    form = CommentForm(request.POST or None,instance=post)   
    if form.is_valid():
        print(request.POST)            
        content = form.cleaned_data["content"]
        my_reply = request.POST.get("reply_id")
        comment_qs = None
        if my_reply:
             comment_qs = Comments.objects.get(id=my_reply)
        comments = Comments.objects.get_or_create(post=post,content=content,reply=comment_qs,user=request.user)
        messages.success(request,"your comment added successfully")
        form.save()
        return redirect(reverse("home:post",kwargs={"id":post.id}))
    context={"posts":post,
    "forms":form,
    "category_count":category_count,
    "latest":latest,
    "comments":comment,
    "similar":similar_posts,
    "votes":myvote,
    
    }
    return render(request,"post.html",context)

@login_required()
def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None )
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()
            messages.success(request, "your post will be publish after the Admin approve it")
            return redirect(reverse("home:post",kwargs={"id":instance.id}))
    context={"form":form}
    return render(request,"post_create.html",context)


@login_required()
def post_update(request,id):
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance=post )
    if request.user == post.user:
        if form.is_valid():
            instance =form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()
            messages.success(request, "You successfully updated the post")
            return redirect(reverse("home:post",kwargs={"id":post.id}))
    else:
        raise Http404
    context={"form":form}
    return render(request,"post_update.html",context)

@login_required()
def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    if request.user != post.user:
        raise Http404
    else:
        post.delete()
    return redirect(reverse("home:index"))

def post_vote_up(request,id):
    post=Post.objects.get(id=id)
    vote =Voter.objects.filter(post_id=post.id,user_id=request.user.id)
    if request.user != post.user:
        if request.user.is_authenticated:
            if vote.exists():
                v=Voter.objects.get(post_id=post.id,user_id=request.user.id)
                if v.vote_up == False and v.vote_down == True:
                    post.votes += 1
                    post.save()
                    v.delete()
                    messages.success(request,"vote deleted successuflly")
                    return redirect("home:post",id=post.id)
                if v.vote_up ==True and v.vote_down ==False:
                    messages.success(request," you cant vote twice")
                    return redirect("home:post",id=post.id)    
            else:
                Voter.objects.create(user_id=request.user.id,post_id=post.id,vote_up=True)
                post.votes +=1
                post.save()
                messages.success(request,"vote added successfully")
                return redirect("home:post",id=post.id)
        else:
            messages.success(request,"your must login to Vote")
            return redirect("home:post",id=post.id)
    else:
        messages.success(request,"your cant vote for your post")
        return redirect("home:post",id=post.id)

def post_vote_down(request,id):
    post=Post.objects.get(id=id)
    vote =Voter.objects.filter(post_id=post.id,user_id=request.user.id)
    if request.user != post.user:
        if request.user.is_authenticated:
            if vote.exists():
                v=Voter.objects.get(post_id=post.id,user_id=request.user.id)
                if v.vote_down == True and v.vote_up == False :
                    messages.success(request,"you cant vote twice")
                    return redirect("home:post",id=post.id)
                if v.vote_down == False and v.vote_up ==True:
                    post.votes -=1
                    post.save()
                    v.delete()
                    messages.success(request,"vote deleted successuflly")
                    return redirect("home:post",id=post.id)  
            else:
                Voter.objects.create(user_id=request.user.id,post_id=post.id,vote_down=True)
                post.votes -=1
                post.save()
                messages.success(request,"vote added successfully")
                return redirect("home:post",id=post.id)
        else:
            messages.success(request,"you must login to Vote")
            return redirect("home:post",id=post.id)  
    else:
        messages.success(request,"you cant vote for your post")
        return redirect("home:post",id=post.id)  

def blog(request):
    tags= Tag.objects.all().order_by("-id")[0:9]
    latest = Post.objects.filter(approved=True).order_by("-timestamp")[0:3]
    category_count = get_category_count()
    post = Post.objects.filter(approved=True)
    paginator = Paginator(post,4)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    context={"posts":post,
    "tags":tags,
    "pagination":page_obj,
    "latest":latest,
    "category_count":category_count}
  
    return render(request,"blog.html",context)


@login_required()
def profile(request,id):
    profile=get_object_or_404(Author,id=id)
    if request.user.id != profile.user.id:
        raise Http404
    form=ProfileUser(request.POST or None ,request.FILES or None,instance=request.user)
    if form.is_valid():
        my_email=EmailAddress.objects.get(user=request.user)
        my_email.email,my_email.primary,my_email.verified = form.cleaned_data["email"],False,False
        my_email.save()
        if form.cleaned_data["image"]:
            profile.image=form.cleaned_data["image"]
            profile.save()
        form.save()
        messages.success(request,"your profile has been updated")
        return redirect(reverse("home:profile",kwargs={"id":id}))
        # return redirect(reverse("account_login"))
    context={"profile":profile,"form":form}
    return render(request,"profile.html",context)
    ## Admin Area

def Admin(request):
    if request.user.is_superuser:
        post = Post.objects.filter(approved=False).order_by("-timestamp")
    else:
        raise Http404
    context={"posts":post}
    return render(request,"admin.html",context)


def Admin_Post_Update(request,id):
    post = get_object_or_404(Post,id=id)
    form = AdminForm(request.POST or None,request.FILES or None,instance=post )
    if request.user.is_superuser:
        if form.is_valid():
            instance =form.save(commit=False)
            instance.user = post.user
            instance.save()
            form.save_m2m()
            messages.success(request, "You successfully updated the post")
            return redirect(reverse("home:admin"))
    else:
        raise Http404
    context={"form":form}
    return render(request,"admin_post_update.html",context)
def Admin_Post_Delete(request,id):
    post = get_object_or_404(Post,id=id)
    if not request.user.is_superuser:
        raise Http404
    post.delete()
    return redirect(reverse("home:admin"))

def Admin_User_Delete(request,id):
    user = User.objects.filter(id=id)
    if request.user.is_superuser:
        raise Http404
    else:
        user.delete()
    return redirect(reverse("home:admin"))
 
def Contact(request):
    form=ContactForm(request.POST or None)
    if form.is_valid():
        subject=form.cleaned_data["subject"]
        message=form.cleaned_data["message"]
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=False,
    )
        messages.success(request,"your message has been sent successfully")
        form=ContactForm()
    context={"form":form}
    return render(request,"contact.html",context)
