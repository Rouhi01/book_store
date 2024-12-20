from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نظر شما چیست؟',
                'rows': 2,
            })
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'ریپلای خود را بنویسید...',
                'rows': 2,
            })
        }


class LikeForm(forms.Form):
    content_id = forms.IntegerField(widget=forms.HiddenInput(attrs={
        'class':'white-btn mr-10'
    }))


# class LikeCommentForm(forms.Form):
#     content_id = forms.IntegerField(widget=forms.HiddenInput())

