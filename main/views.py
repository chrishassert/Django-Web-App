from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .forms import *
from django.views.generic import *
from .models import *
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
import datetime
import django.contrib.auth
from django.db.models import Q

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'main/login.html')

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searchedState = request.POST['inputState']
            searchedWord = request.POST['input']
            if searchedState == 'Title':
                searchedList = Listing.objects.all().filter(book_title__icontains=searchedWord)
            elif searchedState == 'Author':
                searchedList = Listing.objects.all().filter(author__icontains=searchedWord)
            elif searchedState == 'Course':
                searchedList = Listing.objects.all().filter(book_course__icontains=searchedWord)
            elif searchedState == 'ISBN':
                searchedList = Listing.objects.all().filter(isbn=searchedWord)
            return render(request, 'main/home.html', {'searchedList': searchedList, 'searched': True})

        else:
            searchedList = Listing.objects.all()
            return render(request, 'main/home.html', {'searchedList': searchedList, 'searched': False})
    else:
        return redirect('/login')

def profile(request):
    # Profile.objects.filter(user=request.user).update(phone_number=request.POST["phoneNumber"])
    if request.user.is_authenticated:
        if request.method == 'POST':        
            if 'phoneNumber' in request.POST:
                if(len(request.POST['phoneNumber']) == 10):
                    Profile.objects.filter(user=request.user).update(phone_number=request.POST["phoneNumber"])
            else:
                uploaded_file = request.FILES['document']
                store = FileSystemStorage('textexchange/uploads/'+str(request.user))
                store.save(uploaded_file.name, uploaded_file)
                Profile.objects.filter(user=request.user).update(profileImage=str(request.user)+'/'+str(uploaded_file))
        userid = request.user
        phonenumber = Profile.objects.get(user=request.user).phone_number
        if Profile.objects.get(user=request.user).profileImage:
            profileImage = Profile.objects.get(user=request.user).profileImage.url
        else:
            profileImage = "https://www.indiaspora.org/wp-content/uploads/2018/10/image-not-available.jpg"
        return render(request, 'main/profile.html', {'user': userid, 'phonenumber': phonenumber, 'profileImage': profileImage})
    else:
        return redirect('/login')

def sell(request):
    if request.user.is_authenticated:
        return render(request, 'main/sell.html')
    else:
        return redirect('/login')

