from django.contrib import admin

from .models import Version, Book, Chapter, Verse

class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "version_name", "position", "alt_name", "testament", "slug", "deutero")
    list_filter = ("alt_name",)
    search_fields = ('name', 'alt_name')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "book_name", "number")
    list_filter = ("book", )
    search_fields = ('book',)

class VerseAdmin(admin.ModelAdmin):
    list_display = ("chapter", "number", "__str__", "text")
    search_fields = ("text", )

admin.site.register(Version)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Verse, VerseAdmin)
