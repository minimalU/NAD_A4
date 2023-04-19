from django.shortcuts import render
from .models import Post, Photo
from django.http import JsonResponse, HttpResponse
from .forms import PostForm
from profiles.models import Profile
from .utils import action_permission

# is_ajax() is depreciated
from django.http import HttpResponse 
from django.views.decorators.http import require_http_methods


#from django.core import serializers

# Create your views here.

def post_list_and_create(request):
    # Adding a form to the Modal
    form = PostForm(request.POST or None)
    # qs = Post.objects.all()
    # if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if form.is_valid():
            author = Profile.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            return JsonResponse({
                'title': instance.title,
                'body': instance.body,
                'author': instance.author.user.username,
                'id': instance.id
            })
        
    context = {
        # 'qs': qs,
        'form': form,
    }
    return render(request, 'posts/main.html', context)


# Creating the Post Detail Page
def post_detail(request, pk):
    obj = Post.objects.get(pk=pk)
    form = PostForm()

    context = {
        'obj': obj,
        'form': form,
    }

    return render(request, 'posts/detail.html', context)


# with each button click we are going to run this function view and add new posts by slicing with lower-upper boundaries
def load_post_data_view(request, num_posts):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        visible = 3
        upper = num_posts 
        lower = upper - visible 
        size = Post.objects.all().count()
        
        qs = Post.objects.all()
        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body' : obj.body,
                'liked': True if request.user in obj.liked.all() else False,
                'count': obj.like_count,
                'author' : obj.author.user.username           
            }
            data.append(item)
        return JsonResponse({'data': data[lower:upper], 'size': size})
    
#Working on the Post Detail Page - Part 2
def post_detail_data_view(request, pk):
    obj = Post.objects.get(pk=pk)
    data = {
        'id': obj.id,
        'title': obj.title,
        'body': obj.body,
        'author': obj.author.user.username,
        'logged_in': request.user.username,
    }
    return JsonResponse({'data': data})


# Like button with ajax - part2 12:00
def like_unlike_post(request):
    # if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk=pk)
        if request.user in obj.liked.all():
            liked = False
            obj.liked.remove(request.user)
        else:
            liked = True
            obj.liked.add(request.user)
        return JsonResponse({'liked': liked, 'count': obj.like_count})


# Writing Update and Delete Views
def update_post(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        new_title = request.POST.get('title')
        new_body = request.POST.get('body')
        obj.title = new_title
        obj.body = new_body
        obj.save()
        return JsonResponse({
            'title': new_title,
            'body': new_body
        })

@action_permission
def delete_post(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        obj.delete()
        return JsonResponse({})
    return JsonResponse({'msg': 'access denied'})

# Creating the View for Image Uploading    
def image_upload_view(request):
    #print(request.FILES)
    if request.method =='POST':
        img = request.FILES.get('file')
        new_post_id = request.POST.get('new_post_id')
        post = Post.objects.get(id=new_post_id)
        Photo.objects.create(image=img, post=post)
    return HttpResponse()