from os import environ

SESSION_CONFIGS = [

    # dict(
    #     name='Payment_alternative4',
    #     display_name="Trial",
    #     num_demo_participants=4,
    #     app_sequence=['Payment_alternative4'],
    # ),
    # dict(
    #     name='game21',
    #     display_name="Game 21",
    #     num_demo_participants=1,
    #     app_sequence=['game21'],
    # ),
    # dict(
    #     name='game24',
    #     display_name="Game 24",
    #     num_demo_participants=4,
    #     app_sequence=['game24'],
    # ),
    # dict(
    #     name='game1',
    #     display_name="Game 1",
    #     num_demo_participants=3,
    #     app_sequence=['game1'],
    # ),
    # #
    # dict(
    #     name='game11',
    #     display_name="Game 11",
    #     num_demo_participants=1,
    #     app_sequence=['game11'],
    # ),
    #
    # dict(
    #     name='game14',
    #     display_name="Game 14",
    #     num_demo_participants=4,
    #     app_sequence=['game14'],
    # ),
    # dict(
    #     name='Game3',
    #     display_name="Game 3",
    #     num_demo_participants=3,
    #     app_sequence=['game3'],
    # ),
    # dict(
    #     name='Game31',
    #     display_name="Game 31",
    #     num_demo_participants=2,
    #     app_sequence=['game31'],
    # ),
    # dict(
    #     name='Game34',
    #     display_name="Game 34",
    #     num_demo_participants=4,
    #     app_sequence=['game34'],
    # ),
    # dict(
    #     name='Payment_alternative1',
    #     display_name="Payment_alternative",
    #     num_demo_participants=3,
    #     app_sequence=['Payment_alternative'],
    # ),
    dict(
        name='Part_I',
        display_name="Part_I",
        num_demo_participants=3,
        app_sequence=['game2', 'game3', 'Payment_alternative'],
    ),
    dict(
        name='Part_II',
        display_name="Part_II",
        num_demo_participants=4,
        app_sequence=['game24', 'game34', 'EG', 'Payment_alternative4'],
    ),
    dict(
        name='1_person',
        display_name="1_person",
        num_demo_participants=1,
        app_sequence=['game21', 'game31', 'Payment_alternative1'],
    ),
    #
    # dict(
    #     name='Eckel',
    #     display_name="EG",
    #     num_demo_participants=4,
    #     app_sequence=['EG'],
    # ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config
# Add payment to app sequence
# Plan is to run individual and then put them together in one app sequence

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=7.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='part1',
        display_name='Group behavior 1',
        participant_label_file='_rooms/part1.txt',
        #use_secure_urls=True
    ),
    dict(
        name='part2',
        display_name='Group behavior 2',
        participant_label_file='_rooms/part2.txt',
        #use_secure_urls=True  # This allows you to send secured urls to participants to avoid link issues. However,
        # you cannot require label before beginning.
    ),
    dict(
        name='new',
        display_name='New Person',
        participant_label_file='_rooms/new.txt',
    #    use_secure_urls=True
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Experiment 1
"""

SECRET_KEY = 'v+%k^o8voashbiktc#!vh*%lne@6a3cbz%69e-a7k#%)9$ub5-'

INSTALLED_APPS = ['otree']
