from random import random, randrange
import random

from otree.api import *

c = Currency

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'EG'
    players_per_group = None
    num_rounds = 1

    choice_1_high = 84
    choice_2_high = 108
    choice_3_high = 132
    choice_4_high = 156
    choice_5_high = 180
    choice_6_high = 210

    choice_1_low = 84
    choice_2_low = 72
    choice_3_low = 60
    choice_4_low = 48
    choice_5_low = 36
    choice_6_low = 6
    instruction_template = 'EG/instruction.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery_win = models.IntegerField(initial=random.randrange(0, 2))
    lottery_selected = models.IntegerField()
    choice = models.IntegerField(
        choices=[
            [1, "Lottery 1"],
            [2, "Lottery 2"],
            [3, "Lottery 3"],
            [4, "Lottery 4"],
            [5, "Lottery 5"],
            [6, "Lottery 6"],
        ]
    )


def set_payoffs(group: Group):
    players = group.get_players()
    list_high = [Constants.choice_1_high, Constants.choice_2_high, Constants.choice_3_high, Constants.choice_4_high,
                 Constants.choice_5_high, Constants.choice_6_high]

    list_low = [Constants.choice_1_low, Constants.choice_2_low, Constants.choice_3_low, Constants.choice_4_low,
                Constants.choice_5_low, Constants.choice_6_low]
    for p in players:
        Player.chosen = p.choice - 1
        if p.lottery_selected == 1:  # Change back to lottery_win if you want all gambles chosen to be the same.
            p.payoff = list_high[Player.chosen]
        else:
            p.payoff = list_low[Player.chosen]


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def before_next_page(player, timeout_happened):
        lottery_selected = random.randrange(0, 2)
        player.lottery_selected = lottery_selected  # Added to allow players to different numbers picked per player


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


class Finalresults(Page):
    def is_displayed(Player):
        return Player.round_number == Constants.num_rounds

    def vars_for_template(Player):
        group = Player.group
        round_select = Player.in_round(1).lottery_selected
        participant = Player.participant
        p_p4 = ["Risk"]
        if round_select == 0:
            round_selected = ["Tails"]
        elif round_select == 1:
            round_selected = ["Heads"]
        if Player.round_number == Constants.num_rounds:
            for i in range(1, Constants.num_rounds + 1):
                prv = Player.in_round(i)
                ppr = [float(prv.payoff)]
                p_p4 = p_p4 + ppr
            p_p4 = p_p4 + round_selected
            Player.participant.vars['Risk_payoff'] = p_p4
            return dict(Decisions=p_p4)


page_sequence = [MyPage, ResultsWaitPage, Results, Finalresults]
