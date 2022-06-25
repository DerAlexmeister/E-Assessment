import numpy as np
import pandas as pd

from django.shortcuts import render
from django.http.response import HttpResponse

from random import choice

from . form import NormalForm

from .normal_form import Guess, TruthTable, Question, DISJUNCTION, CONJUNCTION
from .assessment import BooleanAssessment
from ..core import generateNumbers


QUESTION_KEY = 'question'


def normal_form(request):
    if request.method == 'POST':
        assessment = BooleanAssessment()

        question = Question.from_dict(request.session[QUESTION_KEY])
        response = NormalForm(question, request.POST)

        if response.is_valid():
            guess = response.cleaned_data['guess']
            return render(request, 'normal_form.html', {
                'question': guess.question,
                'table': guess.question.function.table.to_html(),
                'input': response,
                'correction': "You are correct",
            })
        else:
            return HttpResponse(response.errors.get('guess'))

    else:
        variables = {"a", "b"}
        results = generateNumbers(1, 2**len(variables))
        table = TruthTable.create(variables, "f", results)
        normal_form = choice([DISJUNCTION, CONJUNCTION])

        question = Question(normal_form, table)

        request.session[QUESTION_KEY] = question.to_dict()

        return render(request, 'normal_form.html', {
            'question': question,
            'table': question.function.table.to_html(),
            'input': NormalForm(question),
        })