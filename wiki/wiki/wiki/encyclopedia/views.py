from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from . import util
import random


def md_to_html(title):
     content = util.get_entry(title)
     markdowner = Markdown()
     if content == None:
         return None
     else:
         return  markdowner.convert(content)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def title(request, entry):
    html_content = md_to_html(entry)
    if html_content == None:
        return render(request, "encyclopedia/404.html")
    elif html_content != None:
        return render(request, "encyclopedia/page_layout.html", {
            "text": html_content,
            "title": entry
        })


def search(request):
    entry = request.POST.get('q')
    entries = util.list_entries()
    if entry in entries:
        return render(request, "encyclopedia/page_layout.html", {
            "title": entry,
            "text": md_to_html(entry)
        })
    else:
        def match_search(word_list, searchable):
            return [word for word in word_list if searchable in word]

        matches = match_search(entries, entry)
        return render(request, "encyclopedia/results.html",{
            "matches": matches
        })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        entry_title = request.POST.get('title')
        content = request.POST.get('text')
        entries = util.list_entries()
        if entry_title in entries:
            return HttpResponse("Title already exists")
        else:
            util.save_entry(entry_title, content)
            return render(request, "encyclopedia/page_layout.html", {
                "text": util.get_entry(entry_title)
            })

def edit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        html_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": html_content
        })

def update(request):
    title = request.POST.get('title')
    text = request.POST.get('text')
    util.save_entry(title,text)
    return render(request, "encyclopedia/page_layout.html", {
        "text": md_to_html(title),
        "title": title
    })


def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return render(request, "encyclopedia/page_layout.html", {
        "text": md_to_html(random_entry),
        "title": random_entry
    })








