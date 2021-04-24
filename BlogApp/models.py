from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from allauth.account.models import EmailAddress
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User,default=1, on_delete=models.CASCADE)
    image = models.ImageField(default="user-icon.png")
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_Author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
class Category(models.Model):
    title = models.CharField(max_length=50)


    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    overviews = RichTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user= models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    image = models.ImageField()
    category = models.ManyToManyField(Category)
    approved = models.BooleanField(default=False) 
    tags = TaggableManager()
    votes = models.IntegerField(default=0)
    views= models.PositiveIntegerField(default=0)
  #  next_post = models.ForeignKey("self",related_name="next",on_delete=models.SET_NULL,null=True,blank=True)
  #  previous_post = models.ForeignKey("self",related_name="previous",on_delete=models.SET_NULL,null=True,blank=True)

    # @property
    # def views_count(self):
    #     return PostViews.objects.filter(post=self).count()
    @property   
    def view_count(self):
        return PostView.objects.filter(post=self).count()
    def get_absolute_url(self):
        return reverse("home:post", kwargs={"id": self.id})
    def get_update_url(self):
        return reverse("home:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("home:delte", kwargs={"id": self.id})
        

    def __str__(self):
        return self.title
# class PostViews(models.Model):
#     ip = models.GenericIPAddressField(default="45.243.82.169")
#     post= models.ForeignKey("Post",on_delete=models.CASCADE)

#     def __str__(self):
#         return (f"{self.ip} for post {self.post.id}")

class PostView(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey("Post",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Voter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    vote_up = models.BooleanField(default=False)
    vote_down = models.BooleanField(default=False) 
    def __str__(self):
        return self.post.title

class Comments(models.Model):
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.ForeignKey("self",related_name="replies",null=True,blank=True,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        if self.reply:
            return (f"reply id {self.reply.id} on comment {self.id}")
        else:
            return (f"comment id {self.id} for post {self.post.id}")



