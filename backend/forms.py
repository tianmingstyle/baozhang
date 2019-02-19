from django.forms import Form
from django.forms import widgets
from django.forms import fields


class TroubleCreate(Form):
    title = fields.CharField(
        widget=widgets.Input(attrs={'class':'form-control'}),
        required=True,
    )
    detail = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control', 'id':'detail'}),
        required=True,

    )


class Trouble_kill(Form):
    title = fields.CharField(
        widget = widgets.Input(attrs={'class': 'form-control', 'disabled':'disabled'}),
        required=False
    )
    detail = fields.CharField(
        widget = widgets.TextInput(attrs={'class': 'form-control', 'id': 'detail', 'disabled': 'disabled'}),
        required=False
    )
    solution = fields.CharField(
        widget = widgets.TextInput(attrs={'class': 'form-control', 'id': 'solution'})
    )


