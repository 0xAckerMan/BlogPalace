from django import forms
from .models import Comment

class CommentForm(forms.modelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

    # overriding default forms setting and adding some bootstrap class 

    def __init__(self, *args, **kwargs):
        supper(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class': 'form-control'}
