from django.forms import ModelForm, Textarea, TextInput

from .models import Memo


class MemoForm(ModelForm):
    class Meta:
        model = Memo
        widgets = {
            'commentary': Textarea(attrs={'placeholder': 'Ваш комментарий об этом месте'}),
            'place': TextInput(attrs={'placeholder': 'Выберите место на карте'}),
            'name': TextInput(attrs={'placeholder': 'Название места'})
        }
        exclude = ['user']

        labels = {
            "place": "Посещенное место",
            "name": "Название места",
            "commentary": "Комметарий о месте"
        }