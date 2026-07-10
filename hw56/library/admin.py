from django.contrib import admin

from .models import Author, Book, Reader, Loan

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "birth_year")
    list_filter = ("country", "birth_year")
    search_fields = ("name", "country")
    ordering = ("name",)

class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "publication_year",
        "pages",
        "is_available",
    )
    list_filter = (
        "author",
        "publication_year",
        "is_available",
    )
    search_fields = (
        "title",
        "isbn",
        "author__name",
    )
    ordering = ("-publication_year",)

class ReaderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
    )
    search_fields = (
        "name",
        "email",
    )
    ordering = ("name",)

class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "reader",
        "book",
        "loan_date",
        "return_date",
    )
    list_filter = (
        "loan_date",
        "return_date",
        "book__author",
    )
    search_fields = (
        "reader__name",
        "reader__email",
        "book__title",
        "book__author__name",
    )
    ordering = ("-loan_date",)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Loan, LoanAdmin)
