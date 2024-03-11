from collections import namedtuple
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.fields import EmailField

class Artist_detail(models.Model):
    artist = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.PositiveBigIntegerField()
    adhar = models.ImageField(upload_to='images/artist_adhar_images')
    address = models.CharField(max_length=500)

    def __str__(self):
        return str(self.artist)    

class CustomerContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_no = models.PositiveBigIntegerField()
    address = models.TextField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    zip = models.PositiveIntegerField()

    def __str__(self):
        return str(self.address) 

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/category')

    def __str__(self):
        return self.title

class Post(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=35)
    description = models.CharField(max_length=350)
    image_1 = models.ImageField(upload_to='images/post_images')
    image_2 = models.ImageField(upload_to='images/post_images',null=True,blank=True)
    price = models.PositiveIntegerField()
    availablity_status = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='blogpost_like',blank=True)

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.like.count()
    
    def get_artist(self):
        return str(self.posted_by)

class FAQ(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=3000,null=True,blank=True,default=None)
    product = models.ForeignKey(Post,on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    asked_by = models.ForeignKey(User,on_delete=models.CASCADE)
    asked_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.question

class Cart(models.Model):
    holder = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart_holder')
    product = models.ManyToManyField(Post, related_name='cart_products',blank=True)

    def __str__(self):
        return str(self.holder)
    

class Orders(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    ordered_products = models.ManyToManyField(Post, related_name='ordered_products')
    done_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25)
    address = models.ForeignKey(CustomerContact,on_delete=models.DO_NOTHING,blank=True,null=True)
    amount = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return str(self.id)
    
    def get_name(self):
        return str(self.receiver.first_name)+(" ")+str(self.receiver.last_name)
    
    def get_email(self):
        return str(self.receiver.email)
    
class Payment(models.Model):
    amount = models.PositiveIntegerField()
    payer = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20)
    done_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Orders,on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return str(self.payer)

class ContactUs(models.Model):
    name = models.CharField(max_length=30)
    message = models.TextField(max_length=1000)
    subject = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)


    def __str__(self):
        return str(self.message)

class Blog(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    img = models.ImageField(upload_to='images/blog_images',null=True,blank=True)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subject)
    
    


