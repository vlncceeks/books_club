from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Avg, Count, Q

from books.models import UserBook
from events.models import Event

User = get_user_model()


def user_profile(request, user_id):

    user = get_object_or_404(
        User.objects.select_related("role") 
        .filter( 
            id=user_id, 
            role__name__isnull=False 
        ) 
    )

    data = {
        "username": user.username,
        "role": user.role.name,
        "status": user.status,
        "bio": user.bio,
        "joined": user.date_joined,
        "url": user.get_absolute_url(),
    }

    return JsonResponse(data,
        json_dumps_params={"ensure_ascii": False})

def user_books_by_status(request, user_id, status):

    books = UserBook.objects.filter(
        user__id=user_id,   
        reading_status=status,
    ).exclude(
        rating__isnull=True  
    ).select_related(
        "book",
        "book__genre"
    ).order_by(
        "-rating",           
        "book__title"
    )


    data = []

    for ub in books:
        data.append({
            "title": ub.book.title,
            "author": ub.book.author,
            "status": ub.reading_status,
            "rating": ub.rating,
        })

    return JsonResponse(data, safe=False,
        json_dumps_params={"ensure_ascii": False})

def user_events(request, user_id):

    now = timezone.now()

    events = Event.objects.filter(
        participants__id=user_id
    ).exclude(
        event_date__lt=now  
    ).select_related(
        "book",
        "organizer__role"
    ).order_by(
        "event_date"   
    )
    
    data = []

    for event in events:
        data.append({
            "title": event.title,
            "book": event.book.title,
            "event_date": event.event_date,
            "free_places": event.free_places,
        })

    return JsonResponse(data, safe=False,
        json_dumps_params={"ensure_ascii": False})


def active_users(request):

    users = User.manager.active().order_by(
        "role__name",
        "username"
    )

    data = []

    for user in users:
        data.append({
            "username": user.username,
            "role": user.role.name,
        })

    return JsonResponse(data, safe=False,
        json_dumps_params={"ensure_ascii": False})

def user_books_stats(request, user_id):

    stats = UserBook.objects.filter(
        user__id=user_id,
        reading_status="read"
    ).aggregate(
        avg_rating=Avg("rating"),
        total_books=Count("id")
    )

    return JsonResponse(
        stats,
        json_dumps_params={"ensure_ascii": False}
    )

def users_reading_stats(request):

    users = User.objects.annotate(
        read_books=Count(
            "user_books",
            filter=Q(
                user_books__reading_status="read"
            )
        )
    ).order_by(
        "-read_books"
    )

    data = []

    for user in users:
        data.append({
            "username": user.username,
            "read_books": user.read_books
        })

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={"ensure_ascii": False}
    )