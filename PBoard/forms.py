from django.forms import ModelForm, Form
from django.forms.widgets import Input, Select, NumberInput, Textarea, FileInput, CheckboxInput
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(ModelForm):
    class Meta:
        model = Post
        is_multipart = True
        fields = ('name', 'photo', 'user_score', 'info', 'rubric', 'show_authorship')
        widgets = {
            'name': Input(attrs={'class': 'sections', 'id': 'name', 'spellcheck': 'false'}),
            'rubric': Select(attrs={'class': 'sections', 'id': 'rubrics'}),
            'photo': FileInput(attrs={'class': 'sections',
                                      'id': 'photo',
                                      'type': 'file',
                                      'name': 'photo'}),
            'user_score': NumberInput(attrs={'class': 'sections', 'id': 'din', 'type': 'number',
                                        'name': 'assesiment', 'min': '1', 'max': '10', 'step': '0.1'}),
            'info': Textarea(attrs={'name': 'link', 'id': 'info', 'class': 'sections'}),
            'show_authorship':CheckboxInput()
        } 
    
    def clean(self):
        super().clean()
        errors = {}
 
        for p in Post.objects.all():
            if self.cleaned_data['name'] == p.name:
                errors['name'] = ValidationError('Публикация с таким названием уже существует.')

        if errors:
            raise ValidationError(errors)


    


