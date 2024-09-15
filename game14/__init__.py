from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'game14'
    players_per_group = 4
    num_rounds = 5
    conversion_rate = 0.01
    volunteer_timeout = 30
    instructions_template = 'game14/instructions.html'
    instructions_template_all = 'game14/instructions_for_all.html'
    num_other_players = players_per_group - 1

    # """Payoff for each player if at least one volunteers"""
    general_benefit = cu(100)

    # """Cost incurred by volunteering player"""
    volunteer_cost = cu(20)


class Subsession(BaseSubsession):
    pass


def record_round_start(group):
    import time
    group.start_timestamp = time.time()


def set_payoffs(group):
    players = group.get_players()
    group.num_volunteers = sum([p.volunteer for p in players])
    group.timing = min([p.submission_timestamp for p in players])
    # timing1 = round(group.timing, 7)
    # volunteer_timing = []
    for p in players:
        p.next_round = p.round_number + 1
        if group.num_volunteers == 1:
            baseline_amount = Constants.general_benefit
            if p.volunteer:
                # if p.submission_timestamp == min(Player.submission_timestamp for Player in players):
                p.payoff = baseline_amount - Constants.volunteer_cost
            if not p.volunteer:
                p.payoff = baseline_amount
        elif group.num_volunteers > 1:
            baseline_amount = Constants.general_benefit
            if p.volunteer:
                # volunteer_timing= [] + Player.submission_timestamp
                if p.submission_timestamp == min(Player.submission_timestamp for Player in players):
                    p.payoff = baseline_amount - Constants.volunteer_cost
                else:
                    p.payoff = baseline_amount
            if not p.volunteer:
                p.payoff = baseline_amount
        else:
            baseline_amount = cu(50)
            p.payoff = baseline_amount


class Group(BaseGroup):
    start_timestamp = models.FloatField()
    num_volunteers = models.IntegerField()
    timing = models.FloatField()


def understanding1_error_message(player, value):
    group = player.group
    if value != 50:
        return f"Your answer is incorrect. Please remember that, 'If no one invests in your group, all members of the " \
               f"group will get a payoff of 50 ECUs.' "


def understanding2_error_message(player, value):
    if value != 80:
        return f"Your answer is incorrect. Please remember that, 'If more than 1 person invests, the payoff of the first " \
               f"person to invest will be 80 ECUs and the other group members will get a payoff of 100 ECUs each.' "


def understanding3_error_message(player, value):
    if value != 100:
        return f"Your answer is incorrect. Please remember that, 'If at least one group member invests, the other group " \
               f"members will get a payoff of 100 ECUs and the payoff of the person that invests will be 80 ECUs.' "


def id_number_error_message(player, string):
    py_list = ['A', 'B', 'C', 'D']
    if string not in py_list:
        return f"Your answer is incorrect, please make sure you have the correct code."


class Player(BasePlayer):
    next_round = models.IntegerField()
    volunteer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label='Do you wish to '
                                                                                                 'invest?')
    id_number = models.StringField(widget=widgets.RadioSelect,
                                   choices=[["A", "A"], ["B", "B"],
                                            ["C", "C"], ["D", "D"]],
                                   label=f"Enter player id to begin")
    E_part1 = models.FloatField(label=f"Part I earnings")
    E_selected = models.IntegerField(label=f"Part I selected game")
    E_puzzle1 = models.FloatField(label=f"Part I Puzzle Earnings")
    submission_timestamp = models.FloatField()
    understanding1 = models.IntegerField(
        label=' Assuming no one in your group invests, what will be your round payoff?',
        min=0)
    understanding2 = models.IntegerField(
        label=' Assuming someone in your group invests but you invest first, what will be your round payoff?',
        min=0)
    understanding3 = models.IntegerField(
        label=' Assuming you do not invest but someone else invests, what will be your round payoff?',
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
                                  label='To what extent do you agree with the following statement: "The group member sitting on my left '
                                        'was helpful in solving the puzzle game.”')
    Helpful2 = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                           [2, "Neither Agree or Disagree"], [3, "Agree"],
                                           [4, "Strongly Agree"]],
                                  label='To what extent do you agree with the following statement: "The group member sitting on my right '
                                        'was helpful in solving the puzzle game.”')
    Helpful3 = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Strongly Disagree"], [1, "Disagree"],
                                           [2, "Neither Agree or Disagree"], [3, "Agree"],
                                           [4, "Strongly Agree"]],
                                  label='To what extent do you agree with the following statement: "The group member sitting opposite me '
                                        'was helpful in solving the puzzle game.”')


class Check(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    form_model = 'player'
    form_fields = ['id_number', 'E_part1', 'E_selected', 'E_puzzle1']


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
        return Constants.volunteer_timeout - time.time() + group.start_timestamp > 1

    @staticmethod
    def before_next_page(Player, timeout_happened):
        group = Player.group
        import time
        # Convert to a relative timestamp (in seconds):
        # Player.submission_timestamp = time.time() - group.start_timestamp
        if Player.volunteer:
            Player.submission_timestamp = time.time() - group.start_timestamp
        else:
            Player.submission_timestamp = 30 + time.time() - group.start_timestamp

    @staticmethod
    def get_timeout_seconds(Player):
        group = Player.group
        import time
        return Constants.volunteer_timeout - time.time() + group.start_timestamp


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


class Finalresults(Page):
    def is_displayed(Player):
        return Player.round_number == Constants.num_rounds

    def vars_for_template(Player):
        group = Player.group
        part1 = [Player.in_round(1).E_part1]
        puzzle1 = [Player.in_round(1).E_puzzle1]
        Part1_game_selected = [Player.in_round(1).E_selected]
        pp21 = [" "]
        participant = Player.participant
        p_p3 = ["Number of investors in your group"]
        if Player.round_number == Constants.num_rounds:
            for i in range(1, Constants.num_rounds + 1):
                prv = Player.in_round(i)
                pp_phrase1 = ["Period " + str(i) + " payoff is "]
                pp = [float(prv.payoff)]
                grv = group.in_round(i)
                pp_phrase2 = ["Period " + str(i) + " total number of volunteers is "]
                pp1 = [grv.num_volunteers]
                pp_phrase3 = ["Period " + str(i) + " decision was to "]
                pp2 = [float(prv.volunteer)]
                if pp2 == 1.0:
                    pp21 = ["Invest"]
                else:
                    pp21 = ["Do not invest"]
                p_p3 = p_p3 + pp_phrase1 + pp + pp_phrase2 + pp1 + pp_phrase3 + pp21
            p_p3 = p_p3 + part1 + puzzle1 + Part1_game_selected
            Player.participant.vars['Decisions1'] = p_p3  # + part1 + puzzle1
            return dict(Decisions1=p_p3)


# page_sequence = [Introduction_all_games, Introduction, WaitToStart, Decision,
#                 ResultsWaitPage, Results, Finalresults]

page_sequence = [Check, Sent, Introduction_all_games, Introduction, Understanding, Understood, WaitToStart, Decision,
                 ResultsWaitPage, Results, Finalresults]
