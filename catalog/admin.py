from django.contrib import admin

from .models import Genre,Author,Language,Book,BookInstance

# Register your models here.
#@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display=['id','title','author','display_genre']

   
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','date_of_birth','date_of_death']
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=['id','imprint','book','status']


admin.site.register(Book,BookAdmin)
admin.site.register(Genre)
admin.site.register(Language)