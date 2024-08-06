from django import forms

 

class StudentForm(forms.Form):

    firstname = forms.CharField(label="Enter first name", max_length=50)

    file = forms.FileField()  # for creating file input