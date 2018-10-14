from django.contrib import admin

from .models import Council, Category, Document, Chapter, Article, Note

class CouncilAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'location')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('council', 'latin_name', 'english_name', 'pontiff', 'category', 'position', 'slug', 'promulgation_date', 'location')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('document', 'title', 'number')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'number', 'text')

class NoteAdmin(admin.ModelAdmin):
    list_display = ('number', 'article', 'text')

admin.site.register(Council, CouncilAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Note, NoteAdmin)
