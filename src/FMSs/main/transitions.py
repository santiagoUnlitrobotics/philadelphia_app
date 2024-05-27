from raya.tools.fsm import BaseTransitions

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.constants import *
from src.static.fleet import *
from src.static.leds import *
from src.static.sound import *
from .helpers import Helpers
from .errors import *


class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers

    async def SETUP_ACTIONS(self):
        if await self.app.nav.is_localized():
            self.set_state('NAV_TO_WAREHOUSE_FLOOR_SKILL')
        else:
            self.abort(*ERR_COULD_NOT_LOCALIZE)


    async def NAV_TO_WAREHOUSE_FLOOR_SKILL(self):
        if await self.helpers.check_if_robot_in_warehouse_floor():
            self.set_state('NAV_TO_WAREHOUSE')

    
    async def NAV_TO_WAREHOUSE(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('ATTACH_TO_CART_SKILL')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_WAREHOUSE)


    async def ATTACH_TO_CART_SKILL(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NAV_TO_DELIVERY_FLOOR_SKILL')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_CART)


    async def NAV_TO_DELIVERY_FLOOR_SKILL(self):
        if await self.helpers.check_if_robot_in_delivery_floor():
            self.set_state('NAV_TO_DELIVERY_POINT')
            
    
    async def NAV_TO_DELIVERY_POINT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NOTIFY_ORDER_ARRIVED')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_DELIVERY_POINT)


    async def NOTIFY_ORDER_ARRIVED(self):
        self.set_state('WAIT_FOR_CHEST_CONFIRMATION')


    async def WAIT_FOR_CHEST_CONFIRMATION(self):
        sensors_data = self.app.sensors.get_all_sensors_values()
        button_chest = sensors_data['chest_button']
        if button_chest!=0:
            self.set_state('CONFIRMATION_ON_FLEET')

        if not self.sound.is_playing():
            await self.app.leds.animation(
                **LEDS_WAIT_FOR_BUTTON_CHEST_HEAD, 
                wait=False
            )
            await self.app.leds.animation(
                **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON,
                wait=False
            )
            await self.app.sound.play_sound(
                **SOUND_WAIT_FOR_CHEST_BUTTON,
                wait=False,
            )
        
    async def CONFIRMATION_ON_FLEET(self):
        if not self.sound.is_playing():
            await self.app.leds.animation(
                **LEDS_WAIT_FOR_FLEET_CONFIRMATION,
                wait=False
            )
            await self.app.sound.play_sound(
                **SOUND_WAIT_FOR_FLEET_CONFIRMATION,
                wait=False,
            )
        
        # response = await self.app.fleet.request_action(
        #     **FLEET_REQUEST_CONFIRMATION_PACKAGE
        # )
        # if response == 'ok':
        #     self.set_state('PACKAGE_DELIVERED')

        if not self.app.sound.is_playing():
            self.set_state('PACKAGE_DELIVERED')

        
    async def PACKAGE_DELIVERED(self):
        await self.app.leds.animation(
            **LEDS_PACKAGE_DELIVERED,
                wait=False
            )
        await self.app.sound.play_sound(
            **SOUND_PACKAGE_DELIVERED,
            wait=True,
        )
        self.set_state('CHECK_IF_MORE_PACKAGES')

    
    async def CHECK_IF_MORE_PACKAGES(self):
        if self.helpers.check_if_more_packages():
            self.helpers.set_next_package()
            self.set_state('NAV_TO_DELIVERY_FLOOR_SKILL')
        else:
            self.set_state('NAV_TO_WAREHOUSE_FLOOR_SKILL_RETURN')


    async def NAV_TO_WAREHOUSE_FLOOR_SKILL_RETURN(self):
        if await self.helpers.check_if_robot_in_warehouse_floor():
            self.set_state('NAV_TO_WAREHOUSE_RETURN')
        else:
            self.set_state('REQUEST_FOR_HELP')

    
    async def NAV_TO_WAREHOUSE_RETURN(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('DE_ATTACH_CART_SKILL')
            else:
                self.set_state('REQUEST_FOR_HELP')
    
    
    async def REQUEST_FOR_HELP(self):
        self.set_state('RELEASE_CART')


    async def RELEASE_CART(self):
        self.abort(*ERR_NAV_RETURN_WAREHOUSE_FAILED)


    async def DE_ATTACH_CART_SKILL(self):
        self.set_state('NOTIFY_ALL_PACKAGES_STATUS')


    async def NOTIFY_ALL_PACKAGES_STATUS(self):
        self.set_state('END')


    async def PACKAGE_NOT_CONFIRMED(self):
        self.set_state('CHECK_IF_MORE_PACKAGES')


    async def MAX_RETRIES_ON_NOTIFICATION(self):
        await self.app.sleep(5)
        self.set_state('PACKAGE_NOT_DELIVERED')


    async def PACKAGE_NOT_DELIVERED(self):
        await self.app.sleep(5)
        self.set_state('CHECK_IF_MORE_PACKAGES')
