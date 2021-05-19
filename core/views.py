from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from core.forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate

import cv2
import numpy as np
import face_recognition
from base64 import b64decode
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


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

        if user :
            login(request,user)

            #Get captured image
            url = request.POST.get('url')
            format, imgstr = url.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(b64decode(imgstr))

            myfile = f"{user.id}_testimg" +"."+ ext
            fs = FileSystemStorage(location='media/test_images/')
            fs.delete(myfile)
            fs.save(myfile,data)
            
            #Compare images
            test_img = face_recognition.load_image_file(f'media/{user.profile_image}')
            test_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2RGB)
            face_loc = face_recognition.face_locations(test_img)[0]
            encode_face = face_recognition.face_encodings(test_img)[0]

            fs = FileSystemStorage()
            imgS = face_recognition.load_image_file(f'media/test_images/{user.id}_testimg.png')
            imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
            face_loc = face_recognition.face_locations(imgS)
            try:
                imgS_encoding = face_recognition.face_encodings(imgS)[0]
                results = face_recognition.compare_faces([encode_face],imgS_encoding)
                if results[0]:
                    #cap.release()
                    return HttpResponseRedirect(reverse('core:index'))
                
                else:
                    #cap.release()
                    logout(request)
                    return HttpResponseRedirect(reverse('core:login'))
            except:
                #cap.release()
                logout(request)
                return HttpResponseRedirect(reverse('core:login'))


    return render(request,'login.html')


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:login'))

