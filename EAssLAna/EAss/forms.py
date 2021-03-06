from django import forms
from django.utils import timezone

from EAss.models import QAWSet

class BinaryAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answer = forms.IntegerField()

class OctaAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answer = forms.IntegerField()

class ClozeForm(forms.Form):
    cloze_id = forms.IntegerField(widget=forms.HiddenInput())
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())

    def __init__(self, num_gaps: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(num_gaps):
            field_name = ClozeForm.get_gap_key(i)
            self.fields[field_name] = forms.CharField(required=False)

    @staticmethod
    def get_gap_key(index: int) -> str:
        return str(index)

class SCAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Options_q = forms.ChoiceField(choices=[], label="Statements")
    

    def __init__(self, *args, **kwargs):
        try:
            super(SCAnswerForm, self).__init__(*args, **kwargs)
            if 'initial' in kwargs.keys():
                self.fields['Options_q'].choices = (kwargs['initial'])['Options']
        except Exception as error:
            print(error)

class MCAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Options_q = forms.MultipleChoiceField(choices=[], label="Statements")
    

    def __init__(self, *args, **kwargs):
        try:
            super(MCAnswerForm, self).__init__(*args, **kwargs)
            if 'initial' in kwargs.keys():
                self.fields['Options_q'].choices = (kwargs['initial'])['Options']          
        except Exception as error:
            print(error)

class TtAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Qanswer = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Hint = forms.CharField(max_length=1024, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        try:
            super(TtAnswerForm, self).__init__(*args, **kwargs)
            if 'initial' in kwargs.keys():
                
                for x in ((kwargs['initial'])['Options']):
                    self.fields[x] = forms.TypedChoiceField(coerce=lambda x: x =='True', choices=((False, 'Wrong'), (True, 'Right')))
           
        except Exception as error:
            print(error)

class OpenAssemblerAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=16384, widget=forms.HiddenInput())
    CodeAnswer = forms.CharField(max_length=16384, label=False, widget=forms.Textarea(attrs={"rows":5, "cols":20}))
   
class GatesAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    BeginTime = forms.DateTimeField(widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Gateanswer = forms.IntegerField()
    Expectedcircuitfunction = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answerircuitfunction = forms.CharField(max_length=1024)
    Imgpath = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Expectedanswer = forms.IntegerField(widget=forms.HiddenInput())
    Input = forms.CharField(max_length=1024, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(GatesAnswerForm, self).__init__(*args, **kwargs)
        self.fields['Gateanswer'].label = "Answer for result in gate circuit image"
        self.fields['Answerircuitfunction'].label = "Answer for circuitfunction of gate circuit image"
