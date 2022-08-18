from ._builtin import Page, WaitPage
from .models import Constants
from .stuff import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG
import random


class Welcome(Page):
    form_model = 'player'


class GeneralInstructions(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    def before_next_page(self):
        self.player.browser = self.request.META.get('HTTP_USER_AGENT')
        self.player.participant.vars["prolific_id"] = self.player.prolific_id
        self.player.participant.vars["participation_fee"] = Constants.participation_fee


class InstructionsTask1(Page):
    form_model = 'player'


class Task1Check1(UnderstandingQuestionsPage):
    page_title = 'Understanding Check'
    set_correct_answers = False
    form_model = 'player'
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'
    template_name = 'dana/UnderstandingQuestionsPage.html'

    def get_questions(self):
        return self.player.get_questions_method()

    def before_next_page(self):
        self.player.store_uq_dana()


class Instructions2Task1(Page):
    form_model = 'player'


class Task1Check2(UnderstandingQuestionsPage):
    page_title = 'Understanding Check'
    set_correct_answers = False
    form_model = 'player'
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'
    template_name = 'dana/UnderstandingQuestionsPage2.html'

    def get_questions(self):
        return self.player.get_questions_method2()

    def before_next_page(self):
        self.player.store_uq_dana2()


class Task1Reveal(Page):
    form_model = 'player'
    form_fields = ['reveal', 'task1']

    def before_next_page(self):
        self.player.scenario1 = random.choice([True, False])
        if not self.player.reveal:
            self.player.set_payoffs1()


class Task1(Page):
    form_model = 'player'
    form_fields = ['task1']

    def is_displayed(self):
        return self.player.task1 is None

    def vars_for_template(self):
        return dict(reveal=self.player.reveal, scenario1=self.player.scenario1)

    def before_next_page(self):
        self.player.set_payoffs1()


class SummaryTask1(Page):
    form_model = 'player'

    def vars_for_template(self):
        return dict(reveal=self.player.reveal,
                    payoff1_self=self.player.payoff1_self,
                    payoff1_charity=self.player.payoff1_charity,
                    )

    def before_next_page(self):
        import time
        # start timer to find out how long a person is stuck on next wait page
        self.player.participant.vars["wait_page_arrival"] = time.time()
        self.player.participant.vars["too_long"] = False

page_sequence = [
    Welcome,
    GeneralInstructions,
    InstructionsTask1,
    Task1Check1,
    Instructions2Task1,
    Task1Check2,
    Task1Reveal,
    Task1,
    SummaryTask1
]
