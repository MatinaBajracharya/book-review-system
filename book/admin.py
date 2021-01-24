from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import BookDetail, Review

# Register your models here.
class BookDetailAdmin(ImportExportModelAdmin):
    pass

admin.site.register(BookDetail, BookDetailAdmin)
admin.site.register(Review)