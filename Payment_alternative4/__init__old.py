from otree.api import *
import random

c = cu

doc = 'Show questionnaire (and collect payment details), report payoffs from previous apps.'


class Constants(BaseConstants):
    name_in_url = 'questionnaire_and_payment4'
    players_per_group = None
    num_rounds = 1
    conversion_rate = 0.01


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    totalpoints_currency = models.FloatField()
    Paymentsused = models.CurrencyField()
    round_selected = models.IntegerField()
    age = models.IntegerField(label='What is your age?', min=0, max=100)
    gender = models.StringField(widget=widgets.RadioSelect,
                                choices=[[0, 'Male'], [1, 'Female'], [2, 'Other'],
                                         [3, 'Prefer not to say']], label='What is your gender?')
    Marital_status = models.StringField(widget=widgets.RadioSelect,
                                        choices=[[0, 'Single/Never Married'],
                                                 [1, 'Married/Has Domestic Partner'],
                                                 [2, 'Divorced/Separated'],
                                                 [3, 'Prefer Not to Say']],
                                        label='What is your marital status?')
    Residence = models.StringField(widget=widgets.RadioSelect, choices=[[1, "Yes"], [0, "No"]],
                                   label="Do you live with your parents outside of school? ")
    Residence1 = models.StringField(label="What zip code did you grow up in?")
    Education = models.StringField(widget=widgets.RadioSelect,
                                   choices=[[0, "Some College"], [1, "College Degree"],
                                            [2, "Postgraduate"]], label='Education level')
    Major = models.StringField(label='What is your major at the University of Arkansas?')
    understanding = models.StringField(widget=widgets.RadioSelect,
                                       choices=[[0, 'Not at all'], [1, 'A little'],
                                                [2, 'Average'], [3, 'Quite well'],
                                                [4, 'Completely']],
                                       label='How well do you believe that you understood the instructions of '
                                             'experiment? ')

    Income = models.StringField(choices=[[0, 'Less than $49,999 '], [1, '$50,000 - $79,999'],
                                         [2, '$80,000 - $109,000'], [3, '$110,000- $139,999'],
                                         [4, '$140,000 - $199,999'], [5, 'Over $200,000']],
                                widget=widgets.RadioSelect,
                                label="Which category best describes your annual family income?")
    Volunteering = models.StringField(widget=widgets.RadioSelect,
                                      choices=[[0, "Did not volunteer"], [1, "Volunteered less than 3 times "],
                                               [2, "Volunteered up to 5 times"],
                                               [3, "Volunteered less than 10 times"],
                                               [4, "Volunteered more than 10 times"]],
                                      label='Approximately how many times did you volunteer in the past year?')

    Employment_status = models.StringField(widget=widgets.RadioSelect,
                                           choices=[[0, "Not working outside home"], [1, "Student"],
                                                    [2, "Employed"]],
                                           label="What is your employment status?")

    # Occupation = models.StringField(label="12.	Please indicate your primary occupation if you chose other above ")

    Salary = models.StringField(widget=widgets.RadioSelect,
                                choices=[[0, "Less than $13,999"], [1, "$14,000 - $27,999"],
                                         [2, "$28,000 - $43,999"], [3, "$44,000 - $65,999"],
                                         [4, "$66,000 - $89,000"],
                                         [5, "$90,000 or above"]],
                                label="What is your salary per year?")

    Finances = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Prefer not to answer"], [1, "Poor"],
                                           [2, "Not so good"], [3, "Good"],
                                           [4, "Very good"],
                                           [5, "Excellent"]],
                                  label="How would you describe the state of your own personal finances these days? ")

    Religion = models.StringField(widget=widgets.RadioSelect,
                                  choices=[[0, "Christian (Catholic) "], [1, "Christian (Other)"],
                                           [2, "Muslim"], [3, "Jewish"],
                                           [4, "Hindu"],
                                           [5, "Buddhist"], [6, "Other"]],
                                  label="Primary Religious Affiliation")

    Race = models.StringField(widget=widgets.RadioSelect,
                              choices=[[0, "White"], [1, "African-American/Black"],
                                       [2, "Hispanic"], [3, "American Indian or Native Alaskan"],
                                       [4, "Asian (Chinese, Japanese, Korean, etc.) or Pacific"],
                                       [5, "Indian Subcontinent "], [6, "Middle Eastern "],
                                       [7, 'Some other ethnicity']],
                              label="What is your ethnicity ?")

    # Race1 = models.StringField(label="If you chose other above, please specify")

    Political = models.StringField(widget=widgets.RadioSelect,
                                   choices=[[0, "Republican Party"], [1, "Democratic Party"], [2, "Independent"],
                                            [3, "Other"]],
                                   label="In politics today, do you consider yourself a Republican, a Democrat, "
                                         "an Independent, or something else?")
    Res = models.StringField(widget=widgets.RadioSelect,
                             choices=[[0, "Strongly Agree"], [1, "Agree"], [2, "Neither Agree or Disagree"],
                                      [3, "Disagree"], [3, "Strongly Disagree"]],
                             label='To what extent do you agree with the following statement: "I see myself as '
                                   'someone who is reserved."')
    Soc = models.StringField(widget=widgets.RadioSelect,
                             choices=[[0, "Strongly Agree"], [1, "Agree"], [2, "Neither Agree or Disagree"],
                                      [3, "Disagree"], [3, "Strongly Disagree"]],
                             label='To what extent do you agree with the following statement: "I see myself as '
                                   'someone who is outgoing, sociable."')
    Game1 = models.StringField(widget=widgets.RadioSelect,
                               choices=[[0, 'Not at all'], [1, 'A little'],
                                        [2, 'Average'], [3, 'Quite well'],
                                        [4, 'Completely']],
                               label='How familiar were you with Game 1 (Group Account Contribution Game) before the '
                                     'study today?')
    Game2 = models.StringField(widget=widgets.RadioSelect,
                               choices=[[0, 'Not at all'], [1, 'A little'],
                                        [2, 'Average'], [3, 'Quite well'],
                                        [4, 'Completely']],
                               label='How familiar were you with Game 2 (Group Hours Spent on Activity Game) before '
                                     'the study today?')
    Game3 = models.StringField(widget=widgets.RadioSelect,
                               choices=[[0, 'Not at all'], [1, 'A little'],
                                        [2, 'Average'], [3, 'Quite well'],
                                        [4, 'Completely']],
                               label='How familiar were you with Game 3 (The Lottery Game) before the '
                                     'study today?')


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'Marital_status', 'Residence', 'Residence1', 'Education', 'Major', 'understanding',
                   'Income', 'Volunteering', 'Employment_status', 'Salary', 'Finances', 'Religion', 'Race', 'Political',
                   'Res', 'Soc', 'Game1', 'Game2', 'Game3'
                   ]

    @staticmethod
    def before_next_page(player, timeout_happened):
        round_selected = random.randrange(0, 2)
        player.round_selected = round_selected


