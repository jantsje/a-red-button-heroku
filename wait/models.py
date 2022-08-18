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
doc = """
This is the waiting app in between tasks
"""


class Constants(BaseConstants):
    name_in_url = 'wait'
    players_per_group = 2
    num_rounds = 1

    timeout = 5  # in minutes


class Subsession(BaseSubsession):
    def creating_session(self):
        pass

    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= 2:
            return waiting_players[:2]
        for player in waiting_players:
            if player.waiting_too_long():
                # make a single-player group.
                player.participant.vars["too_long"] = True
                return [player]
            else:
                player.participant.vars["too_long"] = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    timeout = models.FloatField()
    time_hidden = models.FloatField()

    def waiting_too_long(self):
        import time
        timespent = time.time() - self.participant.vars["wait_page_arrival"]
        self.time_hidden = (100*timespent)/(60*Constants.timeout)
        return timespent > Constants.timeout * 60

