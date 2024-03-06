from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from django.views.generic import ListView , DetailView , UpdateView , CreateView , FormView, DeleteView  , RedirectView
from .forms import CommentForm , PostCreateForm ,PostUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin  ,UserPassesTestMixin
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.urls import reverse

# def blog_list(request):
#     posts = Post.objects.all()

#     return render(request , 'blog/blog_list.html' , {
#         'posts' : posts,
#     })

# def blog_detail(request , slug): 
#     post_detail = get_object_or_404(Post , slug=slug)

#     return render(request , 'blog/blog_detail.html' , {
#         'post_detail' : post_detail,
#     })

class BlogList(ListView):
    model = Post
    template_name='blog/blog_list.html'
    paginate_by = 4

    def get_queryset(self, *args, **kwargs): 
        qs = super(Post, self).get_queryset(*args, **kwargs) 
        qs = qs.order_by("?") 
        return qs 

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list
    


class BlogDetail(FormMixin, DetailView ):
    model = Post
    template_name='blog/blog_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.comment_author = self.request.user
        new_comment.save()
        return super(BlogDetail, self).form_valid(form)

class DocLikeRedirect(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post , slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.like.all():
                obj.like.remove(user)
            else:
                obj.like.add(user)
        return url_

class DocReadedRedirect(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post , slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            obj.readed.add(user)
        return url_


# class PostCreateView(LoginRequiredMixin ,CreateView):
#     model = Post
#     # fields = ['title' , 'short_description' , 'description' , 'image']
#     form_class = CreatePostForm
#     template_name = 'blog/add_new_post.html'

#     def form_valid(self , form ):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

class CreateBlogView( LoginRequiredMixin , CreateView):
    model = Post
    form_class  = PostCreateForm
    template_name= 'blog/add_new_post.html'

    def form_valid(self , form ):
        form.instance.author = self.request.user
        return super().form_valid(form)



class UpdateBlogView(UserPassesTestMixin , LoginRequiredMixin ,UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name= 'blog/update_post.html'

    def form_valid(self , form ):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DeleteBlogView(UserPassesTestMixin , LoginRequiredMixin ,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


