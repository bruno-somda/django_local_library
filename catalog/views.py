import datetime
from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'index.html', context=context)

def renew_book_librarian(request,pk):

    book_instance = get_object_or_404(BookInstance,pk=pk)
    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()
            return HttpResponseRedirect(reverse("all-borrowed"))
    else :
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks =3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form":form,
        "book_instance": book_instance,
        }
    return render(request,"catalog/renew_book_librarian.html",context)


class BookListView(generic.ListView):
    model = Book
    

class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by=10
class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    model= BookInstance
    login_url ="/login/"
    redirect_field_name = 'redirect_to'
    template_name = 'catalog/bookinstance_list_borrower_user.html'
    paginate_by=1

    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower = self.request.user)
                                .filter(status__exact= 'o')
                                .order_by('due_back')
        )

class LoanedBooksByLibriansListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
    login_url ="login/"
    redirect_field_name = 'redirect_to'
    permission_required = "catalog.can_mark_returned"
    model= BookInstance
    paginate_by=5
    template_name = 'catalog/bookinstance_list_borrower_librians.html'
    def get_queryset(self):
        books = BookInstance.objects.filter(borrower__isnull=False)
        return books

class AuthorCreate(generic.CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}

class AuthorUpdate(generic.UpdateView):
    model = Author
    fields="__all__"

class AuthorDelete(generic.DeleteView):
    model= Author
    success_url= reverse_lazy('authors')

    def form_valid(self,form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete",kwargs={'pk':self.object.pk})
            )

class BookCreate(generic.CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn','genre','language']

class BookUpdate(generic.UpdateView):
    model = Book
    fields="__all__"
    
class BookDelete(generic.DeleteView):
    model = Book
