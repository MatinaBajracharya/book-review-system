import csv, io, os
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import BookDetail
from django.views.generic import ListView, DetailView

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
    template = "book/book_detail.html"  
    try:
        book = get_object_or_404(BookDetail, pk=pk)
        # details = Post.objects.get(pk=pk)
        # comments = Comment.objects.filter(post=post).order_by('-id')
    except BookDetail.DoesNotExist:
        raise Http404("Book does not exist.")

        # if request.method == 'POST':
        #     comment = request.POST.get('comm') 
        #     comm_id = request.POST.get('comm_id')

        #     if comm_id:
        #         SubComment(post=post,
        #             user = request.user,
        #             comment = comment,
        #             comment_reply = Comment.objects.get(id=int(comm_id))
        #         ).save()
        #     else:
        #         Comment(post=post, user = request.user, comment=comment).save()

        # comments = []
        # for c in Comment.objects.filter(post=post):
        #     comments.append([c, SubComment.objects.filter(comment_reply = c)])

        context = {
            'book' : book,
        }
        return render(request, template, context)
