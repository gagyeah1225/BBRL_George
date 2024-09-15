import random
from otree.api import *

c = cu

doc = 'Show questionnaire (and collect payment details), report payoffs from previous apps.'


class Constants(BaseConstants):
    name_in_url = 'questionnaire_and_payment'
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


class Questionnaire(Page):
    pass

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
        #Payments3 = participant_pay[2]
        # Payments4 = participant_pay[3]

        Payments = [Payments1] + [Payments2]
        # risk_pay = Payments[3]
        amount_owned = Payments[Player.round_selected]  ###Times exchange rate if applicable
        # rr = risk_pay[1]
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
        ppp = [r2c2] + [r3c2] + [r4c2] + [r5c2] + [r6c2]
        # Points_nrr = [r2c2]+[r3c2]+[r4c2]+[r5c2]+[r6c2]
        Points = sum(ppp)
        Player.totalpoints_currency = round(Points)
        Player.payoff = c(Points * Constants.conversion_rate)
        return dict(a1=r1c2, a2=r2c2, a3=r2c3, a4=r2c4,
                    a5=r3c2, a6=r3c3, a7=r3c4,
                    a8=r4c2, a9=r4c3, a10=r4c4,
                    a11=r5c2, a12=r5c3, a13=r5c4,
                    a14=r6c2, a15=r6c3, a16=r6c4, Points_earned=Points,
                    game_selected=Player.round_selected + 1, pay_me=amount_owned)


class Goodbye(Page):
    pass


# page_sequence = [ResultsWaitPage, Payments]

page_sequence = [Questionnaire, ResultsWaitPage, Payments, Goodbye]
