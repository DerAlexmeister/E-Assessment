from textwrap import indent
from django.contrib import admin
from django.urls import path

from .views import index
from .views import generateMCExample
from .views import generateBinaryExpression
from .views import clozeTextGenerator
from .views import generateSCQuestions
from .views import generateMCQuestions
from .views import generateBinaryQuestions
from .views import generateOctaQuestions
from .views import generateTruthTables
from .views import returnMasterTemplate
from .views import generateOpenAssemblerQuestions
from .views import generateGateQuestions
from .normal_forms.view import normal_form

urlpatterns = [
    ## Production
    path('', index, name="homeview"),
    path('mcgenerator/', generateMCQuestions),
    path('scgenerator/', generateSCQuestions),
    path('bingenerator/', generateBinaryQuestions),
    path('octagenerator/', generateOctaQuestions),
    path('clozegenerator/', clozeTextGenerator),
    path('ttgenerator/', generateTruthTables),
    path('oagenerator/', generateOpenAssemblerQuestions),
    path('gatesgenerator/', generateGateQuestions),
    path('normalform/', normal_form),

    ## Examples 
    path('example/', generateMCExample),
    path('examplebin/', generateBinaryExpression),
    #path('examplecloze/', clozeText),
    #path('examplett/', generateTruthTables),

    ## Testing
    path('master/', returnMasterTemplate),
]
