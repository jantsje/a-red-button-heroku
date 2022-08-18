from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01,
    participation_fee=0.00,
    doc=""
)

SESSION_CONFIGS = [

    # dict(
    #     name='classroom_aia',
    #     display_name="Classroom all-in-auction",
    #     num_demo_participants=3,
    #     app_sequence=['classroom_aia'],
    #     timeout_seconds=15,
    #     endowments=[0, 1, 2, 3, 4],
    #     land=[[6, 4, 3, 2, 1], [8, 5, 3, 2], [10, 9, 7]],
    #     num_sessions=4,
    #     rounds_per_session=6,
    #     players_per_group=30,
    #     doc="""Make sure to set players_per_group equal to the number of participants."""
    # ),
    dict(
        name='dana',
        display_name="Dana only",
        num_demo_participants=1,
        app_sequence=['dana']),
    dict(
        name='button_only1',
        display_name="Button only Baseline",
        treatment="Baseline",
        num_demo_participants=2,
        app_sequence=['the_button'],
        cc_code="CCCODE"),
    dict(
        name='button_only2',
        display_name="Button only Request",
        treatment="Request",
        num_demo_participants=2,
        app_sequence=['the_button'],
        cc_code="CCCODE"),
    dict(
        name='button_only3',
        display_name="Button only Request + Punishment",
        treatment="Request + Punishment",
        num_demo_participants=2,
        app_sequence=['the_button'],
        cc_code="CCCODE"),
    dict(
        name='button',
        display_name="The Button (Control)",
        num_demo_participants=10,
        treatment="Baseline",
        app_sequence=['dana', 'wait', 'the_button'],
        cc_code="CCCODE"),
    dict(
        name='button_request',
        display_name="The Button (Request)",
        num_demo_participants=10,
        treatment="Request",
        app_sequence=['dana', 'wait', 'the_button'],
        cc_code="CCCODE"),
    dict(
        name='button_request3',
        display_name="The Button (Request+ Punishment)",
        num_demo_participants=10,
        treatment="Request + Punishment",
        app_sequence=['dana', 'wait', 'the_button'],
        cc_code="CCCODE"),

]
# see the end of this file for the inactive session configs

ROOMS = [
    dict(
        name='lenka_full',
        display_name='Lenka Full Info',
        participant_label_file='_rooms/lenka_full_info.txt',
    ),
    dict(
        name='lenka_partial',
        display_name='Lenka Partial Info',
        participant_label_file='_rooms/lenka_partial_info.txt',
    ),
    dict(
        name='lenka_no',
        display_name='Lenka No Info',
        participant_label_file='_rooms/lenka_no_info.txt',
    ),
    dict(
        name='sulagna_full',
        display_name='Sulagna Full Info',
        participant_label_file='_rooms/sulagna_full_info.txt',
    ),
    dict(
        name='sulagna_partial',
        display_name='Sulagna Partial Info',
        participant_label_file='_rooms/sulagna_partial_info.txt',
    ),
    dict(
        name='sulagna_no',
        display_name='Sulagna No Info',
        participant_label_file='_rooms/sulagna_no_info.txt',
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'
LANGUAGE_SESSION_KEY = '_language'  # we need this to deal with the issue of the very last page
# That is shown to users when they click 'Next' at the VERY last page

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0
USE_POINTS = True
USE_THOUSAND_SEPARATOR = True
POINTS_CUSTOM_NAME = 'points'


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
OTREE_AUTH_LEVEL = 'DEMO'

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games. I tried to get the otree auth level to demo.
"""

# don't share this with anybody.
SECRET_KEY = '{{ secret_key }}'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'otreeutils']

OTREE_REST_KEY = "7021uksf_jantsje"
