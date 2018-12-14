from django.shortcuts import render, redirect , HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from keras.models import load_model

import numpy as np
from keras.preprocessing import image
import json


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        request.session['q'] = uploaded_file_url
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })



    return render(request, 'core/simple_upload.html')

def model(request):
    model = load_model('/home/siddhesh/Desktop/P/pothole_model.h5')
    verify_url =  request.session['q']
    test_image = image.load_img(verify_url[1:], target_size=(150, 150))

    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    a = model.predict(test_image)

    return render(request , 'core/model.html',{'a': a})


def form(request):
    return render(request, 'core/form.html',{})

def upload(request):
    image_path = []
    label=[]
    image_test_path = []
    model = load_model('/home/siddhesh/Desktop/P/pothole_model.h5')
    for count , x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open('/home/siddhesh/Desktop/a/AxisBankAIChallenge/media/file_' + str(count) + ".jpg", 'wb+') as destination:
                image_path.append("../media/file_"+str(count)+".jpg")
                image_test_path.append(destination.name)
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)

    for x in image_test_path:
        test_image = image.load_img(x, target_size=(150, 150))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        y_pred = model.predict(test_image)
        label.append(y_pred[0][0])

    final = zip(image_path,label)

    image_path = json.dumps(image_path)
    label = json.dumps(image_path)
    request.session['x'] = image_path
    request.session['y'] = label
    return render(request,'core/prediction.html',{'images': final})

import csv

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Submission.csv"'

    writer = csv.writer(response)
    writer.writerow(['Image_id','Decision'])
    image_path = request.session['x']
    label = request.session['y']
    #users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    #for user in users:
    #    writer.writerow(user)

    #for image, lab in zip(image_path,label):
    #    writer.writerow([image,str(lab)])

    writer.writerow([image_path,label])
    return response