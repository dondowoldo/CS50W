from django.shortcuts import render

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