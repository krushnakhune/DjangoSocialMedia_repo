from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import (ListView,UpdateView,DeleteView,DetailView,CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentForm


def home(request):
    context={'posts':Post.objects.all().order_by('-date_posted')}
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if post.author==self.request.user:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if post.author==self.request.user:
            return True
        else:
            return False

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

def blog_python_view(request):
    return render(request,'blog/python.html')

def latestlistview(request):
    latest_posts=Post.objects.all().order_by('-date_posted')[:3]
    return render(request,'blog/latest_posts.html',{'latest_posts':latest_posts})

def questionsview(request):
    return render(request,'blog/questions_post.html')

#def post_detail_view(request,pk):
 #   post=Post.objects.get(id=pk)
  #  comments = post.comments.filter(active=True)
   # if request.method == "POST":
    #    form = CommentForm(request.POST)
     #   if form.is_valid():
      #      new_comment = form.save(commit=False)
       #     new_comment.post = post
        #    new_comment.save()
    #else:
     #   form = CommentForm()
    #return render(request,'blog/post.html',{'form':form,'comments':comments,'post':post})

def comments(request,pk):
    post=get_object_or_404(Post,id=pk)
    comments=post.comments.filter(active=True)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        form=CommentForm()
    return render(request,'blog/comments.html',{'comments':comments,'form':form})