# need to fix redirect
def listing(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # form = ListingForm(request.POST, request.FILES)
            # # print(form)
            # if form.is_valid(): 
            #     print("working")
            #     newform = form.save(commit=False)
            #     newform.userid = Profile.objects.get(user=request.user)
            #     newform.save()
            #     return redirect('/sell/')
            listing = Listing()
            # listing.book_image = request.FILES['book_image']
            listing.seller_name = request.POST['seller_name']
            listing.book_title = request.POST['book_title']
            listing.author = request.POST['author']
            listing.isbn = request.POST['isbn']
            listing.book_course = request.POST['book_course']
            listing.price = request.POST['price']
            listing.book_description = request.POST['book_description']
            listing.userid = Profile.objects.get(user=request.user)
            listing.save()
            if 'book_image' in request.FILES:
                uploaded_file = request.FILES['book_image']
                store = FileSystemStorage('textexchange/uploads/textbook/'+str(request.user))
                store.save(uploaded_file.name, uploaded_file)
                Listing.objects.filter(book_title=request.POST['book_title'], userid=Profile.objects.get(user=request.user)).update(book_image='textbook/'+str(request.user)+'/'+str(uploaded_file))
            return redirect('/sell')
        # form = ListingForm()
        return render(request, 'main/listing.html')
    else:
        return redirect('/login')
        
# Gets to the payment page
class PaymentView(TemplateView):
    template_name = 'main/listings.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.RAVE_PUBLIC_KEY
        context['price'] = 1
        return context

# Page to indicate successful payment
class paymentSuccess(TemplateView):
    template_name = 'main/paymentSuccess.html'

# displays the listings that a user created
class DisplayUserListings(ListView):
    template_name = 'main/sell.html'

    def get(self, request, *args, **kwargs):
        # checks to see if user is logged in before trying to access Profile
        if(request.user.is_authenticated):
            form = ListingForm()
            id = Profile.objects.get(user=request.user)
            listings = Listing.objects.all().filter(userid=id)
            args = {'form': form, 'listings': listings}
            return render(request, self.template_name, args,)
        else:
            return redirect('/login')

# displays the listings to remove
class DisplayListingsRemove(ListView):
    template_name = 'main/removeListing.html'

    def get(self, request, *args, **kwargs):
        # checks to see if user is logged in before trying to access Profile
        if(request.user.is_authenticated):
            # deletes a listing
            if (request.GET.get('DeleteButton')):
                id = Profile.objects.get(user=request.user)
                Listing.objects.filter(book_title = request.GET.get('DeleteButton'), userid=id).delete()
                return redirect('/removeListing/')
            form = ListingForm()
            id = Profile.objects.get(user=request.user)
            listings = Listing.objects.all().filter(userid=id)
            args = {'form': form, 'listings': listings}
            return render(request, self.template_name, args,)
        else:
            return redirect('/login')

# displays listing on individual page

class ListingList(ListView):
    model = Listing

def listingdetail(request,id):
    if request.user.is_authenticated:    
        listing = Listing.objects.get(id = id)
        return render(request, 'main/listings.html', {'listing': listing})
    else:
        return redirect('/login')

def message(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ListingForm(request.POST)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.userid = Profile.objects.get(user=request.user)
                newform.save()
                return redirect('/sell/')
        form = ListingForm()
        return render(request, 'main/listing.html', {'form': form})
    else:
        return redirect('/login')

class InboxView(View):
    def get(self, request, *args, **kwargs):
        args = {}
        if (request.user.is_authenticated):
            people = Map.objects.all().filter(Q(user=request.user) | Q(send=request.user)).order_by('-pub_date')
            num_results = Map.objects.all().filter(Q(user=request.user) | Q(send=request.user)).order_by('-pub_date').count()
            if(num_results!=0):
                args = {'people': people, 'user':request.user}
            return render(request, 'main/inbox.html', args)
        else:
            return redirect('/login')

    def post(self, request):
        if (request.user.is_authenticated):
            other = User.objects.all().filter(username=request.POST['rec'])
            #other = User.objects.get(username=request.POST['rec'])
            o = other.last()
            if(o):
                m = Message.objects.all().filter(Q(sender=request.user, recipient=o) | Q(sender=o, recipient=request.user)).order_by('-pub_date')
                args = {'m': m, 'o': o}
                return render(request, 'main/conversation.html', args)
            return render(request, 'main/message.html')
        else:
            return redirect('/login')

class SendMessageView(View):
    def get(self, request):
        args = {}
        if (request.user.is_authenticated):
            people = Map.objects.all().filter(user=request.user).order_by('-pub_date');
            args = {'people': people}
            return render(request, 'main/message.html', args, )
        else:
            return redirect('/login')

    #When I submit it will do the post
    def post(self, request):
        args = {}
        if (request.user.is_authenticated):
            other = User.objects.all().filter(username=request.POST['recipient'])
            o = other.last()
            if (o):
                sh = Map.objects.all().filter(Q(user=request.user, send = o) | Q(send=request.user, user = o))
                s = sh.first()
                if (s):
                    s.pub_date = django.utils.timezone.now()
                    s.save()
                else:
                    map = Map.objects.create(user=request.user, send=o, pub_date=django.utils.timezone.now())
                    map.save()
                mess = Message.objects.create(sender=request.user, recipient=o, message=request.POST['textbox'],
                                              pub_date=django.utils.timezone.now())
                mess.save()
                # m = Message.objects.all().filter(recipient=o)
                m = Message.objects.all().filter(Q(sender=request.user, recipient=o) | Q(sender=o, recipient=request.user)).order_by('-pub_date')
                args = {"other": o, 'm': m}
            else:
                b = bool(True)
                args = {"boolean" : b}
            return render(request, 'main/message.html', args, )
        else:
            return redirect('/login')
            

def message(request):
    args = {}
    if (request.user.is_authenticated):
        other = User.objects.all().filter(username=request.POST['recipient'])
        o = other.first()
        if(o):
            sh = Map.objects.all().filter(Q(user=request.user, send = o) | Q(send=request.user, user = o))
            s = sh.first()
            if(s):
                s.pub_date=django.utils.timezone.now()
                s.save()
            else:
                maps = Map.objects.create(user=request.user,send=o,pub_date=django.utils.timezone.now())
                maps.save()
            mess = Message.objects.create(sender=request.user, recipient=o, message=request.POST['textbox'],
                                             pub_date=django.utils.timezone.now())
            mess.save()
            # m = Message.objects.all().filter(recipient=o)
            m = Message.objects.all().filter(Q(sender=request.user, recipient=o) | Q(sender=o, recipient=request.user)).order_by('-pub_date')
            args = {"other": o, 'm': m}
        return render(request, 'main/message.html', args, )
    else:
        return redirect('/login')
