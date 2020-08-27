from django.http import Http404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from django.http import *
from django.shortcuts import render
from .forms import AuthorsForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book


def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'На складе')
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.

    # Количество посещений этого view, подсчитанное в переменной session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри переменной context
    return render(request, 'index.html',
                  context={'num_books': num_books, 'num_instances': num_instances,
                           'num_instances_available': num_instances_available, 'num_authors': num_authors,
                           'num_visits': num_visits},
                  )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


# получение данных из БД и загрузка шаблона authors_add.html
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, "catalog/authors_add.html", {"form": authorsform, "author": author})


# сохранение данных об авторах в БД
def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")


# удаление авторов из БД
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


# изменение данных в БД
def edit(request, id):
    try:
        author = Author.objects.get(id=id)
        if request.method == "POST":
            author.first_name = request.POST.get("first_name")
            author.last_name = request.POST.get("last_name")
            author.date_of_birth = request.POST.get("date_of_birth")
            author.date_of_death = request.POST.get("date_of_death")
            author.save()
            return HttpResponseRedirect("/authors_add/")
        else:
            return render(request, "/edit.html/", {"author": author})
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


# изменение данных в БД
def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request, "edit1.html", {"author": author})


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


'''
def authors_add(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")  # получить значения поля Имя
        last_name = request.POST.get("last_name")  # значения поля Возраст
        date_of_birth = request.POST.get("date_of_birth")  # получить значения поля Имя
        date_of_death = request.POST.get("date_of_death")  # значения поля Возраст
        output = "<h2>Пользователь</h2><h3>Имя - {0}, Фамилия – {1}, Дата раждения- {2}, Дата смерти- {3} </h2 >"\
            .format(first_name, last_name, date_of_birth, date_of_death)
        return HttpResponse(output)
    else:
        authorsform = AuthorsForm()
        return render(request, "catalog/authors_add.html", {"form": authorsform})
'''


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Универсальный класс представления списка книг,
    находящихся в заказе у текущего пользователя.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')


'''
def authors(request):
    first_name = Author.objects.all()
    last_name = Author.objects.all()
    date_of_birth = Author.objects.all()
    date_of_death = Author.objects.all()
    # Отрисовка HTML-шаблона authors.html с данными внутри переменной context
    return render(request, 'authors.html',
                  context={'first_name': first_name, 'last_name': last_name,
                           'date_of_birth': date_of_birth, 'date_of_death': date_of_death},
                  )
'''
# python manage.py runserver
