from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewEntryForm(forms.Form):
     title = forms.CharField(label="Title")
     content = forms.CharField(widget=forms.Textarea(attrs={"rows": "20", "cols": "100"}))


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
             return HttpResponseRedirect(reverse("wiki:title", args=[searched]))
        
def create(request):
     if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
           "form": NewEntryForm()
     })
     else:
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:title", args=[title]))
        else:
             return render(request, "encyclopedia/create.html", {
                  "form": form
             })