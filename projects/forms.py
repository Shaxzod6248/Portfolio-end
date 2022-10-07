from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import *


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description',
                  'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Izohni shu yerga yozing',
            'body': 'Ovoz qoldiring'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})