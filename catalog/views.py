from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
from .models import Book, Author, BookInstance, Genre

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

class BookListView(generic.ListView):
    model = Book
    paginate_by= 2

class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author

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
    template_name = 'catalog/bookinstance_list_borrower_librians.html'
    def get_queryset(self):
        books = BookInstance.objects.filter(borrower__isnull=False)
        return books