from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2 as md
import random
from .wiki_entry import WikiEntry


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, title):
    return render(request, "encyclopedia/article.html", {
        "article_title": title,
        "article_body": md.markdown(util.get_entry(title))
    })


def search(request):
    if request.method == 'POST':
        search_term = request.POST['query']
        entries = util.list_entries()
        match_entries = []
        for entry in entries:
            if entry.lower() == search_term.lower():
                return article(request, search_term)
            elif search_term in entry:
                match_entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": match_entries
        })
    return HttpResponseRedirect('/')


def add(request):
    form = WikiEntry()
    if request.method == "POST":
        form = WikiEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_body = form.cleaned_data["entry_body"]
            if title not in util.list_entries():
                util.save_entry(title, entry_body)
                return HttpResponseRedirect(
                    reverse("encyclopedia:article", args=[title]))
            else:
                form.add_error(
                    "title",
                    "An entry for this topic already exists!")

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "new_entry": True
    })


def random_page(request):
    entry = random.choice(util.list_entries())
    return article(request, entry)


def edit(request, title):
    form = None
    if request.method == "POST":
        form = WikiEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_body = form.cleaned_data["entry_body"]
            util.save_entry(title, entry_body)
            return HttpResponseRedirect(
                reverse("encyclopedia:article", args=[title]))
    else:
        form = WikiEntry(initial={
                "title": title,
                "entry_body": util.get_entry(title)})

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title,
        "new_entry": False
    })
