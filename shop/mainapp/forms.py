from django.forms import ModelForm
from mainapp.models import Category

class CategoryForm (ModelForm):
    def __init__(self,*args, **kwargs):
        super(CategoryForm, self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    class Meta:
        model=Category
        fields="__all__"


