from django.views.generic.base import RedirectView
from Rare_app.form import PassResetForm, SetNewPassword
from django.urls import path
from Rare_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
urlpatterns = [

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/images/favicon.ico'))),
    path('',views.homeView,name="home"),
    path('register/',views.registrationView,name="register"),
    path('login/',views.loginView,name="login"),
    path('changepassword/',views.changePasswordView,name="changepassword"),
    path('logout/',views.logoutView,name="logout"),
    path('newpost/',views.newPostView,name="newpost"),
    path('newblog/',views.newBlogView,name="newblog"),
    path('posts/<int:id>/',views.categoryPostView,name="posts"),
    path('postdetails/<int:id>/',views.FAQView,name="postdetails"),
    path('allposts',views.allPostView,name="allposts"),
    path('artistdetails/<int:id>/',views.artistDetailsView,name="artistdetails"),
    path('manageartist/',views.manageArtistView,name="manageartist"),
    path('approveartist/<int:id>/',views.approveArtistView,name="approveartist"),
    path('refuseartist/<int:id>/',views.rejectArtistView,name="rejectartist"),
    path('likepost/<int:id>/',views.LikePostView,name="likepost"),
    path('myposts',views.mypostsView,name="myposts"),
    path('editpost/<int:id>/',views.editPostView,name="editpost"),
    path('editblog/<int:id>/',views.editBlogView,name="editblog"),
    path('deletepost/<int:id>/',views.deletePostView,name="deletepost"),
    path('deleteblog/<int:id>/',views.deleteBlogView,name="deleteblog"),
    path('viewartist/<int:id>/',views.viewArtist,name="viewartist"),
    path('myfaqs',views.myFAQsView,name="myfaqs"),
    path('deletefaq/<int:id>/',views.deleteFAQView,name="deletefaq"),
    path('finalizeaddress/<int:id>/',views.finalizeAddressView,name="finalizeaddress"),
    path('editfaq/<int:id>/',views.editFAQView,name="editfaq"),
    path('removeproduct/<int:id>/',views.removeFromCartView,name="removeproduct"),
    path('addproduct/<int:id>/',views.addToCartView,name="addproduct"),
    path('editprofile',views.editProfileView,name="editprofile"),
    path('search',views.searchView,name="search"),
    path('cart',views.cartView,name="cart"),
    path('aboutus',views.aboutUsView,name="aboutus"),
    path('contactus',views.contactUsView,name="contactus"),
    path('checkout',views.checkoutView,name="checkout"),
    path('payment/<int:id>/',views.paymentView,name="payment"),
    path('order_details/<int:id>/',views.orderDetailsView,name="orderdetails"),
    # path('changeorderstatus/<int:id>/',views.changeOrderStatusView,name="changeorderstatus"),
    path('saveorder/<int:id>/',views.saveOrderView,name="saveorder"),
    path('paymentsuccess/<int:id>/',views.paymentSuccessView,name="paymentsuccess"),
    path('orderedproducts/<int:id>/',views.orderedProductsView,name="orderedproducts"),
    path('blogs',views.latestblogsView,name="blogs"),
    path('myblogs',views.myblogsView,name="myblogs"),
    path('myorders',views.myOrdersView,name="myorders"),
    path('receivedrders',views.receivedOrdersView,name="receivedorders"),
    path('selectaddress',views.selectAddressView,name="selectaddress"),






    #password reset urls
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=PassResetForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=SetNewPassword), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)