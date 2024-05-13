from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView
)

from comment.models.comment import Comment
from post.models.image import Image
from post.models.like import Like
from post.models.post import Post
from post.models.tag import Tag
from user_profile.models.follower import Follower


class HomeView(ListView):
    paginate_by = 3
    model = Post
    template_name = 'home.html'
    ordering = ['-time_creation']


class FeedView(ListView):
    model = Post
    template_name = 'feed.html'

    def get_queryset(self):
        current_user = self.request.user
        following_users = Follower.objects.filter(
            follower=current_user
        ).values_list('following', flat=True)
        queryset = Post.objects.filter(user__in=following_users)
        queryset = queryset.prefetch_related(
            'likes').annotate(likes_count=Count('likes'))
        return queryset.order_by('-time_creation')


class PostDetail(ListView):
    model = Comment
    template_name = 'post_detail.html'
    context_object_name = 'comments'

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        context['post'] = post
        context['is_liked'] = post.view_is_liked(self.request.user)
        for comment in context['comments']:
            comment.is_liked = comment.is_liked(self.request.user)
        return context


class AddPostView(LoginRequiredMixin, CreateView):
    template_name = 'add_post.html'
    model = Post
    fields = ['description']

    def form_valid(self, form):
        description = form.cleaned_data['description']
        images = self.request.FILES.getlist('images')
        _tags = self.request.POST.get('tags', '')
        post = Post.objects.create(
            description=description, user=self.request.user
        )
        for image in images:
            Image.objects.create(post=post, image=image)
        for tag_name in _tags.split(','):
            tag_name = tag_name.strip()
            tag, _ = Tag.objects.get_or_create(tag=tag_name)
            post.tags.add(tag)

        return redirect('post_detail', pk=post.pk)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit_post.html'
    fields = ['description']

    def form_valid(self, form):
        description = form.cleaned_data['description']
        _tags = self.request.POST.get('tags', '')
        form.instance.user = self.request.user
        form.save()

        post = form.instance
        post.tags.clear()

        for tag_name in _tags.split(','):
            tag_name = tag_name.strip()
            tag, _ = Tag.objects.get_or_create(tag=tag_name)
            post.tags.add(tag)

        return redirect('post_detail', pk=post.pk)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, post_id) -> JsonResponse:
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Post),
            object_id=post.id
        )
        data = {"success": True, "created": created}
        if not created:
            like.delete()
        return JsonResponse(data)
