from django.shortcuts import redirect, render

from . import util
from django.utils.html import strip_tags



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    return render(request, "encyclopedia/entry_page.html", {
        "entry": util.get_entry(title),
        "title": title
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get('q')
        if query.strip():
            if util.get_entry(query):
                return render(request, "encyclopedia/entry_page.html", {
                    "entry": util.get_entry(query),
                    "title": query
                })
            matching_entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            if matching_entries:
                return render(request, "encyclopedia/index.html", {
                    "entries": matching_entries
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": []
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def create_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Check if the title or content is empty
        if not title.strip() or not content.strip():
            error_message = "Title and content cannot be empty."
            return render(request, "encyclopedia/create_page.html", {"error_message": error_message})
        
        # Check if an entry with the provided title already exists
        if util.get_entry(title):
            error_message = "An entry with this title already exists."
            return render(request, "encyclopedia/create_page.html", {"error_message": error_message})

        # Save the entry add # to title
        util.save_entry(title, content)

        # Redirect the user to the newly created entry's page
        return redirect('entry_page', title=title)
    
    return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get('content')

        # Check if the content is empty
        if not content.strip():
            error_message = "Content cannot be empty."
            return render(request, "encyclopedia/edit_page.html", {
                "error_message": error_message,
                "entry": util.get_entry(title),
                "title": title,
            })

        # Save the entry
        util.save_entry(title, content)

        # Redirect the user to the entry's page
        return redirect('entry_page', title=title)
    
    return render(request, "encyclopedia/edit_page.html", {
        "entry": util.get_entry(title),
        "title": title,
        "content": util.get_entry(title),
    })

def random_page(request):
    import random
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect('entry_page', title=title)

    

    
