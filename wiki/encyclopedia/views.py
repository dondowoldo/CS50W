from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2

from . import util


# Checks if the title that user wants to add already exists or not.
def is_unique(title):
     if not util.get_entry(title):
          return True
     return False


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "20", "cols": "100"}))
    
    # If the title already exists, application raises a validation error without saving.
    def clean_title(self):
        data = self.cleaned_data.get("title")
        
        if not is_unique(data):
             raise forms.ValidationError("Error: This page already exists.")
        return data

class EditEntryForm(forms.Form):
    edit_content = forms.CharField(widget=forms.Textarea(attrs={"rows": "20", "cols": "100"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def content(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/content.html", {
            "retrieve": markdown2.markdown(util.get_entry(title)),
            "name": title
                })
    else:
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

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        edit_form = EditEntryForm({"edit_content": content})
    
        return render(request, "encyclopedia/edit.html", {
             "form": edit_form,
             "title": title 
            })
    else:
         edit_form = EditEntryForm(request.POST)
         if edit_form.is_valid():
              content = edit_form.cleaned_data["edit_content"]
              util.save_entry(title, content)
              return HttpResponseRedirect(reverse("wiki:title", args=[title]))
         else:
              return render(request, "encyclopedia/edit.html", {
                 "form": edit_form  
              })

def randomPage(request):
     random_entry = random.choice(util.list_entries())
     return HttpResponseRedirect(reverse("wiki:title", args=[random_entry]))