from django.forms import ModelForm, Form
from .models import News
from django.forms.widgets import Input, Textarea, FileInput


class NewsForm(ModelForm):
    class Meta:
        model = News
        is_multipart = True
        fields = ('title', 'content', 'image')
        widgets = {
            'title': Input(attrs={'type': "None", "name": "title", 'class': "sections", 'id': "name",
                                  'spellcheck': "false", 'maxlength': "50", 'required': ""}),
            'content': Textarea(attrs={'name': "content", 'cols': "40", 'rows': "10",
                                       'id': "info", 'class': "sections", 'maxlength': "500"}),
            'image': FileInput(attrs={'type': "file", 'name': "image", 'class': "sections", "id": "photo",
                                      'accept': "image/*", }),
        }
