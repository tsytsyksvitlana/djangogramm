from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView
)
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from post.models.like import Like
from comment.models.comment import Comment


class AddCommentView(LoginRequiredMixin, CreateView):
    template_name = 'add_comment.html'
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        post_id = self.kwargs['post_id']
        form.instance.post_id = post_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})


class EditCommentView(LoginRequiredMixin, UpdateView):
    template_name = 'edit_comment.html'
    model = Comment
    fields = ['text']

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post_id})


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post_id})


class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, comment_id) -> JsonResponse:
        comment = get_object_or_404(Comment, pk=comment_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=comment.id
        )
        data = {"success": True, "created": created}
        if not created:
            like.delete()
        return JsonResponse(data)