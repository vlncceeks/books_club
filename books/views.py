from django.shortcuts import render
from django.db.models import Avg
from books.models import Book
from django.http import JsonResponse

def books_rating(request):

    books = Book.objects.annotate(
        avg_rating=Avg(
            "user_books__rating"
        )
    ).order_by(
        "-avg_rating"
    )

    data = []

    for book in books:
        data.append({
            "title": book.title,
            "author": book.author,
            "avg_rating": book.avg_rating
        })

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={"ensure_ascii": False}
    )