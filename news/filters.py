from django_filters import FilterSet
from .models import Post
import django_filters
from django.forms import DateInput
# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые  Django дженерики.
class PostFilter(django_filters.FilterSet):
    # time_in = django_filters.DateFilter(widget=DateInput(attrs={'type':'date'}),lookup_expr='gte')
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
        model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = ['title', 'category']