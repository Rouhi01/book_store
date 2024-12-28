from django import forms
from .models import Comment, Contact


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'full_name', 'topic', 'content']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control valid',
                'name': 'email',
                'id': 'email',
                'type': "email",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'ایمیل'",
                'placeholder': 'ایمیل'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'name',
                'id': 'name',
                'type': "text",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'نام و نام خانوادگی'",
                'placeholder': 'نام و نام خانوادگی'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'subject',
                'id': 'subject',
                'type': "text",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'موضوع'",
                'placeholder': 'موضوع'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'name': 'message',
                'id': 'message',
                'cols': '30',
                'rows': '9',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'متن پیام'",
                'placeholder': 'متن پیام'
            })
        }
