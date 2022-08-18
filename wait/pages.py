from ._builtin import Page, WaitPage
from .models import Constants


class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    template_name = 'wait/ResultsWaitPage.html'
    form_fields = ['too_long']

    def js_vars(self):
        return dict(
            timeout=Constants.timeout,
            time_left_prev_page=self.participant.vars["wait_page_arrival"],
            percent=self.player.time_hidden
        )


page_sequence = [ResultsWaitPage]
