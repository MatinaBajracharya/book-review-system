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
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# recommendation
import pandas as pd 
import numpy as np 
from surprise import Reader, Dataset
from surprise import SVD
import copy

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

def book_list(request):
    template = "browse.html"
    if(request.user.is_authenticated):
        book_list_df = recommendation(request)
    else:
        columns=['id', 'ISBN', 'Book_Title', 'Image_URL_L', 'Book_Author']
        book_list_df = pd.DataFrame(columns = columns)
    populars = popular_books(request, 3)
    try:
        books = BookDetail.objects.all()
        rating = Review.objects.all()
        paginator = Paginator(books, 12)  
        page = request.GET.get('page')
        page_obj = paginator.page(page)
    except BookDetail.DoesNotExist:
        raise Http404("Book does not exist.")
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except:
        raise Http404("Something went wrong.")   

    context={
        'pred': book_list_df,
        'populars': populars,
        'books': books,
        'rating': rating,
        'page': page,
        'page_obj': page_obj,
    }

    return render(request, template, context)
    
def popular_books(request, items):
    rating_num = pd.DataFrame(list(Review.objects.filter(rating__gte = 3).values().order_by('-rating')))
    rating_num = rating_num.drop_duplicates(subset = 'ISBN_id', keep = "first")
    rating_num = rating_num.head(items)
    details = []
    columns=['id', 'ISBN', 'Book_Title', 'Image_URL_L', 'Book_Author']
    popular_isbn = rating_num['ISBN_id'].tolist()
    for i in popular_isbn:
        popular_book = BookDetail.objects.get(id = i)
        details.append([popular_book.id, popular_book.ISBN, popular_book.Book_Title,popular_book.Image_URL_L, popular_book.Book_Author])
    book_list_df = pd.DataFrame(details,columns=columns)
    return book_list_df


def detail(request, pk):
    try:
        template = "book_detail.html"
        form = ReviewForm(request.POST)
        book = get_object_or_404(BookDetail, pk=pk)
        obj = Review.objects.filter(ISBN = pk).order_by('-date_posted')
        rate_avg = obj.aggregate(Avg('rating')).get('rating__avg')
        paginator = Paginator(obj, 4)  # 4 posts in each page
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
    except:
        raise Http404("Something went wrong.")

    try:
        avg_rating = math.floor(rate_avg*10)/10
    except:
        avg_rating = 0

    if request.is_ajax():
        if form.is_valid():
            data = Review()
            data.ISBN = BookDetail.objects.get(pk=pk)
            data.review = form.cleaned_data['comment']
            data.rating = form.cleaned_data['rate']
            current_user= request.user
            data.user_id=current_user.id
            data.save()
            return JsonResponse({
                'msg': 'Success'
            })
        messages.success(request, "Your review has been sent. Thank you for your interest.")

    context = {
        'book' : book,
        'form': form,
        'avg_rating': avg_rating,
        'page': page,
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

    try:
        paginator = Paginator(results, 8)  
        page = request.GET.get('page')
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except:
        raise Http404("Something went wrong.")
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)

def autosuggestbook(request):
    query_original = request.GET.get('term')
    queryset = Post.objects.filter(Q(Book_Title__icontains=query_original))
    mylist = []
    mylist += [x.title for x in queryset]
    return JsonResponse(mylist, safe=False)

def recommendation(request):
    current_id = request.user.id
    ratings = Review.objects.filter(user = current_id)
    all_ratings = Review.objects.all()
   
    data = []
    ratings_not_zero = []
    
    for rate in ratings:
        user_id = [int(rate.user_id)]
        book_id = [str(rate.ISBN.ISBN)]
        rating_id = [int(rate.rating)]

        data.extend(zip(user_id, book_id, rating_id))

    for rate in all_ratings:
        user_id = [int(rate.user_id)]
        book_id = [str(rate.ISBN.ISBN)]
        rating_id = [int(rate.rating)]

        ratings_not_zero.extend(zip(user_id, book_id, rating_id))

    new_df = pd.DataFrame(data,columns=["user_id","id","book_rating"])
    books = pd.DataFrame(list(BookDetail.objects.all().values()))    
    ratings_not_zero = pd.DataFrame(ratings_not_zero,columns=["user_id","isbn","book_rating"])

    result = res_to_book(new_df,books)

    model = SVD()

    model1 = trainData(ratings_not_zero, model)
    pred = recommend(current_id,ratings_not_zero,model1)

    details = []
    columns=['id', 'ISBN', 'Book_Title', 'Image_URL_L', 'Book_Author']
    list_isbn = pred['isbn'].tolist()

    for i in list_isbn:
        recommend_book = BookDetail.objects.get(ISBN = i)
        details.append([recommend_book.id, recommend_book.ISBN, recommend_book.Book_Title,recommend_book.Image_URL_L, recommend_book.Book_Author])
    book_list_df = pd.DataFrame(details,columns=columns)

    pred_book_rating = res_to_booktoo(pred,books)
    return book_list_df

def res_to_book(res,books):
    res_book = list(res['id'].values)
    books_names = []
    for i in res_book:
        books_names.append(books[books.ISBN == i].Book_Title.values[0])
    return books_names    

def res_to_booktoo(res,books):
    res_book = list(res['isbn'].values)
    books_names = []
    for i in res_book:
        books_names.append(books[books.ISBN == i].Book_Title.values[0])
    return books_names

def trainData(df, model):
    '''
        df should contain user id, book id and rating column
    '''
    model2 = copy.deepcopy(model)
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df, reader)
    data = dataset.build_full_trainset()
    model = model2.fit(data)
    return model

def recommend(user,df,model,output_limit=8):
    user_rated_books = df.loc[df.user_id==user, 'isbn']
    unique_ids = df.isbn.unique()

    # removing the rated books for the recommendations
    book_ids_topredict = np.setdiff1d(unique_ids,user_rated_books)
    
    pred = []
    for iid in book_ids_topredict:
        pred.append((iid, model.predict(uid=user,iid=iid).est))
        
    pred_df = pd.DataFrame(pred,columns=['isbn','pred_rating'])
    pred_df.sort_values('pred_rating',ascending=False, inplace=True)
    
    return pred_df.head(output_limit)

def history(request):
    template = "history.html"
    current_id = request.user.id
    ratings = Review.objects.filter(user = current_id)

    context = {
        'ratings': ratings,
    }
    
    return render(request, template, context)


