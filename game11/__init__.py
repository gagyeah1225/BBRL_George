import random

from otree.api import *
from otree.models import player, group


class Constants(BaseConstants):
    name_in_url = 'game11'
    players_per_group = None
    num_rounds = 5
    conversion_rate = 0.01
    volunteer_timeout = 30
    instructions_template = 'game11/instructions.html'
    instructions_template_all = 'game11/instructions_for_all.html'
    num_other_players = 0

    # """Payoff for each player if at least one volunteers"""
    general_benefit = cu(100)

    # """Cost incurred by volunteering player"""
    volunteer_cost = cu(20)


class Subsession(BaseSubsession):
    pass


def record_round_start(group):
    import time
    player.start_timestamp = time.time()


class Group(BaseGroup):
    pass


def set_payoffs(group: Group):
    players = group.get_players()
    for p in players:
        p.next_round = p.round_number + 1
        volunteer1 = p.volunteer
        volunteers_together1 = [volunteer1] + [p.picked1] + [p.picked2]
        p.num_volunteers = int(sum(volunteers_together1))
        if p.num_volunteers > 0:
            baseline_amount = Constants.general_benefit
            if p.volunteer:
                p.payoff = baseline_amount - Constants.volunteer_cost
            else:
                p.payoff = baseline_amount
        else:
            baseline_amount = cu(50)
            p.payoff = baseline_amount


def understanding1_error_message(player, value):
    group = player.group
    if value != 50:
        return f"Your answer is incorrect. Please remember that, 'If no one invests in your group, all members of the " \
               f"group will get a payoff of 50 ECUs.' "


def understanding2_error_message(player, value):
    if value != 100:
        return f"Your answer is incorrect. Please remember that, 'If at least one group member invests, the other group " \
               f"members will get a payoff of 100 ECUs and the payoff of the person or computer bot that invests will "\
               f"be 80 ECUs.'"

def understanding3_error_message(player, value):
    if value != 80:
        return f"Your answer is incorrect. Please remember that, 'If at least one group member invests, the other group " \
               f"members will get a payoff of 100 ECUs and the payoff of the person or computer bot that invests will "\
               f"be 80 ECUs.'"


def id_number_error_message(player, string):
    py_list = ['D']
    if string not in py_list:
        return f"Your answer is wrong, please make sure you have the correct code "


class Player(BasePlayer):
    next_round = models.IntegerField()
    picked1 = models.IntegerField()
    picked2 = models.IntegerField()
    num_volunteers = models.IntegerField()
    start_timestamp = models.FloatField()
    volunteer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label=f"Do you wish to invest?")
    id_number = models.StringField(label=f"What is your ID number?")
    submission_timestamp = models.FloatField()
    understanding1 = models.IntegerField(
        label='Assuming no one in your group invests, what will be your round payoff?',
        min=0)

    understanding2 = models.IntegerField(
        label='Assuming you do not invest but a computer bot invests, what will be your round payoff?',
        min=0)
    understanding3 = models.IntegerField(
        label='Assuming you invest but no one else in your group invests, what will be your round payoff?',
        min=0)


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


class WaitToStart(WaitPage):
    after_all_players_arrive = 'record_round_start'
    title_text = 'Waiting for other players to begin'


class Decision(Page):
    form_model = 'player'
    form_fields = ['volunteer']

    timer_text = 'You have 30 seconds to decide.'

    @staticmethod
    def is_displayed(Player):
        group = Player.group
        # Expecting will always be (just under) 30s left,
        import time
        return Constants.volunteer_timeout - time.time() + player.start_timestamp > 1

    @staticmethod
    def before_next_page(Player, timeout_happened):
        group = Player.group
        import time
        # Convert to a relative timestamp (in seconds):
        Player.submission_timestamp = time.time() - player.start_timestamp

    @staticmethod
    def get_timeout_seconds(Player):
        group = Player.group
        import time
        return Constants.volunteer_timeout - time.time() + player.start_timestamp

    @staticmethod
    def before_next_page(player, timeout_happened):
        number_selected1 = random.randrange(0, 2, 1)
        number_selected2 = random.randrange(0, 2, 1)
        player.picked1 = number_selected1  # Added to allow players to different numbers picked per player
        player.picked2 = number_selected2  # Added to allow players to different numbers picked per player


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


class Finalresults(Page):
    def is_displayed(Player):
        return Player.round_number == Constants.num_rounds

    def vars_for_template(Player):
        group = Player.group
        pp21 = [" "]
        participant = Player.participant
        p_p3 = ["Number of investors in your group"]
        if Player.round_number == Constants.num_rounds:
            for i in range(1, Constants.num_rounds + 1):
                prv = Player.in_round(i)
                pp_phrase1 = ["Period " + str(i) + " payoff is "]
                pp = [float(prv.payoff)]
                # grv = group.in_round(i)
                pp_phrase2 = ["Period " + str(i) + " total number of volunteers is "]
                pp1 = [prv.num_volunteers]
                pp_phrase3 = ["Period " + str(i) + " decision was to "]
                pp2 = [float(prv.volunteer)]
                if pp2 == 1.0:
                    pp21 = ["Invest"]
                else:
                    pp21 = ["Do not invest"]
                p_p3 = p_p3 + pp_phrase1 + pp + pp_phrase2 + pp1 + pp_phrase3 + pp21
                Player.participant.vars['Decisions1'] = p_p3
            return dict(Decisions1=p_p3)


#page_sequence = [Introduction, WaitToStart, Decision, ResultsWaitPage, Results, Finalresults]

page_sequence = [Check, Introduction_all_games, Introduction, Understanding, Understood, WaitToStart, Decision,
                 ResultsWaitPage, Results, Finalresults]
