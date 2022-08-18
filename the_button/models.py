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
This is the button game. 
"""


class Constants(BaseConstants):
    name_in_url = 'the_button'
    players_per_group = 2
    num_rounds = 1

    # roles
    sender_role = "Sender"
    receiver_role = "Receiver"

    # Button payoffs
    optionA = [0, 0]  # bonus payments NO CLICK [receiver, charity] - in pence
    optionB = 1  # bonus payment CLICK - in pound
    payoffs_charity = [["-", 2.5], ["-", 1], ["-", 0.5], ["+", 0.5]]

    punishment = 20  # punishment budget in pence
    payoff_sender = 50
    cost_of_sending_baseline = 10
    cost_of_sending_extra = 25
    cost_of_sending_positive = 10

    timer = 30  # in seconds

    participation_fee = 0.75  # in pounds


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            if 'treatment' in self.session.config:
                g.treatment = self.session.config["treatment"]
            else:
                g.treatment = random.choice(["Baseline", "Request"])

            self.session.vars["treatment"] = g.treatment

            if self.round_number == 1:
                import string
                g.group_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        for p in self.get_players():
            p.participant.label = p.role
            p.participant.vars["too_long"] = False
            p.participant.vars["payoff2_self"] = ""
            p.participant.vars["payoff2_charity"] = ""
            p.participant.vars["payoff2_self_p"] = ""
            p.participant.vars["payoff2_charity_p"] = ""
            p.participant.vars["cost_of_sending"] = ""
            p.participant.vars['punished'] = ""
            p.participant.vars['punishment'] = ""
            if self.session.vars["treatment"] == "Extra Costly":
                p.cost_of_sending = Constants.cost_of_sending_extra
            elif self.session.vars["treatment"] == "Sending Positive":
                p.cost_of_sending = Constants.cost_of_sending_positive
            else:
                p.cost_of_sending = Constants.cost_of_sending_baseline
            p.participant.vars["cost_of_sending"] = p.cost_of_sending
            if self.session.vars["treatment"] == "Sending Positive":
                p.bonus_minus_cost = Constants.payoff_sender + p.cost_of_sending
            else:
                p.bonus_minus_cost = Constants.payoff_sender - p.cost_of_sending


class Group(BaseGroup):
    treatment = models.StringField()
    messages_num = models.IntegerField()
    group_id = models.StringField()

    def store_request(self):
        receiver = self.get_player_by_role(Constants.receiver_role)
        self.session.vars["request"] = receiver.request

    def store_message(self):
        sender = self.get_player_by_role(Constants.sender_role)
        sender.participant.vars["message"] = ""
        receiver = self.get_player_by_role(Constants.receiver_role)
        selected_situation = random.choice(range(0, len(Constants.payoffs_charity)))
        messages = [sender.message_1, sender.message_2, sender.message_3, sender.message_4]
        self.messages_num = messages.count("True")
        receiver.payoff_charity = str(Constants.payoffs_charity[selected_situation][0]) + "£" + \
                                  str(f'{Constants.payoffs_charity[selected_situation][1]:.2f}')
        if messages[selected_situation] == "False":
            sender.selected_message = "no message"
            receiver.selected_message = ""
            receiver.participant.vars["message"] = ""
            receiver.informed = False
            sender.informed = False
        else:
            sender.selected_message = "message " + str(Constants.payoffs_charity[selected_situation][1])
            amount0 = Constants.payoffs_charity[selected_situation][0]
            amount1 = Constants.payoffs_charity[selected_situation][1]
            receiver.informed = True
            sender.informed = True
            if amount1 > 0:
                receiver.selected_message = "Red Cross: " + \
                                   str(amount0) + "£" + str(amount1)
                receiver.participant.vars["message"] = "Red Cross: " + \
                                   str(amount0) + "£" + str(amount1)
            elif amount1 == 0 and amount0 != "-":
                receiver.selected_message = "Red Cross not affected"
                receiver.participant.vars["message"] = "Red Cross not affected"

    def store_punishment(self):
        receiver = self.get_player_by_role(Constants.receiver_role)
        sender = self.get_player_by_role(Constants.sender_role)
        sender.punished = receiver.punishment
        sender.participant.vars['punished'] = sender.punished
        receiver.participant.vars['punishment'] = receiver.punishment


class Player(BasePlayer):
    prolific_id = models.StringField()
    browser = models.StringField()
    understanding_questions_wrong_attempts = models.PositiveIntegerField()  # for all tasks
    uq_wrong_button = models.PositiveIntegerField()  # for Button task
    scenario1 = models.BooleanField(blank=True)  # whether scenario 1 or 2 will be displayed

    store_time = models.FloatField()  # for the timer
    store_time_test = models.FloatField()  # for the timer
    button = models.BooleanField(initial=0)
    button_test = models.BooleanField(initial=0)
    message = models.StringField()
    payoff_charity = models.StringField()
    punishment = models.IntegerField()
    punished = models.IntegerField()
    selected_message = models.StringField()
    payoff_optionB = models.StringField()
    total_payoff = models.FloatField()
    payoff2_self = models.StringField()  # payoff task 2 (button)
    payoff2_charity = models.StringField()  # payoff task 2 (button)
    request = models.StringField(choices=["True", "False"],
                                 widget=widgets.CheckboxInput,
                                 blank="False")
    message_1 = models.StringField()
    message_2 = models.StringField()
    message_3 = models.StringField()
    message_4 = models.StringField()
    informed = models.BooleanField()
    selected = models.IntegerField()  # which task is selected for payoff
    cost_of_sending = models.IntegerField()
    bonus_minus_cost = models.IntegerField()

    # player fields for final questionnaire
    gender = models.IntegerField(choices=[(0, 'Male'), (1, 'Female'),
                                          (2, 'Non-binary'), (3, 'Rather not say')],
                                 label="What is your gender?",
                                 widget=widgets.RadioSelect,
                                 )
    feedback = models.LongStringField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 130}),
                                      label="This is the end of the survey. "
                                            "In case you have comments, please leave them here.",
                                      blank=True)

    feedback_pilot = models.LongStringField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 130}),
                                            label="If you found any instructions unclear or confusing, "
                                            "please let us know here.",
                                            blank=True)

    age = models.PositiveIntegerField(label="What is your age?",
                                      help_text="years", min=18, max=120)

    punishment_motivation = models.LongStringField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 130}))

    send_motivation1 = models.LongStringField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 130}))

    send_motivation2 = models.LongStringField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 130}))

    button_motivation = models.LongStringField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 130}))
    request_motivation = models.LongStringField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 130}),
                                                blank=True)

    belief0 = models.PositiveIntegerField()   # ???
    belief1 = models.PositiveIntegerField()   # -2.5
    belief2 = models.PositiveIntegerField()   # -1.0
    belief3 = models.PositiveIntegerField()   # -0.5
    belief4 = models.PositiveIntegerField()   # +0.5

    def store_uq_button(self):
        self.uq_wrong_button = self.understanding_questions_wrong_attempts

    def set_payoffs_sender(self):
        try:
            hoi = self.selected + 1
            self.selected = self.selected
        except TypeError:
            if self.participant.vars["too_long"]:  # randomly select task for payment, but not if Task 2 was not played
                self.selected = 1
            else:
                self.selected = random.choice([1, 2])

        # payoffs Task 2 (Button)
        if not self.participant.vars["too_long"]:
            if self.selected_message == "no message":
                message = 0
            else:
                message = 1
            self.participant.vars["payoff2_self"] = Constants.payoff_sender - self.participant.vars["cost_of_sending"] * message
            if self.session.vars["treatment"] == "Punishment":
                if self.participant.vars['punished'] == 1:
                    self.participant.vars["payoff2_self"] = 0
            elif self.session.vars["treatment"] == "Sending Positive":
                self.participant.vars["payoff2_self"] = Constants.payoff_sender + self.participant.vars[
                    "cost_of_sending"] * message
            self.participant.vars["payoff2_self_p"] = str(self.participant.vars["payoff2_self"]) + ' pence'

    def set_payoffs_receiver(self):
        try:
            print(self.selected + 1)
            self.selected = self.selected
        except TypeError:
            if self.participant.vars["too_long"]:  # randomly select task for payment, but not if Task 2 was not played
                self.selected = 1
            else:
                self.selected = random.choice([1, 2])

        # payoffs Task 2 (Button)
        if not self.participant.vars["too_long"]:
            if self.button:
                self.participant.vars["payoff2_self"] = Constants.optionB
                self.participant.vars["payoff2_charity"] = self.payoff_charity
                self.participant.vars["payoff2_self_p"] = str(self.participant.vars["payoff2_self"]) + ' pound'
                self.participant.vars["payoff2_charity_p"] = str(self.participant.vars["payoff2_charity"]) + ' pence'
            else:
                self.participant.vars["payoff2_self"] = Constants.optionA[0]
                self.participant.vars["payoff2_charity"] = Constants.optionA[1]
                self.participant.vars["payoff2_self_p"] = str(self.participant.vars["payoff2_charity"]) + ' pence'
                self.participant.vars["payoff2_charity_p"] = str(self.participant.vars["payoff2_self"]) + ' pence'

    def final_payoffs(self):
        try:
            self.participant.vars["payoff1_self"] = self.participant.vars["payoff1_self"]
            self.participant.vars["payoff1_charity"] = self.participant.vars["payoff1_charity"]
        except KeyError:
            self.participant.vars["payoff1_self"] = "game not played"
            self.participant.vars["payoff1_charity"] = "game not played"

        if self.participant.vars["too_long"]:
            self.participant.vars["payoff2_self_p"] = "game not played"
            self.participant.vars["payoff2_charity_p"] = "game not played"
            self.participant.vars["message"] = ""
        else:
            self.participant.vars["message"] = self.participant.vars["message"]
            if self.participant.vars["payoff2_self"] == 1:
                self.participant.vars["payoff2_self"] = "1.00"
            elif self.participant.vars["payoff2_self"] < 1:
                self.participant.vars["payoff2_self"] = f'{self.participant.vars["payoff2_self"]:.2f}'
            else:
                self.participant.vars["payoff2_self"] = f'{self.participant.vars["payoff2_self"]/100:.2f}'
        self.payoff2_self = self.participant.vars["payoff2_self"]  # to store to the oTree database
        self.payoff2_charity = str(self.participant.vars["payoff2_charity"])

    def get_questions_method3(self):  # only for Senders
        cost = self.participant.vars["cost_of_sending"]
        questions = [
            {
                'question': 'What is the bonus payoff for Player A if they click the button?',
                'options': ['0 pound', '60 pence', str(Constants.optionB) + ' pound'],
                'correct': str(Constants.optionB) + ' pound',
            },
            {
                'question': 'What happens to the donation to the Red Cross if Player A does click the button?',
                'options': ['increases by ' + str(Constants.optionB) + ' pound',
                            'decreases by ' + str(Constants.payoff_sender) + ' pence',
                            'not affected',
                            'decreases or increases: the computer randomly determines by how much'],
                'correct': 'decreases or increases: the computer randomly determines by how much',
            },
            {
                'question': 'What happens to the donation to the Red Cross '
                            'if Player A does **not** click the button?',
                'options': ['increases', 'decreases', 'not affected',
                            'that depends on the situation randomly selected by the computer'],
                'correct': 'not affected',
            },
            {
                'question': 'Suppose you choose communicate a particular consequence of '
                            'pressing the button to the receiver. What does this cost you?',
                'options': ["0 pence", str(cost) + " pence",
                            str(cost) + " pence, but only if the computer "
                                        "randomly selects this consequence to be implemented"],
                'correct': str(cost) + " pence, but only if the computer "
                                       "randomly selects this consequence to be implemented"}]
        if self.session.vars["treatment"] == "Punishment":
            questions.append(
                {
                    'question': 'When can player A cancel your bonus?',
                    'options': ["Never", "Always",
                                "Only if I communicated information about the consequence selected by the computer"],
                    'correct': "Only if I communicated information about the consequence selected by the computer",
                })
        return questions
