from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from student.forms import UserRegistrationForm, StudentProfileForm
from property.models import Property
from property.forms import PropertyForm
from django.db.models import Count
from django.db.models import Q, Avg
from review.models import RoommateReview, StudentReview, PropertyReview
from student.models import StudentProfile

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist')

    context = {'page': page}
    return render(request, 'student/login_register.html', context)

def logoutUser(request):
    """
    Logs out the user and redirects to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the login page.
    """
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profileForm')
        else:
            messages.error(request, 'An Error occured while registration')
    
    context = {'form': form}
    return render(request, 'student/login_register.html', context)

def profileForm(request):
    form = StudentProfileForm()
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = StudentProfileForm()
    context = {'form': form}
    return render(request, 'student/profile_form.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    userProfile = StudentProfile.objects.get(user=user)

    student_reviews = StudentReview.objects.filter(student__user=user)
    roommate_reviews_received = RoommateReview.objects.filter(roommate__user=user)

    student_total_rating_property = student_reviews.aggregate(Avg('rating'))['rating__avg']
    roommate_total_rating_received = roommate_reviews_received.aggregate(Avg('rating'))['rating__avg']

    student_reviews_count = student_reviews.count()
    roommate_reviews_received_count = roommate_reviews_received.count()

    student_reviews = student_reviews.order_by('-created_at')
    roommate_reviews_received = roommate_reviews_received.order_by('-created_at')

    total_reviews = student_reviews_count + roommate_reviews_received_count

    overall_rating = calculate_overall_rating(user)

    context = {
        'user': user,
        'userProfile': userProfile,
        'student_reviews': student_reviews,
        'roommate_reviews_received': roommate_reviews_received,
        'student_total_rating_property': student_total_rating_property,
        'roommate_total_rating_received': roommate_total_rating_received,
        'student_reviews_count': student_reviews_count,
        'roommate_reviews_received_count': roommate_reviews_received_count,
        'overall_rating': overall_rating,
        'total_reviews': total_reviews,
    }
    return render(request, 'student/profile.html', context)

@login_required(login_url='login')
def updateProfile(request, pk):
    user = User.objects.get(id=pk)
    userProfile = StudentProfile.objects.get(user=user)
    form = StudentProfileForm(instance=userProfile)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=userProfile)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {
        'form': form,
        'user': user
    }
    return render(request, 'student/update-user.html', context)


def calculate_overall_rating(student_profile):
    student_ratings = StudentReview.objects.filter(student__user=student_profile).values_list('rating', flat=True)
    roommate_ratings_received = RoommateReview.objects.filter(roommate__user=student_profile).values_list('rating', flat=True)

    all_ratings = list(student_ratings) + list(roommate_ratings_received)

    if all_ratings:
        overall_rating = sum(all_ratings) / len(all_ratings)
        return round(overall_rating, 2)
    else:
        return None

def home(request):
    properties = Property.objects.all()
    page = 'home'

    city_property_counts = Property.objects.values('city').annotate(property_count=Count('id'))
    
    context = {
        'properties': properties,
        'city_property_counts': city_property_counts,
        'page': page,
    }
    return render(request, 'student/home.html', context)

def property(request):
    properties = Property.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    properties = Property.objects.filter(
        Q(name__icontains = q) |
        Q(street_address__icontains = q) |
        Q(city__icontains = q) |
        Q(zip_code__icontains = q) |
        Q(state__icontains = q) |
        Q(country__icontains = q) |
        Q(gender__icontains = q) |
        Q(room__name__icontains = q) |
        Q(room__description__icontains = q) |
        Q(room__room_dimensions__icontains = q) |
        Q(room__price__icontains = q) |
        Q(room__occupancy__icontains = q) |
        Q(room__room_type__name__icontains = q) |
        Q(room__amenities__name__icontains = q) |
        Q(amenities__name__icontains = q) |
        Q(description__icontains = q) 
    )

    property_count = properties.count()
    context = {
        'properties': properties,
        'property_count': property_count,
    }
    return render(request, 'student/property.html', context)

def page_not_found(request):
    return render(request, 'student/404_page.html')

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    reviews = StudentReview.objects.filter(reviewer__id=pk)

    student_total_rating_property = reviews.aggregate(Avg('rating'))['rating__avg']
    reviews_count = reviews.count()
    room_count = Property.objects.get(id=pk).rooms.all().count()


    context = {
        'property': property,
        'reviews': reviews,
        'student_total_rating_property': student_total_rating_property,
        'reviews_count': reviews_count,
        'rooms_count' : room_count
    }
    return render(request, 'student/property_detail.html', context)

def about(request):
    return render(request, 'student/about.html')

def contact(request):
    return render(request, 'student/contact-page.html')

def testimonials(request):
    return render(request, 'student/testimonials.html')


