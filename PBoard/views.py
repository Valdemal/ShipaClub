from django.shortcuts import render
from django.http.response import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Rubric, Estimation
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostForm

from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.db.models import Avg, Count
# REST-framework
from .serializers import RubricSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET',])
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.annotate(Count('post')).order_by('-post__count')
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)

@login_required
def estimations(request):
    if request.method == 'POST' and (json.loads(request.body.decode()) is not None):
        data = json.loads(request.body.decode())
        est_value = float(data['estimation_value'])
        user_id = request.user.pk
        post_id = data['post_id']
        if (est_value >= 1) and (est_value <= 10):
            message = 'Ошибка на стороне сервера!'
            try:
                est = Estimation.objects.get(post_id=post_id, user_id=user_id)
                est.value = est_value
                est.save()
                message = 'Оценка обновлена.'
            except ObjectDoesNotExist:
                est = Estimation(value=est_value,user=User.objects.get(pk=user_id),post=Post.objects.get(pk=post_id))
                est.save()
                message = 'Оценка создана.'
            finally:
                post_est = Estimation.objects.filter(post_id=post_id).aggregate(Avg('value'))['value__avg']
                data = {
                        'message': message,
                        'user':request.user.username,
                        'post_id':post_id,
                        'est_value':est_value,
                        'post_est':post_est,
                }
                return JsonResponse(data)
        else:
            pass

    elif request.method == 'GET' and request.GET:
        post_id = request.GET['post_id']
        data = {'status':False}
        try:
            data['user_est'] = Estimation.objects.get(post_id=post_id,user_id=request.user.pk).value
            data['status'] = True
        except ObjectDoesNotExist:
            pass
        finally:
            return JsonResponse(data)

    elif request.method == 'DELETE' and (json.loads(request.body.decode()) is not None):
        post_id = data = json.loads(request.body.decode())['post_id']
        data = {'status':False}
        user_id = request.user.pk
        try:
            est = Estimation.objects.get(post_id=post_id, user_id=user_id)
            est.delete()
            message = 'Оценка удалена'
            data['status'] = True
        except :
            message = 'Ошибка при удалении'
        finally:
            post_est = Estimation.objects.filter(post_id=post_id).aggregate(Avg('value'))['value__avg']
            data['message'] = message
            data['post_id'] = post_id
            data['post_est'] = post_est
            return JsonResponse(data)


    else:
        raise Http404


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('pboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def test_func(self):
        if self.request.user.is_staff or self.request.user == Post.objects.get(pk=self.get_object().pk).author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'PBoard/create.html'
    form_class = PostForm
    success_url = reverse_lazy('pboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

def by_rubric(request, rubric_name):
    posts = Post.objects.filter(rubric__name=rubric_name)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(name=rubric_name)

    paginator = Paginator(posts, 10)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'posts': page.object_list, 'page': page, 'rubrics': rubrics,
               'current_rubric': current_rubric, }

    return render(request, 'PBoard/by_rubric.html', context)


def index(request):
    posts = Post.objects.all()
    rubrics = Rubric.objects.all()
   # Paginator
    paginator = Paginator(posts, 10)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'posts': page.object_list, 'page': page,
               'rubrics': rubrics,}
    return render(request, 'PBoard/index.html', context)
