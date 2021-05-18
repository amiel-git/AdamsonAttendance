from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from core.forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate

import cv2
import numpy as np
import face_recognition
import base64


def index(request):

    return render(request,'index.html')


def registrationPage(request):

    registrationform = RegistrationForm()

    if request.method == 'POST':
        registrationform = RegistrationForm(request.POST,request.FILES)
        if registrationform.is_valid():

            user = registrationform.save(commit=False)

            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']

            user.save()
            return HttpResponseRedirect(reverse('core:index'))
        
        else:
            return HttpResponse(registrationform.errors)
    
    return render(request,'registration.html',context={'form':registrationform})


def loginView(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email,password=password)

        if user:
            login(request,user)
            print("credentials accepted")
            return HttpResponseRedirect(reverse('core:face'))

    return render(request,'login.html')


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:login'))


def faceRecognitionView(request):
    test_img = face_recognition.load_image_file(f'media/{request.user.profile_image}')
    test_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2RGB)
    face_loc = face_recognition.face_locations(test_img)[0]
    encode_face = face_recognition.face_encodings(test_img)[0]
    cap = cv2.VideoCapture(0)

    success,img =cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) #Scale down the image
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    face_loc = face_recognition.face_locations(imgS)
    try:
        imgS_encoding = face_recognition.face_encodings(imgS)[0]
        results = face_recognition.compare_faces([encode_face],imgS_encoding)
        if results[0]:
            cap.release()
            return HttpResponseRedirect(reverse('core:index'))
        
        else:
            cap.release()
            return HttpResponseRedirect(reverse('core:logout'))
    except:
        cap.release()
        return HttpResponseRedirect(reverse('core:logout'))

def faceCapture(request):

    if request.method == "POST":
        url = request.POST.get('url')
        url_decoded = b64decode(url.encode())
        content = ContentFile(url_decoded)