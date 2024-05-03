from raya.tools.fsm import BaseTransitions

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.constants import *
from src.static.fleet import FLEET_REQUEST_HELP
from .helpers import Helpers


class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def LOCALIZING(self):
        if await self.app.nav.is_localized():
            self.set_state('NAV_TO_CART')


    async def NAV_TO_CART(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('RECOGNIZING_CART')
            else:
                self.set_state('FAILED_FIRST_TRY_NAV_TO_CART')


    async def FAILED_FIRST_TRY_NAV_TO_CART(self):
        if not self.app.sound.is_playing(self.helpers.sound_clear_the_way):
            await self.helpers.play_clear_the_way_sound()
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('RECOGNIZING_CART')
            else:
                self.set_state('FAILED_SECOND_TRY_NAV_TO_CART')
                

    async def FAILED_SECOND_TRY_NAV_TO_CART(self):
        fleet_response = await self.app.fleet.request_action(
            **FLEET_REQUEST_HELP,
            timeout=-1,
        )
        
        self.log.info(f'Fleet response: {fleet_response}')
        # TODO: Check if the response is correct
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('RECOGNIZING_CART')
            else:
                self.set_state('FAILED_THIRD_TRY_NAV_TO_CART')

                
    async def FAILED_THIRD_TRY_NAV_TO_CART(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('RECOGNIZING_CART')
            else:
                self.set_state('FAILED_GOING_BACK_HOME')


    async def RECOGNIZING_CART(self):
        self.set_state('END')


    async def FIRST_TRY_RECOGNIZING_CART(self):
        pass

    async def SECOND_TRY_RECOGNIZING_CART(self):
        pass

    async def FAILED_GOING_BACK_HOME(self):
        pass
    