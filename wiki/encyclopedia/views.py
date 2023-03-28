from django.shortcuts import render
from django.shortcuts import redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def content(request, title):
    return render(request, "encyclopedia/content.html", {
        "retrieve": util.get_entry(title),
        "name": title
    })

def search(request):
        searched = request.GET['q']
        if not util.get_entry(searched):
            matches = []
            for entry in util.list_entries():
                 if searched.lower() in entry.lower():
                      matches.append(entry)
            return render(request, "encyclopedia/search.html", {
                "searched": searched,
                "matches": matches
                })
        else:
             return redirect(f"/wiki/{searched}")