class ResultsWaitPage(WaitPage):
    pass


class Payments(Page):
    form_model = 'player'

    def vars_for_template(Player):
        group = Player.group
        participant = Player.participant
        participant_pay = list(participant.vars.values())
        Payments = []
        Payments1 = participant_pay[0]
        Payments2 = participant_pay[1]
        Payments3 = participant_pay[2]
        # Payments4 = participant_pay[3]

        Payments = [Payments1] + [Payments2] + [Payments3]
        risk_pay = Payments[2]
        Previous_earnings = Payments[0]
        amount_owned = Payments[Player.round_selected]  ###Times exchange rate if applicable
        rr = risk_pay[1]
        Part1 = Previous_earnings[31]
        Puzzle1 = round(Previous_earnings[32], 2)
        r1c2 = amount_owned[0]
        r2c2 = amount_owned[2]
        r2c3 = amount_owned[4]
        r2c4 = amount_owned[6]
        r3c2 = amount_owned[8]
        r3c3 = amount_owned[10]
        r3c4 = amount_owned[12]
        r4c2 = amount_owned[14]
        r4c3 = amount_owned[16]
        r4c4 = amount_owned[18]
        r5c2 = amount_owned[20]
        r5c3 = amount_owned[22]
        r5c4 = amount_owned[24]
        r6c2 = amount_owned[26]
        r6c3 = amount_owned[28]
        r6c4 = amount_owned[30]
        ppp = [r2c2] + [r3c2] + [r4c2] + [r5c2] + [r6c2] + [rr]
        Points_nrr = [r2c2] + [r3c2] + [r4c2] + [r5c2] + [r6c2]
        Points1 = sum(Points_nrr)
        Points = sum(ppp)
        points_total = sum(ppp + [Part1] + [Puzzle1])
        points_currency = round(sum(ppp + [Part1]) * Constants.conversion_rate, 2)
        final_currency = round((sum(ppp + [Part1] + [Puzzle1]) * Constants.conversion_rate) + 7, 2)
        Player.totalpoints_currency = round(points_total, 2)
        Player.payoff = c(final_currency)
        return dict(total=final_currency, pointscurrency=points_currency, pointstotal=points_total, aa=Part1,
                    ab=Puzzle1,
                    a1=r1c2, a2=r2c2, a3=r2c3, a4=r2c4,
                    a5=r3c2, a6=r3c3, a7=r3c4,
                    a8=r4c2, a9=r4c3, a10=r4c4,
                    a11=r5c2, a12=r5c3, a13=r5c4,
                    a14=r6c2, a15=r6c3, a16=r6c4, rr_msg=rr, Points_earned=Points, points_from_2=Points1,
                    game_selected=Player.round_selected + 1, pay_me=amount_owned)


