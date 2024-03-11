from Rare_app.models import FAQ, Artist_detail, Blog, Cart, Category, ContactUs, CustomerContact, Orders, Payment, Post
from django.contrib import admin

@admin.register(Category)
class RegisterCategory(admin.ModelAdmin):
    list_display=['title','description']


@admin.register(Artist_detail)
class RegisterArtistDetails(admin.ModelAdmin):
    list_display=['id','artist','contact','address','adhar']

@admin.register(Post)
class RegisterPost(admin.ModelAdmin):
    list_display = ['title','category','description','price','posted_by','posted_at','availablity_status']

@admin.register(FAQ)
class RegisterFAQ(admin.ModelAdmin):
    list_display = ['question','answer','product','asked_by','asked_at','attended']

@admin.register(Cart)
class RegisterCart(admin.ModelAdmin):
    list_display = ['id','holder']

@admin.register(Payment)
class RegisterPayment(admin.ModelAdmin):
    list_display = ['id','amount']

@admin.register(Orders)
class RegisterOrder(admin.ModelAdmin):
    list_display = ['id','sender']

@admin.register(ContactUs)
class RegisterContactUs(admin.ModelAdmin):
    list_display = ['name','subject']

@admin.register(CustomerContact)
class RegisterCustomerContact(admin.ModelAdmin):
    list_display = ['user','address']
    
@admin.register(Blog)
class RegisterBlog(admin.ModelAdmin):
    list_display = ['subject','posted_by']
