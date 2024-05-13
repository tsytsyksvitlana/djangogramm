from user_profile.models import Follower
from django.shortcuts import get_object_or_404
from typing import Any
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse

from user_profile.sites.forms import CustomUserChangeForm
from user_profile.models import User
from user_profile.models.follower import Follower
from post.models.post import Post


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("self_profile")
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class SelfProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'self_profile.html'
    context_object_name = 'posts'

    def get_queryset(self) -> list[Post]:
        return (
            Post.objects
                .filter(user=self.request.user)
                .order_by('-time_creation')
        )


class SomeoneProfileView(DetailView):
    model = User
    template_name = 'someone_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts = (
            Post.objects
            .filter(user=self.object)
            .order_by('-time_creation')
        )
        context['posts'] = posts
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() == self.request.user:
            return redirect('self_profile')
        return super().dispatch(request, *args, **kwargs)


class UserFollowView(LoginRequiredMixin, View):
    def post(self, request, user_id) -> JsonResponse:
        user_to_follow = get_object_or_404(User, pk=user_id)

        existed_follower = Follower.objects.filter(
            follower=request.user, following=user_to_follow
        ).first()

        if existed_follower:
            existed_follower.delete()
            created = False
        else:
            follower = Follower.objects.create()
            follower.follower.add(request.user)
            follower.following.add(user_to_follow)
            follower.save()
            created = True

        data = {"success": True, "created": created}
        return JsonResponse(data)
