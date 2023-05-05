from auctions.models import Listing

def count_watchlist(request):
    if request.user is not None:
        watch_count = len(Listing.objects.filter(watchlist__id=request.user.id))
        return {'watchcount': watch_count if watch_count > 0 else None}
    return None