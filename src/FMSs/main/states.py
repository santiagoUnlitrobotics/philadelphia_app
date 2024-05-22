from src.static.app_errors import *


# The first state is always the initial one
STATES = [
        'SETUP_ACTIONS',
        'NAV_TO_WAREHOUSE_FLOOR_SKILL',
        'NAV_TO_WAREHOUSE',
        'ATTACH_TO_CART_SKILL',
        'NAV_TO_DELIVERY_FLOOR_SKILL',
        'NAV_TO_DELIVERY_POINT',
        'NOTIFY_ORDER_ARRIVED',
        'WAIT_FOR_CHEST_CONFIRMATION',
        'CONFIRMATION_ON_FLEET',
        'PACKAGE_DELIVERED',
        'PACKAGE_DELIVERED_TO_UNKOWN',
        'MAX_RETRIES_ON_NOTIFICATION',
        'PACKAGE_NOT_DELIVERED',
        
        'CHECK_IF_MORE_PACKAGES',
        'NAV_TO_WAREHOUSE_FLOOR_SKILL_RETURN',
        'NAV_TO_WAREHOUSE_RETURN',
        'REQUEST_FOR_HELP',
        'RELEASE_CART',
        'DE_ATTACH_CART_SKILL',
        'NOTIFY_ALL_PACKAGES_STATUS',
        'END',
    ]


# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'SETUP_ACTIONS'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]


# If one of the states takes more than an especified time, it aborts.
# Format: 'STATE': (<timeout>, <error_tuple>)
# STATES_TIMEOUTS = {
#     'LOCALIZING' : (10.0, APPERR_COULD_NOT_LOCALIZE),
# }
