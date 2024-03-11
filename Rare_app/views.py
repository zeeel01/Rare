from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .form import ArtistForm, ChangePassUser, CheckoutForm, ContactUsForm, EditFAQs, EditProfile, FAQs, LoginUser, NewBlog, NewPost, RegUser
from .models import FAQ, Artist_detail, Blog, Cart, Category, CustomerContact, Orders, Payment, Post
from django.db.models import Q
from Rare_app import form

#----------------------------------------------------------Home------------------------------------------------------------------

def homeView(request):
    cats = Category.objects.all()
    pop_pro = (Post.objects.order_by('-like')).filter(availablity_status=True)
    pop_pro = pop_pro[0:6]
    latest_pro = (Post.objects.order_by('-posted_at')).filter(availablity_status=True)
    latest_pro = latest_pro[0:4]
    return render(request,"index.html",{'cats':cats,'pop_pro':pop_pro,'latest_pro':latest_pro})

#-----------------------------------------------------New Post-------------------------------------------------------------------

@login_required(login_url='login')
def newPostView(request):
    data = Category.objects.all()
    if request.method == 'POST':
        form = NewPost(request.POST,request.FILES)
        if form.is_valid():
            post_data = form.save(commit=False)
            if not post_data.image_2:
                post_data.image_2=post_data.image_1
            post_data.posted_by = request.user
            # post_data.like = 0
            post_data.save()
            return redirect('home')
        else:
            print("Form is not valid")
    else:
        form = NewPost()
    return render(request,"newpost.html",{'form':form,'data':data})

#-------------------------------------------------------New Blog----------------------------------------------------------------

@login_required(login_url='login')
def newBlogView(request):
    if request.method == 'POST':
        form = NewBlog(request.POST,request.FILES)
        if form.is_valid():
            post_data = form.save(commit=False)
            post_data.posted_by = request.user
            post_data.save()
            return redirect('blogs')
        else:
            print("Form is not valid")
    else:
        form = NewBlog()
    return render(request,"newblog.html",{'form':form,})

#-------------------------------------------------------Register---------------------------------------------------------------

def registrationView(request):
    if request.method == "POST":
        form = RegUser(request.POST)
        if form.is_valid():    
            uname=form.cleaned_data['username']
            if request.POST['role'] == 'CUSTOMER':
                form.save()
                curr_user = User.objects.get(username=uname)
                Cart.objects.create(holder=curr_user)
                return redirect('/')
            elif request.POST['role'] == 'ARTIST':
                user=form.save(commit=False)
                user.is_active=False
                form.save()
                x=User.objects.get(username=uname)
                return HttpResponseRedirect('/artistdetails/%d/'% x.id)
        else:
            print("form is not valid")
            for field in form:
                print("Field Error:", field.name,  field.errors)
            form = RegUser()
    else:
        form = RegUser()
        print('--------------------------------------------------------------elsepart')
    return render(request,"registration.html",{'form':form})

#---------------------------------------------------------Login------------------------------------------------------------------

def loginView(request):
    form = LoginUser()
    if request.method == 'POST':
        uname = request.POST['username']
        upass = request.POST['password']
        user = authenticate(username=uname,password=upass)
        if user is None:
            return redirect('login')
        else:
            login(request,user)
        return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,'login.html',{'form':form})

#--------------------------------------------------------------Logout------------------------------------------------------------

@login_required(login_url='login')
def logoutView(request):
    if request.user.is_authenticated:
        print("logged out")
        logout(request)
        return redirect('login')
    else:
        return redirect('login')

#--------------------------------------------------------Artist details------------------------------------------------------------

def artistDetailsView(request,id):
    if request.method=='POST':
        form=ArtistForm(request.POST,request.FILES)
        data = User.objects.get(id=id)
        if form.is_valid():
            user=form.save(commit=False)
            user.artist=data
            user.save()
            return redirect('/')
        else:
            form=ArtistForm(request.FILES)
            for field in form:
                print("Field Error:", field.name,  field.errors)
    else:
        form = ArtistForm()
    return render(request,'artist_details.html',{'form':form})

#-------------------------------------------------------Manage Artist------------------------------------------------------------

def manageArtistView(request):
    cats = Category.objects.all()
    all_data = Artist_detail.objects.filter(artist__in=User.objects.filter(is_active=False))
    return render(request,"manage_artist.html",{'cats':cats,'all_data':all_data})

#------------------------------------------------------Approve Artist------------------------------------------------------------

