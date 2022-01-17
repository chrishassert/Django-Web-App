from django.urls import path

from . import views
from .views import DisplayUserListings, ListingList, listingdetail, DisplayListingsRemove


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    #path('sell/', views.sell, name='sell'),
    path('login/', views.login, name='login'),
    path('listing/', views.listing, name="listing"),
    path('sell/', DisplayUserListings.as_view(), name='sell'),
    path('listings/', ListingList.as_view()),
    path('listings/<int:id>/', listingdetail, name='listingdetail'),
    path('paymentSuccess.html/', views.paymentSuccess.as_view(), name='success'),
    path('message/', views.SendMessageView.as_view(), name="send_message"),
    path('inbox/', views.InboxView.as_view(), name="inbox"),
    path('message/', views.message, name='message'),
    path('removeListing/', DisplayListingsRemove.as_view(), name = 'removeListing'),

    # This one is for later when we create a database
    # path('<int:bookid>/', views.booklist, name='booklist')
]