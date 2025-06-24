from django.shortcuts import render,redirect,get_object_or_404
from main.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def post_list(request):
    query =request.GET.get('q')
    if request.user.is_authenticated:
        your_posts = Post.objects.filter(user=request.user)
        public_posts = Post.objects.exclude(user=request.user)
    else:
        your_posts = None  
        public_posts = Post.objects.all()  
    #  for search query through title of post and render it at top
    if query:
        # for your_post
        match_yours = your_posts.filter(title__icontains=query)
        unmatch_yours = your_posts.exclude(title__icontains=query)
        your_posts = list(match_yours)+list(unmatch_yours)
        
        # for public post
        match_public = public_posts.filter(title__icontains=query)
        unmatch_public = public_posts.exclude(title__icontains=query)
        public_posts = list(match_public)+list(unmatch_public)

    context = {
        'your_posts': your_posts,
        'public_posts': public_posts,
        'query':query,
    }
    return render(request, 'post_list.html', context)

@login_required
def post_create(request):
    if not request.user.is_authenticated: 
        messages.warning(request,'login frist to create a post')
        return redirect('post_list')
    
    if request.method == "POST":
        title = request.POST.get('title')
        # to render image or any files from database
        image = request.FILES.get('image')
        content= request.POST.get('content')
        ins = Post(title= title, image=image,content=content,user=request.user)
        ins.save()
        return redirect('post_list')
    else:
      return render(request,'post_create.html')

@login_required
def edit_post(request,post_id):
    # user = request.user
    post=get_object_or_404(Post,pk=post_id ,user=request.user)
    if request.method == "POST":
        title= request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        # if user want to change on only one of thes field only that will change remaining will same as it as previous
        if title:
            post.title = title
        if image:
            post.image = image
        if content:
            post.content = content
        post.save()
        return redirect('post_list')
    else:
        return render(request,'post_create.html',{'post':post})
@login_required
def delete_post(request, post_id):
     post = get_object_or_404(Post,pk=post_id,user=request.user)
     if request.method == "POST":
         post.delete()
         return redirect('post_list')
     else:
         return render(request,'delete_post.html')
     

def register_view(request):
    if request.method =="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error =False
        if User.objects.filter(username=username).exists():
            user_data_has_error=True
            messages.error(request,'Username alrady exits')
        if User.objects.filter(email=email).exists():
            user_data_has_error=True
            messages.error(request,'Email alrady exits')
        try:
            validate_password(password,user=None)
        except ValidationError as e:
            user_data_has_error= True
            for error_message in e.messages:
                messages.error(request,error_message)

        if user_data_has_error:
            return redirect('register_view')
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.is_active=True
            user.is_staff=True
            user.is_superuser=True
            user.save()
            return redirect('login_view')

    return render(request,'registration/register.html')


def login_view(request):
    if request.method == "POST":
        # not django defualt systen only authenticate through username and password not through email and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('post_list')
        else:
            messages.error(request,'Invalid username or password try again !')
            return redirect('login_view')
    else:
     return render(request,'registration/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('post_list')


    