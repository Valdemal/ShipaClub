from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import News
from django.forms import modelformset_factory
from django.contrib.auth.decorators import user_passes_test
from .forms import NewsForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.cache import cache_page # Для кэша

class NewsCreateView(UserPassesTestMixin, CreateView):
    template_name = 'Mainpage/create_news.html'
    form_class = NewsForm
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all()
        return context
    
    def test_func(self):
        return self.request.user.is_staff

class NewsDeleteView(UserPassesTestMixin,DeleteView):
    model = News
    # form_class = NewsForm
    success_url = reverse_lazy('main:index')
    template_name = 'Mainpage/delete_news.html'

    # def get_context_data(self, *args,**kwargs):
    #     context = super().get_context_data(*args,**kwargs)
    #     context['news'] = News.objects.all()
    #     return context

    def test_func(self):
        return self.request.user.is_staff


class NewsEditView(UserPassesTestMixin,UpdateView):
    model = News
    form_class = NewsForm
    success_url = reverse_lazy('main:index')
    template_name = 'Mainpage/edit_news.html'


    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['news'] = News.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_staff

@user_passes_test(lambda user: user.is_staff)
def allNews(request):
    if request.user.is_staff:
        NewsFormSet = modelformset_factory(News, fields={'title','content','image',},can_delete=True,)

        if request.method == "POST":
            formset = NewsFormSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data:
                        if form.is_valid():
                            news = form.save(commit=False)
                            news.save()
                
                formset.save(commit=False)
                for form in formset.deleted_objects:
                    form.delete()

                return redirect('main:index')
        else:
            formset = NewsFormSet()

        context = {'formset':formset}
        return render(request, 'Mainpage/allnews.html', context)
    else:
        return HttpResponseForbidden('Вам отказано в доступе')



class NewsIndexView(TemplateView):
    template_name = 'Mainpage/index.html'
    
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['news'] = News.objects.all()
        return context

@cache_page(300)
def about(request):
    return render(request,'Mainpage/about.html')


@cache_page(300)
def rules(request):
    return render(request, 'Mainpage/rules.html')
