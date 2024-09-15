import random

from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'game21'
    players_per_group = None
    num_rounds = 5
    endowment = 100
    instruction_template = 'game21/instructions.html'
    instructions_template_all = 'game21/instructions_for_all.html'
    conversion_rate = 0.01


class Subsession(BaseSubsession):
    mpcr = models.FloatField()
    real_world_endowment = models.IntegerField()


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    # individual_share = models.CurrencyField()


def understanding1_error_message(player, value):
    group = player.group
    if value != 100:
        return f"Your answer is incorrect. The total amount allocated to the group account is 0 ECUs and the ECUs you " \
               f"each keep for yourselves will be 100. Therefore, everyone, including you, will get a payoff of " \
               f"100+0.5*0 ECUs each. "


def understanding2_error_message(player, value):
    if value != 50:
        return f"Your answer is incorrect. The total amount allocated to the group account are 100 ECUs and the ECUs you " \
               f"keep for yourself is 0. Therefore, your payoff will be 0+0.5*100 ECUs, and everyone else in your " \
               f"group will get a payoff of 100+0.5*100. "


def understanding3_error_message(player, value):
    if value != 150:
        return f"Your answer is incorrect. The total amount allocated to the group account are 300 ECUs and the ECUs " \
               f"you keep for yourself is 0. Therefore, everyone, including you, will get a payoff of 0+0.5*300 ECUs " \
               f"each. "


def id_number_error_message(player, string):
    py_list = ['D']
    if string not in py_list:
        return f"Your answer is wrong, please make sure you have the correct code "


class Player(BasePlayer):
    next_round = models.IntegerField()
    totalcontributions = models.IntegerField()
    individualshare = models.IntegerField()
    picked1 = models.IntegerField()
    picked2 = models.IntegerField()
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        label=f"How much do you decide to allocate towards the group account? Please enter an integer from 0 to {Constants.endowment} inclusive."
    )
    id_number = models.StringField(widget=widgets.RadioSelect,
                                   choices=[["D", "D"]],
                                   label=f"Enter player id to begin")

    understanding1 = models.IntegerField(
        label='Suppose all group members, including you, keep all their endowment for themselves. What will be your '
              'round payoff? ',
        min=0)
    understanding2 = models.IntegerField(
        label='Now suppose you allocate 100 ECUs to the group account, and none of the other group members '
              'allocate anything. What will be your round payoff? ',
        min=0)
    understanding3 = models.IntegerField(
        label='Suppose all group members, including you, each allocates 100 ECUs to the group account, and keeps 0 '
              'for themselves. What will be your round payoff? ',
        min=0)


# FUNCTIONS
def creating_session(subsession: Subsession):
    # MPCR = [0.3, 0.75, 0.75, 0.3]
    subsession.mpcr = 0.5
    #subsession.real_world_endowment = Constants.endowment.to_real_world_currency(subsession.session)




def set_payoffs(group: Group):
    players = group.get_players()
    for p in players:
        # contributions = [p.contribution for p in players]
        p.next_round = p.round_number + 1
        contributions1 = p.contribution
        contributions_together1 = [contributions1] + [p.picked1] + [p.picked2]
        p.totalcontributions = sum(contributions_together1)
        p.individualshare = int(0.5 * p.totalcontributions)
        # for p in players:
        p.payoff = (Constants.endowment - p.contribution) + p.individualshare


class Check(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    form_model = 'player'
    form_fields = ['id_number']


class Introduction_all_games(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    form_model = 'player'


class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


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


class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'num_other_players': 0,
            #       'real_endowment': f'{Decimal(Constants.endowment) * Constants.conversion_rate} VND'
        }

    def before_next_page(player, timeout_happened):
        number_selected1 = random.randrange(50, 60, 10)
        number_selected2 = random.randrange(50, 60, 10)
        player.picked1 = number_selected1  # Added to allow players to different numbers picked per player
        player.picked2 = number_selected2  # Added to allow players to different numbers picked per player


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


class Finalresults(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    def vars_for_template(Player):
        group = Player.group
        participant = Player.participant
        p_p1 = ["Group Total Allocation"]
        if Player.round_number == Constants.num_rounds:
            for i in range(1, Constants.num_rounds + 1):
                prv = Player.in_round(i)
                pp_phrase1 = ["Period " + str(i) + " payoff is "]
                pp = [float(prv.payoff)]
                #grv = group.in_round(i)
                pp_phrase2 = ["Period " + str(i) + " total allocation is "]
                pp1 = [float(prv.totalcontributions)]
                pp_phrase3 = ["Period " + str(i) + " personal allocation is "]
                pp2 = [float(prv.contribution)]
                p_p1 = p_p1 + pp_phrase1 + pp + pp_phrase2 + pp1 + pp_phrase3 + pp2
                Player.participant.vars['Contributions'] = p_p1
            return dict(Contributions=p_p1)


page_sequence = [Check, Introduction_all_games, Introduction, Understanding, Understood, Decision, ResultsWaitPage, Results,
                 Finalresults]
