from django.utils import timezone
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from upload_form.models import FileNameModel
from django.conf import settings
import sys, os


# Create your views here.

UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../static/pdf/'

#Ccase class @method_decorator(login_required, name='dispatch')
@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()[:5]
    return render(request, 'blog/post_list.html', {'posts':posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def school(request):
    return render(request, 'blog/school.html')

@login_required
def post_school(request, s_year):
    posts = Post.objects.filter(school_year=s_year).order_by('published_date').reverse()
    return render(request,'blog/post_school.html',{'posts':posts})


@login_required
def edit(request):
    if request.method != 'POST':
        return render(request,'blog/form.html')
    
    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

    insert_data = FileNameModel(file_name = file.name)
    insert_data.save()
    
    #title = request.POST.lists()
    #title = request.POST.values().__getitem__()
    
    print(title)
    
    return render(request, 'blog/complete.html')

def fin(request):
    return render(request, 'blog/complete.html')
