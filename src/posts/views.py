from django.shortcuts import render
from .models import Post
from django.http import JsonResponse
from .forms import PostForm
from profiles.models import Profile

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
    context = {
        # 'qs': qs,
        'form': form,
    }
    return render(request, 'posts/main.html', context)

# with each button click we are going to run this function view and add new posts by slicing with lower-upper boundaries
def load_post_data_view(request, num_posts):
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


def hello_world_view(request):
    return JsonResponse({'text': 'hello world x2'})
