from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
import json

# main page function

def index(request):
    all_places = place_information.objects.all()

    for i in all_places:
        print(i.place_type)
        # if i.end_date_time and i.end_date_time >= datetime.now():
        if i.place_type=="temporary" and i.end_date_time and i.end_date_time.strftime('%Y-%m-%d %H:%M:%S')<datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            i.delete()



    return redirect("show")


# perticular place

def place(request, id):
    focused_place = place_information.objects.get(id=id)
    context = {
        'place': focused_place
    }
    return render(request, 'place.html', context)


# Show all pins places with info
def show(request):
    context = {}

    if 'type' in request.GET and request.GET['type'] == 'temporary':
        context['all_places'] = place_information.objects.filter(place_type='temporary')
    elif 'type' in request.GET and request.GET['type'] == 'permanent':
        context['all_places'] = place_information.objects.filter(place_type='permanent')
    else:
        context['all_places'] = place_information.objects.all()
    return render(request, 'show.html', context)


# add pin place

def add(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        place_image = request.FILES['image']
        place_name = request.POST['lc_name']
        place_description = request.POST['lc_details']
        place_longitude = request.POST['longitude']
        place_latitude = request.POST['latitude']
        place_ratings = request.POST['lc_rating']
        place_type = request.POST['lc_type']

        # end_datetime = request.POST['lc_end_date']

        if 'lc_start_date' in request.POST and 'lc_end_date' in request.POST and request.POST['lc_start_date']!="" and request.POST['lc_end_date']!="":
            start_date_time = request.POST['lc_start_date']
            end_date_time = request.POST['lc_end_date']

            print(type(start_date_time))
            print(end_date_time)

            new_place = place_information(
                place_image=place_image, 
                place_name=place_name,
                place_description=place_description,
                place_longitude=place_longitude,
                place_latitude=place_latitude,
                place_ratings=place_ratings,
                place_type=place_type,
                added_by=request.user,
                start_date_time=start_date_time,
                end_date_time=end_date_time
            )
            new_place.save()

            print("Going into temporary condition")


        else:
            new_place = place_information(
                place_image=place_image, 
                place_name=place_name,
                place_description=place_description,
                place_longitude=place_longitude,
                place_latitude=place_latitude,
                place_ratings=place_ratings,
                place_type=place_type,
                added_by=request.user,
            )

            new_place.save()





        return redirect("index")

    return render(request, 'main.html')


def myplaces(request):
    if not request.user.is_authenticated:
        return redirect("login")

    all_places = place_information.objects.filter(added_by=request.user)

    context = {
        'all_places': all_places
    }

    return render(request, 'places.html', context)


def removing(request, id):
    try:
        target_place = place_information.objects.get(id=id)
        target_place.delete()
        return redirect("myplaces")
    except:
        return redirect("myplaces")

# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered number already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)



    return render(request, "signup.html")


# function for login

def login(request):

    if request.method != "POST":
        return render(request, "login.html")
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(username=email, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect("index")
    else:
        messages.info(request, "Incorrect login details!")
        return redirect("login")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

