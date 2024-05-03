from src.static.app_errors import *


# The first state is always the initial one
STATES = [
        'LOCALIZING',
        'NAV_TO_CART',
        
        'FAILED_FIRST_TRY_NAV_TO_CART',
        'FAILED_SECOND_TRY_NAV_TO_CART',
        'FAILED_THIRD_TRY_NAV_TO_CART',
        
        'RECOGNIZING_CART',
        'FIRST_TRY_RECOGNIZING_CART',
        'SECOND_TRY_RECOGNIZING_CART',

        'FAILED_GOING_BACK_HOME',
        'END',
    ]


# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'LOCALIZING'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]


# If one of the states takes more than an especified time, it aborts.
# Format: 'STATE': (<timeout>, <error_tuple>)
STATES_TIMEOUTS = {
    'LOCALIZING' : (10.0, APPERR_COULD_NOT_LOCALIZE),
}
