from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .task import comment_send_email, accept_email


class MmorpgPage(ListView):
    model = Advertisements
    template_name = 'mmorpg.html'
    context_object_name = 'adverts'


class AdvertCreate(CreateView, LoginRequiredMixin):
    model = Advertisements
    template_name = 'advert_create.html'
    form_class = AdvertForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_profile'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form, advert=None):
        advert = form.save(commit=False)
        advert.author = User.objects.get(id=self.request.user.id)
        advert.save()
        return super().form_valid(form)


class AdvertDetail(DetailView):
    model = Advertisements
    template_name = 'advert_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advert = self.get_object()
        context['photo'] = advert.photo
        context['content'] = advert.content
        if Comment.objects.filter(author_id=self.request.user.id).filter(ad_id=self.kwargs.get('pk')):
            context['comments'] = 'Отозваться'
        elif self.request.user == advert.author:
            context['comments'] = 'Мои объявления'
        return context


class AdvertUpdate(UpdateView):
    template_name = 'advert_update.html'
    form_class = AdvertForm
    success_url = '/update/'
    permission_required = 'mmorpg.change_advert'

    def dispatch(self, request, *args, **kwargs):
        author = Advertisements.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Вам нужно быть создателем данного произведения для редактирования!')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisements.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/advert/' + str(self.kwargs.get('pk')))


class AdvertDelete(DeleteView, PermissionRequiredMixin):
    model = Advertisements
    template_name = 'advert_delete.html'
    success_url = reverse_lazy('mmorpg')
    permission_required = 'mmorpg.delete_advert'

    def dispatch(self, request, *args, **kwargs):
        author = Advertisements.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Стереть свое деяние может только создатель')


class Comments(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'responses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = ''
        if self.kwargs.get('pk') and Advertisements.objects.filter(id=self.kwargs.get('pk')).exists():
            title = str(Advertisements.objects.get(id=self.kwargs.get('pk')).title)
            print(title)
        context['form'] = CommentFilterForm(self.request.user, initial={'title': title})
        context['title'] = title
        if title:
            context['filter_responses'] = list(Comment.objects.filter(ad_id__title=title).order_by('-created_at'))
            context['response_ad_id'] = Advertisements.objects.get(title=title).id
        else:
            title = self.request.GET.get('title')
            if title:
                context['filter_responses'] = list(
                    Comment.objects.filter(ad_id__title=title).order_by('-created_at')
                )
            else:
                context['filter_responses'] = list(
                    Comment.objects.filter(ad_id__author_id=self.request.user).order_by('-created_at')
                )
        context['myresponses'] = list(Comment.objects.filter(author_id=self.request.user).order_by('-created_at'))
        return context

    def advert(self, request, *args, **kwargs):
        title = self.request.POST.get('title')
        if title:
            return HttpResponseRedirect('/comments?title=' + title)
        return self.get(request, *args, **kwargs)


@login_required
def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Comment.objects.get(id=kwargs.get('pk'))
        response.accepted = True
        response.save()
        accept_email.delay(response_id=response.id)
        return HttpResponseRedirect('/comments')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def response_delete(request, **kwargs):
    if request.user.is_authenticated:
        response = Comment.objects.get(id=kwargs.get('pk'))
        response.delete()
        return HttpResponseRedirect('/comments')
    else:
        return HttpResponseRedirect('/accounts/login')


class Commentt(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'commentt.html'
    form_class = CommentForm
    success_url = reverse_lazy('mmorpg')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        commentt = form.save(commit=False)
        commentt.author = User.objects.get(id=self.request.user.id)
        commentt.ad = Advertisements.objects.get(id=self.kwargs.get('pk'))
        commentt.save()
        comment_send_email.delay(comment_id=commentt.id)
        return redirect(f'/advert/{self.kwargs.get("pk")}')