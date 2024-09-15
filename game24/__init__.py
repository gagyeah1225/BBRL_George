
from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'game24'
    players_per_group = 4
    num_rounds = 5
    endowment = cu(100)
    instruction_template = 'game24/instructions.html'
    instructions_template_all = 'game24/instructions_for_all.html'
    num_other_players = players_per_group - 1
    conversion_rate = 0.01


class Subsession(BaseSubsession):
    mpcr = models.FloatField()
    units = models.FloatField()
    real_world_endowment = models.CurrencyField()


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


def understanding1_error_message(player, value):
    group = player.group
    if value != 100:
        return f"Your answer is incorrect. The total amount allocated to the group account is 0 ECUs and the ECUs you " \
               f"keep for yourself is 0. Therefore, everyone, including you, will get a payoff of 100+0.438*0 ECUs " \
               f"each. "


def understanding2_error_message(player, value):
    if value != 43.8:
        return f"Your answer is incorrect. The total amount allocated to the group account are 100 ECUs and the ECUs " \
               f"you keep for yourself is 0. Therefore, your payoff will be 0+0.438*100 ECUs, and everyone else in " \
               f"your group will get a payoff of 100+0.438*100 ECUs each. "


def understanding3_error_message(player, value):
    if value != 175.2:
        return f"Your answer is incorrect. The total amount allocated to the group account are 100*4=400 ECUs and the " \
               f"ECUs you keep for yourself is 0. Therefore, everyone, including you, will get a payoff of " \
               f"0+0.438*400 ECUs each. "


def id_number_error_message(player, string):
    py_list = ['A', 'B', 'C', 'D']
    if string not in py_list:
        return f"Your answer is incorrect, please make sure you have the correct code."


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        label=f"How much do you decide to allocate towards the group account? Please enter an integer from 0 to {Constants.endowment} inclusive."
    )
    next_round = models.IntegerField()


    understanding1 = models.FloatField(
        label='Suppose all group members, including you, keep all their endowment for themselves. What will be your '
              'round payoff? (to the nearest 1 decimal place) ',
        min=0)
    understanding2 = models.FloatField(
        label='Now suppose you allocate 100 ECUs to the group account, and none of the other group members '
              'allocate anything. What will be your round payoff? (to the nearest 1 decimal place) ',
        min=0)
    understanding3 = models.FloatField(
        label='Suppose all group members, including you, each allocates 100 ECUs to the group account, and keeps 0 '
              'for themselves. What will be your round payoff? (to the nearest 1 decimal place) ',
        min=0)
    Helpful = models.StringField(widget=widgets.RadioSelect,
                                 choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                          [2, "Neither Agree or Disagree"], [3, "Agree"],
                                          [4, "Strongly Agree"]],
                                 label='To what extent do you agree with the following statement: "My group members '
                                       'were helpful in solving the puzzle game.”')
    Comfort = models.StringField(widget=widgets.RadioSelect,
                                 choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                          [2, "Neither Agree or Disagree"], [3, "Agree"],
                                          [4, "Strongly Agree"]],
                                 label='To what extent do you agree with the following statement: "I feel comfortable '
                                       'asking for help in solving the puzzle game”')

    Attach = models.StringField(widget=widgets.RadioSelect,
                                choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                         [2, "Neither Agree or Disagree"], [3, "Agree"],
                                         [4, "Strongly Agree"]],
                                label='To what extent do you agree with the following statement: "I feel closely '
                                      'attached to my group.”')
    Familiarity = models.StringField(widget=widgets.RadioSelect,
                                     choices=[[0, "I do not know anyone personally"], [1, "I know 1 person personally"],
                                              [2, "I know 2 people personally"], [3, "I know 3 people personally"]],
                                     label='To what extent are you familiar with your group members personally (for '
                                           'example, are they your classmates, roommates or other)?')

    Helpful1 = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                           [2, "Neither Agree or Disagree"], [3, "Agree"],
                                           [4, "Strongly Agree"]],
                                  label='To what extent do you agree with the following statement: "The group member 1 '
                                        'was helpful in solving the puzzle game.”')
    Helpful2 = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                           [2, "Neither Agree or Disagree"], [3, "Agree"],
                                           [4, "Strongly Agree"]],
                                  label='To what extent do you agree with the following statement: "The group member 2  '
                                        'was helpful in solving the puzzle game.”')
    Helpful3 = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                           [2, "Neither Agree or Disagree"], [3, "Agree"],
                                           [4, "Strongly Agree"]],
                                  label='To what extent do you agree with the following statement: "The group member 3 '
                                        'was helpful in solving the puzzle game.”')


# FUNCTIONS
def creating_session(subsession: Subsession):
    # MPCR = [0.3, 0.75, 0.75, 0.3]
    if Constants.players_per_group == 3:
        subsession.mpcr = 0.5
        # subsession.units = 1.5
    elif Constants.players_per_group == 4:
        subsession.mpcr = 0.438
        # subsession.units = 1.752
    else:
        subsession.mpcr = 0.5
    subsession.units = Constants.players_per_group * subsession.mpcr
    subsession.real_world_endowment = Constants.endowment.to_real_world_currency(subsession.session)


def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    mpcr = group.subsession.mpcr
    group.individual_share = (group.total_contribution * mpcr)
    for p in players:
        p.next_round = p.round_number + 1
        p.payoff = (Constants.endowment - p.contribution) + group.individual_share





class Sent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    form_model = 'player'
    form_fields = ['Helpful', 'Helpful1', 'Helpful2', 'Helpful3', 'Comfort', 'Attach', 'Familiarity']


class Introduction_all_games(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

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
            'num_other_players': Constants.players_per_group - 1,
            #       'real_endowment': f'{Decimal(Constants.endowment) * Constants.conversion_rate} VND'
        }


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


class Finalresults(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    def vars_for_template(Player):
        group = Player.group
        # part1 = [Player.in_round(1).E_part1]
        # puzzle1 = [Player.in_round(1).E_puzzle1]
        # Part1_game_selected = [Player.in_round(1).E_selected]
        participant = Player.participant
        p_p1 = ["Group Total Allocation"]
        if Player.round_number == Constants.num_rounds:
            for i in range(1, Constants.num_rounds + 1):
                prv = Player.in_round(i)
                pp_phrase1 = ["Period " + str(i) + " payoff is "]
                pp = [float(prv.payoff)]
                grv = group.in_round(i)
                pp_phrase2 = ["Period " + str(i) + " total allocation is "]
                pp1 = [float(grv.total_contribution)]
                pp_phrase3 = ["Period " + str(i) + " personal allocation is "]
                pp2 = [float(prv.contribution)]
                p_p1 = p_p1 + pp_phrase1 + pp + pp_phrase2 + pp1 + pp_phrase3 + pp2
            # p_p1 = p_p1 + part1 + puzzle1 + Part1_game_selected
            p_p1 = p_p1

            Player.participant.vars['Contributions'] = p_p1
            return dict(Contributions=p_p1)


page_sequence = [ Sent, Introduction_all_games, Introduction, Understanding, Understood, Decision, ResultsWaitPage, Results,
                 Finalresults]
# page_sequence = [Introduction, Understanding, Understood, Decision, ResultsWaitPage, Results,Finalresults]
