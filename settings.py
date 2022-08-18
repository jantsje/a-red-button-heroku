from os import environ


SESSION_CONFIGS = [
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
	# dict(
	# 	name='button',
	# 	display_name="The Button (Control)",
	# 	num_demo_participants=10,
	# 	treatment="Baseline",
	# 	app_sequence=['dana', 'wait', 'the_button'],
	# 	cc_code="CCCODE"),
	# dict(
	# 	name='button_request',
	# 	display_name="The Button (Request)",
	# 	num_demo_participants=10,
	# 	treatment="Request",
	# 	app_sequence=['dana', 'wait', 'the_button'],
	# 	cc_code="CCCODE"),
	# dict(
	# 	name='button_request3',
	# 	display_name="The Button (Request+ Punishment)",
	# 	num_demo_participants=10,
	# 	treatment="Request + Punishment",
	# 	app_sequence=['dana', 'wait', 'the_button'],
	# 	cc_code="CCCODE"),
]
DEBUG = False


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '{{ secret_key }}'

INSTALLED_APPS = ['otree']
