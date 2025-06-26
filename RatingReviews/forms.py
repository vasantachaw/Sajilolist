from django import forms

class CommentForm(forms.Form):
    user_name = forms.CharField(max_length=100, label="Your Name")
    text = forms.CharField(widget=forms.Textarea, label="Comment")
