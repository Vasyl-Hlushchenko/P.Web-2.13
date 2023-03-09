from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuoteForm, AuthorForm, TagForm
from .models import Author, Quote, Tag


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_authors = Author.objects.filter(full_name__in=request.POST.getlist('authors'))
            for author in choice_authors.iterator():
                new_quote.authors.add(author)
            
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    author = Author.objects.get(id=quote.author_id)
    
    return render(request, 'quoteapp/detail.html', {"quote": quote, "author": author})


def find_author(request, author_id):
    author = Author.objects.get(id=author_id)
    
    return render(request, 'quoteapp/find_author.html', {"author": author})
