import csv, io, os, math
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import BookDetail, Review
from django.views.generic import ListView, DetailView
from .forms import ReviewForm
from django.db.models import Avg
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
@permission_required('admin.can_add_log_entry')
def book_detail_upload(request):
    template = "book_detail_upload.html"
    context1 = {}

    if request.method == "GET":
        return render(request, template, context1)

    csv_file = request.FILES['file']

    data_set = csv_file.read().decode('latin-1')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, quotechar='"', delimiter=';', skipinitialspace=True):
        if(column):
            _, created = BookDetail.objects.update_or_create(
                ISBN = column[0],
                Book_Title = column[1],
                Book_Author = column[2],
                Year_Of_Publication = column[3],
                Publisher = column[4],
                Image_URL_S = column[5],
                Image_URL_M = column[6],
                Image_URL_L = column[7],
            )
        

    context = {}
    return render(request, template, context)

class BookListView(ListView):
    model = BookDetail
    template = "/browse.html"
    context_object_name = 'books'
    paginate_by = 12
    

def detail(request, pk):
    template = "book_detail.html"
    form = ReviewForm(request.POST)
  
    try:
        book = get_object_or_404(BookDetail, pk=pk)
        obj = Review.objects.filter(ISBN = pk).order_by('-date_posted')
        num = obj.aggregate(Avg('rating')).get('rating__avg')
        paginator = Paginator(obj, 3)  # 3 posts in each page
        page = request.GET.get('page')
        page_obj = paginator.page(page)

    except BookDetail.DoesNotExist:
        raise Http404("Book does not exist.")
    except Review.DoesNotExist:
        obj = None
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if obj == None:
        avg_rating = 0
    else:
        avg_rating = math.floor(num*10)/10

    if form.is_valid():
        data = Review()
        data.ISBN = BookDetail.objects.get(pk=pk)
        data.review = form.cleaned_data['comment']
        data.rating = form.cleaned_data['rate']
        current_user= request.user
        data.user_id=current_user.id
        data.save()
        messages.success(request, "Your review has ben sent. Thank you for your interest.")
        return redirect('book-detail', pk=pk)

    context = {
        'book' : book,
        'obj': obj,
        'form': form,
        'avg_rating': avg_rating,
        # 'page': page,
        'page_obj': page_obj,
    }
    return render(request, template, context)

def searchbook(request):
    template = 'search_result.html'
    query = request.GET.get('q')

    if query:
        results = BookDetail.objects.filter(Q(Book_Title__icontains=query) | Q(Book_Author__icontains=query))
    else:
        results = BookDetail.objects.all()
        
    context = {
        'book': results,
    }
    return render(request, template, context)



