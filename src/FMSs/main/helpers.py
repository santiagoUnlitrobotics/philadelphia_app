from raya.exceptions import *
from raya.tools.fsm import FSM

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.navigation import *
from src.static.leds import *
from src.static.sound import *


class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app
        self.index_package = 0
        self.current_package = (
            self.app.locations[self.index_package], 
            self.app.floor[self.index_package]
        )

    async def check_if_robot_in_warehouse_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        if is_localized and map_name == NAV_WAREHOUSE_MAP_NAME:
            return True
        return False


    async def check_if_robot_in_delivery_floor(self):
        is_localized,_,_,map_name = await self.app.nav.get_status()
        if is_localized and map_name == self.current_package[1]:
            return True
        return False


    async def check_if_more_packages(self):
        return self.index_package < len(self.app.locations) - 1


    async def set_next_package(self):
        self.index_package += 1
        self.current_package = (
            self.app.locations[self.index_package], 
            self.app.floor[self.index_package]
        )


    async def nav_feedback_async(self, code, msg, distance_to_goal, speed):
        self.app.log.debug(
            f'nav_feedback_async: {code}, {msg}, {distance_to_goal}, {speed}'
        )
        # if code == 9:
        #     await self.app.sound.play_sound(
        #         name='error'
        #     )
        
    async def nav_finish_async(self, code, msg):
        self.app.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )


    async def task_approaching_to_cart_audio(self):
        while True:
            await self.app.leds.animation(**LEDS_ATTACHING_TO_CART)
            await self.app.sound.play_sound(
                **SOUND_ATTACHING_TO_CART,
                wait=True,
            )
            await self.app.sleep(2)

