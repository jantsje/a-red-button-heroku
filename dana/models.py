from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
from django import forms


doc = """
This is the Dana task.
"""


class Constants(BaseConstants):
    name_in_url = 'dana'
    players_per_group = None
    num_rounds = 1

    # Dana payoffs
    danaA_self = 60
    danaB_self = 50
    danaA_other1 = 50
    danaA_other2 = 10

    participation_fee = 1.30  # in pounds
    timeout = 15  # in seconds

class Subsession(BaseSubsession):
    def creating_session(self):
        pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    timeout = models.FloatField()
    prolific_id = models.StringField()
    browser = models.StringField()
    understanding_questions_wrong_attempts = models.PositiveIntegerField()  # for all tasks
    uq_wrong_dana = models.PositiveIntegerField()  # storing UQ Dana
    uq_wrong_dana2 = models.PositiveIntegerField()  # storing UQ Dana 2
    reveal = models.BooleanField(blank=True)  # whether participant decides to reveal information in Dana task
    task1 = models.StringField(blank=True)  # whether participant takes selfish choice in Dana task
    scenario1 = models.BooleanField(blank=True)  # whether scenario 1 or 2 will be displayed

    payoff_optionB = models.StringField()
    total_payoff = models.FloatField()
    payoff1_self = models.StringField()  # payoff task 1 (dana)
    payoff1_charity = models.StringField()  # payoff task 1 (dana)

    def store_uq_dana(self):
        self.uq_wrong_dana = self.understanding_questions_wrong_attempts

    def store_uq_dana2(self):
        self.uq_wrong_dana2 = self.understanding_questions_wrong_attempts

    def set_payoffs1(self):   # payoffs Task 1 (Dana)
        if self.task1 == "A":
            self.payoff1_self = "£" + str(0.01*Constants.danaA_self) + "0"
            if self.scenario1:
                self.payoff1_charity = "£" + str(0.01*Constants.danaA_other1) + "0"
            else:
                self.payoff1_charity = "£" + str(0.01*Constants.danaA_other2) + "0"
        elif self.task1 == "B":
            self.payoff1_self = "£" + str(0.01*Constants.danaB_self) + "0"
            if self.scenario1:
                self.payoff1_charity = "£" + str(0.01*Constants.danaA_other2) + "0"
            else:
                self.payoff1_charity = "£" + str(0.01*Constants.danaA_other1) + "0"
        # to store for next app (button task + final payoffs)
        self.participant.vars["payoff1_self"] = self.payoff1_self
        self.participant.vars["payoff1_charity"] = self.payoff1_charity

    def get_questions_method(self):
        questions = [
            {
                'question': 'In the table my bonus payment is denoted in',
                'options': ['Red', 'Blue'],
                'correct': 'Blue',
            },
            {
                'question': 'If you choose A, the Red Cross obtains a bonus of',
                'options': ['10 pence', '20 pence', '40 pence'],
                'correct': '20 pence',
            },
            {
                'question': 'If you choose B, you earn a bonus of',
                'options': ['10 pence', '30 pence', '20 pence'],
                'correct': '30 pence',
            },

        ]
        return questions

    def get_questions_method2(self):
        questions = [
            {
                'question': 'Which option gives you a bonus payment of ' + str(Constants.danaA_self) + ' pence?',
                'options': ['Option A', 'Option B', 'It depends on the scenario'],
                'correct': 'Option A',
            },
            {
                'question': 'If you choose A, the Red Cross earns a bonus of',
                'options': [str(Constants.danaA_other1) + ' pence', str(Constants.danaA_other2) + ' pence',
                            'either ' + str(Constants.danaA_other1) + ' pence or ' + str(Constants.danaA_other2) +
                            ' pence, depending on the scenario'],
                'correct': 'either ' + str(Constants.danaA_other1) + ' pence or ' + str(Constants.danaA_other2) +
                           ' pence, depending on the scenario',
            },
        ]
        return questions