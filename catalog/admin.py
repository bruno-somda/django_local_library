from django.contrib import admin

from .models import Genre,Author,Language,Book,BookInstance

# Register your models here
# .
class BookInstanceInline(admin.TabularInline):
    model= BookInstance
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display= ('title','author','display_genre')
    inlines=[BookInstanceInline]

class BookInline(admin.TabularInline):
    model= Book
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','date_of_birth','date_of_death']
    inlines=[BookInline]
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=['id','due_back','imprint','book','status']

    fieldsets=(
        (None,{
            'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields': ('status','due_back')
        })
    )
#admin.site.register(Book,BookAdmin)
admin.site.register(Genre)
admin.site.register(Language)