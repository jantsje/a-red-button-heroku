from ._builtin import Page, WaitPage
from .models import Constants
from .stuff import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG
import random
from django.http.response import HttpResponseRedirect


def vars_for_all_templates(self):
    return {
        'treatment': self.session.vars["treatment"]}


class StartButton(WaitPage):
    group_by_arrival_time = True
    title_text = "Please wait"
    body_text = ""

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class InstructionsTask2(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]

    def before_next_page(self):
        try:
            self.player.prolific_id = self.player.participant.vars["prolific_id"]
        except KeyError:
            self.player.prolific_id = "only button for testing"


class BeforeRequest(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.role == Constants.receiver_role and self.session.vars["treatment"] != "Baseline" \
               and not self.player.participant.vars["too_long"]


class Request(Page):
    form_model = 'player'
    form_fields = ['request']

    def is_displayed(self):
        return self.player.role == Constants.receiver_role and self.session.vars["treatment"] != "Baseline" \
               and not self.player.participant.vars["too_long"]

    def before_next_page(self):
        self.group.store_request()


class TestButton(Page):
    form_model = 'player'
    form_fields = ['button_test', 'store_time_test']
    timeout_seconds = Constants.timer

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class TestButtonClicked(Page):
    form_model = 'player'

    def get_timeout_seconds(self):
        return self.player.store_time_test

    def vars_for_template(self):
        return dict(message=self.player.selected_message,
                    payoff_charity=self.player.payoff_charity)

    def is_displayed(self):
        try:
            self.player.store_time_test > 2
        except TypeError:
            return False
        return self.player.store_time_test > 2 and not self.player.participant.vars["too_long"]


class InstructionsSender(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        return self.player.role == Constants.sender_role and not self.player.participant.vars["too_long"]


class WaitForRequest(WaitPage):
    body_text = "Waiting for Player A to decide about a request."

    def is_displayed(self):
        return self.player.role == Constants.sender_role and \
               (self.session.vars["treatment"] != "Baseline") and not self.player.participant.vars["too_long"]


class Task2Check(UnderstandingQuestionsPage):
    page_title = 'Understanding Check'
    set_correct_answers = False
    form_model = 'player'
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'
    template_name = 'the_button/UnderstandingQuestionsPage3.html'

    def get_questions(self):
        return self.player.get_questions_method3()

    def before_next_page(self):
        self.player.store_uq_button()

    def is_displayed(self):
        return not self.player.participant.vars["too_long"] and not self.player.role == "Receiver"


class SelectMessage(Page):
    form_model = 'player'
    form_fields = []
    for i in range(1, len(Constants.payoffs_charity)+1):
        form_fields.append("message_" + str(i))

    def is_displayed(self):
        return self.player.role == Constants.sender_role and not self.player.participant.vars["too_long"]

    def before_next_page(self):
        self.group.store_message()
        self.player.subtract_cost_of_sending()

    def vars_for_template(self):
        vars_for_this_template = dict()
        if self.session.vars["treatment"] != "Baseline":
            vars_for_this_template.update({'request': self.session.vars["request"]})
        return vars_for_this_template


class WaitForMessage(WaitPage):
    body_text = "Player B is making their choice. Please wait."

    def is_displayed(self):
        return self.player.role == Constants.receiver_role and not self.player.participant.vars["too_long"]


class ReadyForButton(Page):
    def is_displayed(self):
        return self.player.role == Constants.receiver_role and not self.player.participant.vars["too_long"]

    def vars_for_template(self):
        return dict(message=self.player.selected_message,
                    informed=self.player.informed)


class Button(Page):
    form_model = 'player'
    form_fields = ['button', 'store_time']
    timeout_seconds = Constants.timer

    def vars_for_template(self):
        return dict(message=self.player.selected_message)

    def is_displayed(self):
        return self.player.role == Constants.receiver_role and not self.player.participant.vars["too_long"]

    def before_next_page(self):
        self.player.set_payoffs_receiver_button()


class ButtonClicked(Page):
    form_model = 'player'

    def get_timeout_seconds(self):
        return self.player.store_time

    def vars_for_template(self):
        return dict(message=self.player.selected_message,
                    payoff_charity=self.player.payoff_charity)

    def is_displayed(self):
        try:
            self.player.store_time_test > 2
        except TypeError:
            return False
        return self.player.role == Constants.receiver_role and self.player.store_time > 2 \
               and not self.player.participant.vars["too_long"]


class FinalChoice(Page):
    form_model = 'player'
    form_fields = ['punishment']

    def vars_for_template(self):
        return dict(informed=self.player.informed,
                    message=self.player.selected_message,
                    button=self.player.button,
                    request=self.player.request)

    def is_displayed(self):
        return self.player.role == Constants.receiver_role and \
               self.session.vars["treatment"] == "Request + Punishment" \
               and not self.player.participant.vars["too_long"]

    def before_next_page(self):
        self.group.store_punishment()


class WaitForFinalChoice(WaitPage):
    body_text = "Player A is making their choice. Please wait."

    def is_displayed(self):
        return self.player.role == Constants.sender_role and \
               self.session.vars["treatment"] == "Request + Punishment" \
               and not self.player.participant.vars["too_long"]


class SummaryTask2(Page):
    form_model = 'player'

    def vars_for_template(self):
        payoff = str(self.participant.vars["payoff2_self"])
        if payoff == "1":
            payoff = "1 pound"
        else:
            payoff = payoff + " pence"
        vars_for_this_template = dict(
                    request=self.player.request,
                    button=self.player.button,
                    payoff2_self=payoff,
                    message=self.player.selected_message,
                    punished=self.player.punished,
                    punishment=self.player.punishment,
                    informed=self.player.informed
                    )
        return vars_for_this_template

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class FinalQuestions(Page):
    form_model = 'player'

    def get_form_fields(self):
        messages = [self.player.message_1, self.player.message_2, self.player.message_3, self.player.message_4]
        messages_num = messages.count("True")
        form_fields = ['gender', 'age']
        if not self.player.participant.vars["too_long"]:
            if self.player.role == "Sender" and messages_num > 0:
                form_fields.append('send_motivation1')
            elif self.player.role == "Sender" and messages_num == 0:
                form_fields.append('send_motivation2')
            if self.player.role == "Receiver" and self.session.vars["treatment"] != "Baseline":
                form_fields.append('request_motivation')
            if self.player.role == "Receiver":
                form_fields.append('button_motivation')
                if self.session.vars["treatment"] == "Request + Punishment":
                    form_fields.append('punishment_motivation')

        form_fields.append('feedback_pilot')
        form_fields.append('feedback')
        return form_fields

    def vars_for_template(self):
        return dict(too_long=self.player.participant.vars["too_long"],
                    button=self.player.button,
                    punished=self.player.punishment,
                    informed=self.player.informed,
                    request=self.player.request)


class FinalQuestions2(Page):
    form_model = 'player'
    form_fields = ['belief1']

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class FinalQuestions2b(Page):
    form_model = 'player'
    form_fields = ['belief2']

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class FinalQuestions2c(Page):
    form_model = 'player'
    form_fields = ['belief3']

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class FinalQuestions2d(Page):
    form_model = 'player'
    form_fields = ['belief4']

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]


class FinalQuestions2a(Page):
    form_model = 'player'
    form_fields = ['belief0']

    def is_displayed(self):
        return not self.player.participant.vars["too_long"]

    def vars_for_template(self):
        return dict(payoff2_self=self.participant.vars["payoff2_self"])

    def before_next_page(self):
        if self.player.role == "Sender":
            self.player.set_payoffs_sender()
        else:
            self.player.set_payoffs_receiver()
        self.player.final_payoffs()


class Payment(Page):
    form_model = 'player'

    def vars_for_template(self):
        return dict(
            payoff1_self=self.player.participant.vars["payoff1_self"],  # get from previous app (Dana task)
            payoff1_charity=self.player.participant.vars["payoff1_charity"],
            payoff2_self=self.player.participant.vars["payoff2_self"],
            payoff2_charity=self.player.participant.vars["payoff2_charity"],
            punished=self.player.participant.vars["punished"],
            punishment=self.player.punishment,
            too_long=self.player.participant.vars["too_long"],
            message=self.player.participant.vars["message"],
            informed=self.player.informed
        )


class PaymentSelected(Page):
    form_model = 'player'

    def vars_for_template(self):
        try:
            if self.player.participant.vars["payoff2_charity"] == 0:
                payoff2_charity_neg = False
            elif self.player.participant.vars["payoff2_charity"][:1] == "-":
                payoff2_charity_neg = True
            else:
                payoff2_charity_neg = False
        except TypeError:
            payoff2_charity_neg = False
        return dict(
            payoff1_self=self.player.participant.vars["payoff1_self"],
            payoff1_charity=self.player.participant.vars["payoff1_charity"],
            payoff2_self=self.player.participant.vars["payoff2_self"],
            payoff2_charity=self.player.participant.vars["payoff2_charity"],
            payoff2_charity_neg=payoff2_charity_neg,
            selected=self.player.selected,
            punished=self.player.punished,
            punishment=self.player.punishment,
            button=self.player.button,
            too_long=self.player.participant.vars["too_long"],
            message=self.player.participant.vars["message"],
            informed=self.player.informed)

    def js_vars(self):
        cc_code = self.session.config["cc_code"]
        link = "https://app.prolific.co/submissions/complete?cc=" + str(cc_code)
        return dict(
            completionlink=link
        )
    pass


page_sequence = [
    StartButton,
    InstructionsTask2,
    TestButton,
    TestButtonClicked,
    InstructionsSender,
    Task2Check,
    BeforeRequest,
    Request,
    WaitForRequest,
    SelectMessage,
    WaitForMessage,
    ReadyForButton,
    Button,
    ButtonClicked,
    FinalChoice,
    WaitForFinalChoice,
    SummaryTask2,
    FinalQuestions2,
    FinalQuestions2b,
    FinalQuestions2c,
    FinalQuestions2d,
    FinalQuestions2a,
    FinalQuestions,
    Payment,
    PaymentSelected,
]
