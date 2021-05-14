from django.forms import ModelForm, Textarea

from .models import Memo


class MemoForm(ModelForm):
    class Meta:
        model = Memo
        widgets = {
            'commentary': Textarea(),
        }
        exclude = ['user']
