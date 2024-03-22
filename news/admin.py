from django.contrib import admin

from .models import Category, Author, Post, PostCategory, Comment,UserCategory

# создаём новый класс для представления постов в админке
class PostAdmin(admin.ModelAdmin):

    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title','time_in')  # оставляем только имя и цену товара
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = ('title','time_in','category')  # добавляем примитивные фильтры в нашу админку
     # добавляем примитивные фильтры в нашу админку
    # search_fields = ('title', 'category','time_in')  # тут всё очень похоже на фильтры из запросов в базу
#не сработало
# class PostInline(admin.TabularInline):
#     model = Post.category.through


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     model = Category
#     inlines = [
#         PostInline,
#     ]

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(UserCategory)





# Register your models here.