class Payments1(Page):
    form_model = 'player'

    def vars_for_template(Player):
        group = Player.group
        participant = Player.participant
        participant_pay = list(participant.vars.values())
        Payments = []
        Payments1 = participant_pay[0]
        Payments2 = participant_pay[1]
        Payments3 = participant_pay[2]
        # Payments4 = participant_pay[3]

        Payments = [Payments1] + [Payments2] + [Payments3]
        risk_pay = Payments[2]
        Previous_earnings = Payments[0]
        amount_owned = Payments[Player.round_selected]  ###Times exchange rate if applicable
        rr = risk_pay[1]
        lottery_flip = risk_pay[2]
        Part1 = Previous_earnings[31]
        Puzzle1 = round(Previous_earnings[32], 2)
        Part1_game_selected = Previous_earnings[33]
        r1c2 = amount_owned[0]
        r2c2 = amount_owned[2]
        r2c3 = amount_owned[4]
        r2c4 = amount_owned[6]
        r3c2 = amount_owned[8]
        r3c3 = amount_owned[10]
        r3c4 = amount_owned[12]
        r4c2 = amount_owned[14]
        r4c3 = amount_owned[16]
        r4c4 = amount_owned[18]
        r5c2 = amount_owned[20]
        r5c3 = amount_owned[22]
        r5c4 = amount_owned[24]
        r6c2 = amount_owned[26]
        r6c3 = amount_owned[28]
        r6c4 = amount_owned[30]
        ppp = [r2c2] + [r3c2] + [r4c2] + [r5c2] + [r6c2] + [rr]
        Points_nrr = [r2c2] + [r3c2] + [r4c2] + [r5c2] + [r6c2]
        Points1 = sum(Points_nrr)
        Points = sum(ppp)
        points_total = sum(ppp + [Part1] + [Puzzle1])
        points_currency = round(sum(ppp + [Part1] + [Puzzle1]) * Constants.conversion_rate, 2)
        final_currency = round((sum(ppp + [Part1] + [Puzzle1]) * Constants.conversion_rate) + 7, 2)
        Player.totalpoints_currency = round(points_total, 2)
        Player.payoff = c(final_currency)
        return dict(total=final_currency, pointscurrency=points_currency, pointstotal=points_total, aa=Part1,
                    ab=Puzzle1, virtual_coin=lottery_flip, Part1_selected_game=Part1_game_selected,
                    a1=r1c2, a2=r2c2, a3=r2c3, a4=r2c4,
                    a5=r3c2, a6=r3c3, a7=r3c4,
                    a8=r4c2, a9=r4c3, a10=r4c4,
                    a11=r5c2, a12=r5c3, a13=r5c4,
                    a14=r6c2, a15=r6c3, a16=r6c4, rr_msg=rr, Points_earned=Points, points_from_2=Points1,
                    game_selected=Player.round_selected + 1, pay_me=amount_owned)


class Goodbye(Page):
    pass


page_sequence = [Questionnaire, ResultsWaitPage, Payments, Payments1, Goodbye]
