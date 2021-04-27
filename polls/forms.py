
from .models import Comment, Tag
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentForm(forms.ModelForm):
    email = forms.EmailField()
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Comment here !',
            'rows': 4,
            'cols': 50,

        }), error_messages={'required': "Please Enter Your Comment"})

    class Meta:
        model = Comment
        fields = ['email', 'content']


class VerifyTagAdmin(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_tag(self):
        """
            Clean form tag.
            :return str email: cleaned tag
            :raise forms.ValidationError: tag already exists.

        """
        tag = self.cleaned_data['tag'].lower()
        for instance in Tag.objects.all().exclude(id=self.instance.id):
            if instance.tag == tag:
                raise forms.ValidationError('Tag already exists')
        return tag

