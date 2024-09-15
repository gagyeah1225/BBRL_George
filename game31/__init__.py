import random
from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'Game31'
    players_per_group = None
    num_rounds = 5
    a = 1
    b = 0.75
    h = 85
    maximum_effort = 70
    instruction_template = 'game31/instruction.html'
    conversion_rate = 0.01


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minimum_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


def understanding1_error_message(player, value):
    group = player.group
    if value != 58:
        return f"Your answer is incorrect. Please see from the table below that, if you choose to spend 50 hours on the activity and the minimum number of " \
               f"hours in your group is 10 hours, then your round payoff will be determined by tracing row 50 for 'your " \
               f"hours' and column 10 for 'group minimum hours' in the payoff table."


def understanding2_error_message(player, value):
    if value != 90:
        return f"Your answer is incorrect. Please see from the table below that, if you choose to spend 20 hours on the activity and the minimum number of " \
               f"hours in the group is 20 hours, then your round payoff will be determined by tracing row 20 for 'your " \
               f"hours' and column 20 for 'group minimum hours' in the payoff table."


def understanding3_error_message(player, value):
    if value != 43:
        return f"Your answer is incorrect. Please see from the table below that, if you choose to spend 70 hours on the activity and the minimum number of " \
               f"hours in your group is 10 hours, then your round payoff will be determined by tracing row 70 for 'your " \
               f"hours' and column 10 for 'group minimum hours' in the payoff table."


class Player(BasePlayer):
    minimum_contribution1 = models.IntegerField()
    maximum_contribution1 = models.IntegerField()
    next_round = models.IntegerField()
    picked1 = models.IntegerField()
    picked2 = models.IntegerField()
    contribution = models.IntegerField(
        min=0, max=Constants.maximum_effort, choices=[10, 20, 30, 40, 50, 60, 70],
        label=f"How many hours do you want to spend on the activity between 10 and {Constants.maximum_effort}?"
    )
    understanding1 = models.IntegerField(
        label='Assuming you chose to spend 50 hours on the activity, and the minimum number of hours chosen in your '
              'group is 10 hours, what will be your round payoff?',
        min=0)
    understanding2 = models.IntegerField(
        label='Assuming you chose to spend 20 hours on the activity, and the minimum number of hours chosen in your '
              'group is 20 hours, what will be your round payoff?',
        min=0)
    understanding3 = models.IntegerField(
        label='Assuming you chose to spend 70 hours on the activity, and the minimum number of hours chosen in your '
              'group is 10 hours, what will be your round payoff?',
        min=0)


def set_payoffs(group: Group):
    players = group.get_players()
    for p in players:
        # contributions = [p.contribution for p in players]
        p.next_round = p.round_number + 1
        contributions1 = p.contribution
        contributions_together1 = [contributions1] + [p.picked1] + [p.picked2]
        p.minimum_contribution1 = min(contributions_together1)
        p.maximum_contribution1 = max(contributions_together1)
        # for p in players:
        p.payoff = ((Constants.a * min([p.contribution, p.minimum_contribution1])) - (
                Constants.b * p.contribution)) + Constants.h


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def before_next_page(player, timeout_happened):
        number_selected1 = random.randrange(50, 60, 10)
        number_selected2 = random.randrange(50, 60, 10)
        player.picked1 = number_selected1  # Added to allow players to different numbers picked per player
        player.picked2 = number_selected2  # Added to allow players to different numbers picked per player


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Understanding(Page):
    form_model = 'player'
    form_fields = ['understanding1', 'understanding2', 'understanding3']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Understood(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Results(Page):
    pass


class Finalresults(Page):
    def is_displayed(Player):
        return Player.round_number == Constants.num_rounds

    def vars_for_template(Player):
        group = Player.group
        participant = Player.participant
        p_p = ["Group Minimum"]
        if Player.round_number == Constants.num_rounds:
            for i in range(1, Constants.num_rounds + 1):
                prv = Player.in_round(i)
                pp_phrase1 = ["Period " + str(i) + " payoff is "]
                pp = [float(prv.payoff)]
                # grv = group.in_round(i) #Replaced in this code cos there is no more group minimum
                pp_phrase2 = ["Period " + str(i) + " group minimum is "]
                pp1 = [float(prv.minimum_contribution1)]
                pp_phrase3 = ["Period " + str(i) + " effort level is "]
                pp2 = [float(prv.contribution)]
                p_p = p_p + pp_phrase1 + pp + pp_phrase2 + pp1 + pp_phrase3 + pp2
                Player.participant.vars['Decisions'] = p_p
            return dict(Decisions=p_p)


# page_sequence = [Introduction, Decision, ResultsWaitPage, Results, Finalresults]

page_sequence = [Introduction, Understanding, Understood, Decision, ResultsWaitPage, Results, Finalresults]