@login_required(login_url='login')
def approveArtistView(request,id):
    cats = Category.objects.all()
    all_data = Artist_detail.objects.filter(artist__in=User.objects.filter(is_active=False))
    artist_data=Artist_detail.objects.get(id=id)
    data=User.objects.get(username=str(artist_data.artist))
    data.is_active=True
    data.is_staff=True
    data.save()
    return render(request,"manage_artist.html",{'cats':cats,'all_data':all_data})

#-------------------------------------------------------Reject Artist------------------------------------------------------------

@login_required(login_url='login')
def rejectArtistView(request,id):
    cats = Category.objects.all()
    artist_data=Artist_detail.objects.get(id=id)
    artist_data.delete()
    return redirect('manageartist')

#----------------------------------------------------Change Password------------------------------------------------------------

@login_required(login_url='login')
def changePasswordView(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ChangePassUser(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = ChangePassUser(user = request.user)
    context= {'form':form}
    return render(request,'changepass.html',context)

#--------------------------------------------------Filter By Category------------------------------------------------------------

def categoryPostView(request,id):
    cats = Category.objects.all()
    all_data = (Post.objects.filter(
        category=Category.objects.get(id=id)
    )).filter(availablity_status=True)
    return render(request,"all_post.html",{'cats':cats,'all_data':all_data})

#----------------------------------------------------Latest Post View------------------------------------------------------------

def allPostView(request):
    cats = Category.objects.all()
    all_data = (Post.objects.order_by('-posted_at')).filter(availablity_status=True)
    return render(request,"all_post.html",{'cats':cats,'all_data':all_data})

#------------------------------------------FAQ And Detailed Post View------------------------------------------------------------

def FAQView(request,id):
    form=FAQs()
    if request.method=='POST':
        form=FAQs(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            que = form.cleaned_data['question']
            print(que)
            instance.answer=None
            instance.product=Post.objects.get(id=id)
            instance.attended=False
            instance.asked_by=User.objects.get(id=request.user.id)
            instance.save()
        else:
            print("Form is not valid")     
    all_data=Post.objects.get(id=id)
    cats = Category.objects.all()
    if not all_data.image_2:
        all_data.image_2 = all_data.image_1
        all_data.save()
    liked = not all_data.like.filter(id=request.user.id).exists()
    like_list=all_data.like.all()
    ans_que=FAQ.objects.filter(attended=True,product=all_data)
    num_que=ans_que.count()
    return render(request,"post_details.html",{'cats':cats,'form':form,'i':all_data,'answered_faq':ans_que,'num_que':num_que,'liked':liked,'like_list':like_list})

#-----------------------------------------------Like Dislike Post View------------------------------------------------------------

@login_required(login_url='login')
def LikePostView(request,id):
    form=FAQs()
    all_data=Post.objects.get(id=id)
    if all_data.like.filter(id=request.user.id).exists():
        all_data.like.remove(request.user)
        return redirect('/postdetails/'+str(id)+'/')
    else:
        all_data.like.add(request.user)
        return redirect('/postdetails/'+str(id)+'/')

#------------------------------------------------------My Post View------------------------------------------------------------

def mypostsView(request):
    cats = Category.objects.all()
    my_pro=Post.objects.filter(posted_by=request.user)
    return render(request,"myposts.html",{'cats':cats,'my_pro':my_pro})

#----------------------------------------------------------My blogs View------------------------------------------------------------

@login_required(login_url='login')
def myblogsView(request):
    cats = Category.objects.all()
    my_pro=Blog.objects.filter(posted_by=request.user)
    print(my_pro)
    return render(request,"myblog.html",{'cats':cats,'my_pro':my_pro})

#--------------------------------------------------------Edit Post View------------------------------------------------------------

def editPostView(request,id):
    
    if request.method=='POST': 
        obj = Post.objects.get(id=id)
        print(obj)
        form = NewPost(request.POST,request.FILES,instance=obj)   
        if form.is_valid():
            post_data = form.save(commit=False)
            if not post_data.image_2:
                post_data.image_2=post_data.image_1
            post_data.posted_by = request.user
            post_data.save()
            return redirect('myposts')
        else:
            obj = Post.objects.get(id=id)
            form = NewPost(request.POST,request.FILES,instance=obj) 
    else:
        obj = Post.objects.get(id=id)
        form = NewPost(instance=obj)
    return render(request,'edit_post.html',{'form':form})

#---------------------------------------------------------Edit Blog View------------------------------------------------------------

def editBlogView(request,id):
    
    if request.method=='POST': 
        obj = Blog.objects.get(id=id)
        form = NewBlog(request.POST,request.FILES,instance=obj)   
        if form.is_valid():
            post_data = form.save(commit=False)
            post_data.posted_by = request.user
            post_data.save()
            return redirect('myblogs')
        else:
            obj = Blog.objects.get(id=id)
            form = NewBlog(request.POST,request.FILES,instance=obj) 
    else:
        obj = Blog.objects.get(id=id)
        form = NewBlog(instance=obj)
    return render(request,'edit_blog.html',{'form':form})

#-------------------------------------------------------Delete Post View------------------------------------------------------------

def deletePostView(request,id):
    obj=Post.objects.get(id=id)
    obj.delete()
    return redirect('myposts')

#-------------------------------------------------------Delete Blog View------------------------------------------------------------

def deleteBlogView(request,id):
    obj=Blog.objects.get(id=id)
    obj.delete()
    return redirect('myblogs')

#-------------------------------------------------------Show Artist View------------------------------------------------------------

def viewArtist(request,id):
    curr_obj=Post.objects.get(id=id)
    cats = Category.objects.all()
    obj = Post.objects.filter(posted_by=curr_obj.posted_by)
    return render(request,"artist_products.html",{'cats':cats,'my_pro':obj})

#------------------------------------------------------My FAQs------------------------------------------------------------------------

def myFAQsView(request):
    my_pro=Post.objects.filter(posted_by=request.user)
    cats = Category.objects.all()
    faqs=FAQ.objects.filter(product__in=my_pro)
    print(faqs)
    return render(request,"faq_artist.html",{'cats':cats,'faqs':faqs})

#-------------------------------------------------------Delete FAQ------------------------------------------------------------------

def deleteFAQView(request,id):
    obj=FAQ.objects.get(id=id)
    obj.delete()
    return redirect('myfaqs')

#------------------------------------------------------Edit FAQ--------------------------------------------------------------------

def editFAQView(request,id):
    curr_FAQ = FAQ.objects.get(id=id)
    if request.method == 'POST':
        form = EditFAQs(request.POST,instance=curr_FAQ)
        if form.is_valid():
            answered_faq = form.save(commit=False)
            answered_faq.product = curr_FAQ.product
            answered_faq.question = curr_FAQ.question
            answered_faq.attended = True
            answered_faq.asked_by = curr_FAQ.asked_by
            answered_faq.asked_at = curr_FAQ.asked_at
            answered_faq.save()
            return redirect('myfaqs')
        else:
            print("form is not valid")
    else:
        form = EditFAQs(instance=curr_FAQ)
    return render(request,"edit_faq.html",{"form":form})

#-----------------------------------------------------------------Edit Profile------------------------------------------------------

def editProfileView(request):
    if request.method == 'POST':
        form = EditProfile(request.POST,instance=request.user)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.username=request.user.username
            obj.password=request.user.password
            obj.save()
            return redirect("home")
        else:
            print("form is not valid")
    else:
        form = EditProfile(instance=request.user)
    return render(request,"edit_profile.html",{'form':form})

#------------------------------------------------------------Search Product--------------------------------------------------------

def searchView(request):
    if request.method == 'POST':
        title = request.POST['title']
        if not title:
            return render(request,"search.html",{'cats':cats})
        cats = Category.objects.all()
        result = Post.objects.filter(Q(title__icontains=title) | Q(description__icontains=title))  
        return render(request,"search.html",{'cats':cats,'all_data':result})
    else:
        cats = Category.objects.all()
        return render(request,"search.html",{'cats':cats})

#--------------------------------------------------------------Cart View----------------------------------------------------------

def cartView(request):
    try:
        cart=Cart.objects.get(holder=request.user)
    except:
        cart=Cart()
        cart.holder=request.user
        cart.save()        
    products=cart.product.all()
    total_amt = 0
    for p in products:
        total_amt += p.price
    cats = Category.objects.all()
    return render(request,'cart.html',{'cats':cats,'products':products,'total':total_amt,'total_amt':(total_amt+50)})

#---------------------------------------------------------Remove from cart View---------------------------------------------------

def removeFromCartView(request,id):
    cart=Cart.objects.get(holder=request.user)
    cart.product.remove(id)
    cart.save()
    return redirect('cart')

#----------------------------------------------------------Add to Cart----------------------------------------------------------

@login_required(login_url='login')
def addToCartView(request,id):
    try:
        cart=Cart.objects.get(holder=request.user)
    except:
        cart=Cart()
        cart.holder=request.user
        cart.save()  
    pro =Post.objects.get(id=id)
    if cart.product.count()==0:
        cart.product.add(id)
        cart.save()
        return redirect('cart')
    elif pro in cart.product.all():   
       messages.error(request,"Product is already in the cart!")
       return redirect('cart') 
    elif not pro.posted_by==cart.product.all()[0].posted_by:
        messages.error(request,"Cannot add items from multiple artists at same time!")
        return redirect('home') 
    else:
        cart.product.add(id)
        cart.save()
        return redirect('cart')

#---------------------------------------------------------About Us---------------------------------------------------------------

def aboutUsView(request):
    cats = Category.objects.all()
    return render(request,'about.html',{'cats':cats})

#---------------------------------------------------------Contact Us--------------------------------------------------------------

def contactUsView(request):
    cats = Category.objects.all() 
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactUsForm()
    return render(request,'contact.html',{'cats':cats,'form':form})

#--------------------------------------------------Select Address---------------------------------------------------------------

@login_required(login_url='login')
def selectAddressView(request):
    cust_add= CustomerContact.objects.filter(user=request.user)
    if cust_add:
        return render(request,"my_address.html",{'addresses':cust_add})
    else:
        return redirect('checkout')
    
#---------------------------------------------------Finalize Address-----------------------------------------------------------------


def finalizeAddressView(request,id):
    return redirect('/saveorder/'+str(id)+'/')

#---------------------------------------------------------Add new address---------------------------------------------------------------

def checkoutView(request):
    if request.method=='POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            details =form.save(commit=False)
            details.user=request.user
            details.save()
            return redirect('/saveorder/'+str(details.id)+'/')   
    else:
        form = CheckoutForm()
    return render(request,'checkout.html',{'form':form,})

#------------------------------------------------Save orders-------------------------------------------------------------------------------

def saveOrderView(request,id):
    add = CustomerContact.objects.get(id=id)
    ordered_pro = request.user.cart_holder.product.all()
    amt = 0
    for p in ordered_pro:
        amt += p.price
    ord = Orders()
    ord.receiver= request.user
    ord.sender = ordered_pro[0].posted_by
    ord.status = 'Pending'
    ord.amount = amt
    ord.address=add
    ord.save()
    ord.ordered_products.set(ordered_pro)
    ord.save()
    return redirect('/payment/'+str(ord.id)+'/')

#-------------------------------------------------------Latest Blogs---------------------------------------------------------------

def latestblogsView(request):
    all_blogs = Blog.objects.order_by('-posted_at')
    return render(request,'blogs.html',{'all_blogs':all_blogs})

#------------------------------------------------------------Payment-------------------------------------------------------------------

def paymentView(request,id):
   ord  = Orders.objects.get(id=id)
   amt = ord.amount
   return render(request,'payment.html',{'amount':amt,'id':ord.id}) 

#-------------------------------------------------------Payment Success----------------------------------------------------------

def paymentSuccessView(request,id):
    ord  = Orders.objects.get(id=id)
    pay = Payment()
    pay.amount = ord.amount
    pay.payer = ord.receiver
    pay.order = ord
    pay.status = 'Successful'
    pay.save()
    for p in ord.ordered_products.all():
        p.availablity_status=False
        p.save()
    cart = Cart.objects.get(holder=request.user)
    cart.product.clear()
    cart.save()
    return redirect('myorders')

#-------------------------------------------------------My Orders--------------------------------------------------------------------------

def myOrdersView(request):
    ords = (Orders.objects.filter(receiver=request.user)).order_by('-done_at')
    return render(request,'my_orders.html',{'orders':ords})

#------------------------------------------------------Ordered Products-------------------------------------------------------------------

def orderedProductsView(request,id):
    ord=Orders.objects.get(id=id)
    products=Post.objects.all()
    coming_pro = []
    obj = ord.ordered_products.all()
    for product in products:
        if product in obj:
            coming_pro.append(product)
    return render(request,'ordered_products.html',{'products':coming_pro,})

#-------------------------------------------------Received Orders------------------------------------------------------------------------

def receivedOrdersView(request):
    ord = (Orders.objects.filter(sender=request.user)).order_by('-done_at')
    return render(request,'received_orders.html',{'orders':ord})

#-------------------------------------------Order details & Change Status-----------------------------------------------------------------

def orderDetailsView(request,id):
    ord=Orders.objects.get(id=id)
    name=ord.get_name()
    email=ord.get_email()
    pay_details = Payment.objects.get(order=ord)
    if request.method=='POST':
        status=request.POST['status']
        if status=='Rejected':
            for p in ord.ordered_products.all():
                p.availablity_status=True
                p.save()
        ord.status=status
        ord.save()
        return redirect('/order_details/'+str(id)+'/')
    return render(request,'order_details.html',{'ord':ord,'pay_details':pay_details,'name':name,'email':email})
