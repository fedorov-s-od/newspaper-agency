from typing import Any

from django.db.models.query import Q
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.template import loader

from .models import Newspaper, Topic
from .forms import (
    SearchForm,
    NewspaperCreateForm,
    LoginForm,
    SignUpForm,
    FilterTopicForm,
)


@login_required(login_url='/login/')
def index(request: HttpRequest) -> HttpResponse:
    context = {
        'segment': 'index',
        'num_newspapers': Newspaper.objects.count(),
        'num_redactors': get_user_model().objects.count(),
        'num_topics': Topic.objects.count(),
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='/login/')
def pages(request: HttpRequest) -> HttpResponse:
    context = {}

    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class NewspaperListView(generic.ListView):
    model = Newspaper
    context_object_name = 'newspaper_list'
    template_name = 'newspaper/newspaper_list.html'
    paginate_by = 5

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
            )

        filter_query = self.request.GET.get('by_topic', None)

        if filter_query:
            queryset = queryset.filter(topic=filter_query)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['filter_form'] = FilterTopicForm(self.request.GET)
        return context


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperCreateForm
    success_url = reverse_lazy('newspaper:newspaper-list')


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = '__all__'
    success_url = reverse_lazy('newspaper:newspaper-list')


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy('newspaper:newspaper-list')


class TopicListView(generic.ListView):
    model = Topic
    context_object_name = 'topic_list'
    template_name = 'newspaper/topic_list.html'


class RedactorListView(generic.ListView):
    model = get_user_model()
    context_object_name = 'redactor_list'
    template_name = 'newspaper/redactor_list.html'
    paginate_by = 5

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)

        if search_query:
            queryset = queryset.filter(username__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context


class RedactorDetailView(generic.DetailView):
    model = get_user_model()


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    fields = ('first_name', 'last_name', 'email')
    template_name = 'newspaper/profile.html'
    success_url = reverse_lazy('newspaper:profile')

    def get_object(self, queryset: Any = None) -> Any:
        return self.request.user


def login_view(request: HttpRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, 'accounts/login.html', {'form': form, 'msg': msg})


def register_user(request: HttpRequest) -> HttpResponse:
    msg = None
    success = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form, 'msg': msg, 'success': success},
    )
