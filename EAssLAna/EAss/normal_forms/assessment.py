from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass

from . import model
from .normal_form import Guess, TruthTable, Literal, NormalForm, DISJUNCTION, CONJUNCTION


def to_dnf(formula: TruthTable) -> NormalForm:
    clauses = []
    for _, assignment in formula.table[formula.results==1].iterrows():
        clause = []
        for v in formula.variables:
            clause.append(Literal(v, bool(assignment[v])))
        clauses.append(clause)
    return NormalForm(clauses)


def to_cnf(formula: TruthTable) -> NormalForm:
    clauses = []
    for _, assignment in formula.table[formula.results==0].iterrows():
        clause = []
        for v in formula.variables:
            clause.append(Literal(v, bool(assignment[v])))
        clauses.append(clause)
    return NormalForm(clauses)


SOLUTIONS_CALCULATORS = {
    DISJUNCTION: to_dnf,
    CONJUNCTION: to_cnf,
}


class Assessment(ABC):
    @abstractmethod
    def assess(self, guess: Guess, **kwargs) -> str:
        pass


class BooleanAssessment(Assessment):
    def assess(self, guess: Guess, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        if guess.answer == solution:
            return "You are correct!"
        else:
            return "You are false!"


class GradingAssessment(Assessment):
    def assess(self, guess: Guess, guess_model, penalty, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        counter = 0
        for g, e in zip(solution.clauses, guess.answer.clauses):
            if g == e:
                counter += 1

        counter = max(counter - penalty, 0)
        if guess_model:
            correction = model.NormalFormCorrection(guess=guess_model, UserID=guess_model.UserID, points=counter, total_points=len(solution.clauses))
            correction.save()

        return f"{counter}/{len(solution.clauses)}"



class CorrectingBooleanAssessment(Assessment):
    def assess(self, guess: Guess, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )

        guess = deepcopy(guess)

        response = []
        for s in solution.clauses:
            if s in guess.answer.clauses:
                response.append((s, True))
                guess.answer.clauses.remove(s)
            else:
                response.append((s, False))

        if guess.question.normal_form == DISJUNCTION:
            inner = "*"
            outer = "+"
        elif guess.question.normal_form == CONJUNCTION:
            inner = "+"
            outer = "*"
        else:
            raise Exception("Unknown normal form")

        clause = f" {outer} ".join(
            f"""<span style="color:{"green" if right else "red"}">
               {f" {inner} ".join(str(lit) for lit in clause)}
               </span>"""
            for clause, right in response
        )
        return f"<p>f(a)  =    {clause}</p>"


class DifferenceAssessment(Assessment):
    def assess(self, guess: Guess, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )

        response = []
        for g in guess.answer.clauses:
            if g in solution.clauses:
                response.append((g, True))
                solution.clauses.remove(g)
            else:
                response.append((g, False))

        if guess.question.normal_form == DISJUNCTION:
            inner = "*"
            outer = "+"
        elif guess.question.normal_form == CONJUNCTION:
            inner = "+"
            outer = "*"
        else:
            raise Exception("Unknown normal form")

        clause = f" {outer} ".join(
            f"""<span style="color:{"green" if right else "red"}">
               {f" {inner} ".join(str(lit) for lit in clause)}
               </span>"""
            for clause, right in response
        )
        return f"<p>f(a)  =    {clause}</p>"


class GradingAndCorrectionAssessment(Assessment):
    def __init__(self):
        self._grading = GradingAssessment()
        self._difference = CorrectingBooleanAssessment()

    def assess(self, guess: Guess, guess_model, penalty, **kwargs) -> str:
        grading = self._grading.assess(guess, guess_model, penalty, **kwargs)
        difference = self._difference.assess(guess, **kwargs)

        return f"""
        Correct solution ({grading}):
            {difference}
        </p>
        """


@dataclass
class RememberingAssessment(Assessment):
    assessment: Assessment

    def assess(self, guess: Guess, qaw, user, duration, **kwargs) -> str:
        question = model.NormalFormQuestion(normal_form=guess.question.normal_form)
        question.save()

        for col, _ in guess.question.function.table[guess.question.function.results==1].iterrows():
            function_value = model.FunctionValue(question=question, one=col)
            function_value.save()

        answer = model.NormalFormAnswer()
        answer.save()

        for clause in guess.answer.clauses:
            term = model.NormalFormTerm(answer=answer)
            term.save()

            for lit in clause:
                literal = model.NormalFormLiteral(term=term, variable=lit.variable, sign=lit.sign)
                literal.save()

        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        AllCorrect = guess.answer == solution
        guess_model = model.NormalFormGuess(Set=qaw, UserID=user.id, Duration=duration, AllCorrect=AllCorrect,question=question, answer=answer)
        guess_model.save()

        return self.assessment.assess(guess, **{'guess_model': guess_model, **kwargs})


ASSESSMENTS = {
    'boolean': RememberingAssessment(BooleanAssessment()),
    'grading': RememberingAssessment(GradingAssessment()),
    'correcting_boolean': RememberingAssessment(CorrectingBooleanAssessment()),
    'grading_correction': RememberingAssessment(GradingAndCorrectionAssessment()),
    'difference': DifferenceAssessment(),
}
