from django.contrib import admin

from .models import Commentary, CommentaryText, Topic

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "version")

class CommentaryTextAdmin(admin.ModelAdmin):
    list_display = ("commentary", "book", "chapter", "verse", "heading", "text")


admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(CommentaryText, CommentaryTextAdmin)
admin.site.register(Topic)
