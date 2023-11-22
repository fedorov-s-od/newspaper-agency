from django.db.models.query import Q
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Newspaper
from .forms import SearchForm
from .forms import SearchForm, NewspaperCreateForm


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_newspapers": Newspaper.objects.count(),
        "num_assigned_newspaper": Newspaper.objects.filter(publishers=request.user.pk).count() if request.user.is_authenticated else 0,
    }

    return render(request, "newspaper/index.html", context=context)


class NewspaperListView(generic.ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    template_name = "newspaper/newspaper_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperCreateForm
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
