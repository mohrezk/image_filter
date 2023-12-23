from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View
from django.http.response import HttpResponse
from .models import Image
from accounts.models import CustomUser
from .process_image import Process 
from .classify_image import Classify
import os 
from random import randint
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"
    
class ImageListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'images/image_list.html'
    context_object_name = 'images'
    ordering = ['-uploaded_at']

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    template_name = 'images/image_create.html'
    fields = ['image']  
    success_url = reverse_lazy('list_images')  

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ImageDetailView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'images/image_detail.html'
    context_object_name = 'image'



class ApplyFilterView(View):

    def post(self, request, id, *args, **kwargs):
        image = get_object_or_404(Image, pk=id)

        selected_filter = request.POST.get('imageProcessing')
        
        # img = [image.image.url[1:]]
        
        img = image.image.url[1:]
        
        process = Process(selected_filter, request.user.id)

        new_img = process.process_image(img)
        
        new_image =  Image()
        if not Image.objects.filter(image=new_img[5:]).exists():
            new_image.image = new_img[5:]
            new_image.user = get_object_or_404(CustomUser, id= request.user.id)
            new_image.processed = True
            new_image.save()


        
        return HttpResponse(f'<img src="/{new_img}" width="200" height="200">')
        

class ApplyFilterOnSelectedView(View):
    def post(self, request, *args, **kwargs):
        selected_image_ids = request.POST.getlist('selectedImages')
        selected_filter = request.POST.get('imageProcessing')

        processed_images = []

        for image_id in selected_image_ids:
            image = get_object_or_404(Image, id=image_id)
            img_path = image.image.url[1:]

            processed_images.append(img_path)


        process = Process(selected_filter, request.user.id)

        new_images = process.process_image(processed_images)

        for img in new_images:
            if not Image.objects.filter(image=img[5:]).exists():
                new_image =  Image()
                new_image.image = img[5:]
                new_image.user = get_object_or_404(CustomUser, id= request.user.id)
                new_image.processed = True
                new_image.save()
 
        

        return HttpResponse('<script>window.location.reload();</script>')
        # return HttpResponse(', '.join(f'<img src="/{img}" width="200" height="200">' for img in new_images))


class ImageListClassifyView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'images/classify_list.html'
    context_object_name = 'images'
    ordering = ['-uploaded_at']

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
    

class ClassifyImageView(View):
    def post(self, request, id):
        folder = randint(10000000, 99999999) 
        classify = Classify(folder_name=f"{folder}")

        image = get_object_or_404(Image, pk=id)
        img = image.image.url[1:]

        result = classify.classify_image(img)

        responseHTML =  f"<ul class='ul-features'>{' - '.join([f'<li>{value}</li>' for value in result])}</ul>" + "<div class='imageResult'>"  f"<img src='/media/{folder}/{os.path.basename(img)}'>" +  "</div>"
        if result:
            return HttpResponse(responseHTML)
        return  HttpResponse(f'<h1>No Data</h1>')
    

class ClassifySelectedImagesView(View):
    def post(self, request):


        selected_image_ids = request.POST.getlist('selectedImages')
        folder = randint(10000000, 99999999) 
        classify = Classify(folder_name=f"{folder}")

        images = []

        for image_id in selected_image_ids:
            image = get_object_or_404(Image, id=image_id)
            img_path = image.image.url[1:]

            images.append(img_path)


        result = classify.classify_images(images)

        # context = {'result': result}

        # return render(request, 'classify_list.html', context)

        j = 0
        responseHTML = ""
        for i in result:
            div = "<div class='imageResult-view'>"

            # for j in i:
            #     r = f"<div class='result'>{j} </div>"
            #     div += r

            div += f"<ul class='ul-features'>{' - '.join([f'<li>{value}</li>' for value in i])}</ul>"
            div += f"<img class='img-view' src='/media/{folder}/{os.path.basename(images[j])}'>"
            j += 1
            div += "</div>"
            responseHTML += div
            
        print(responseHTML)

        if result:
            return HttpResponse(f'{responseHTML}')
        return  HttpResponse(f'<h1>No Data</h1>')