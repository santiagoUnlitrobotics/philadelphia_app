from raya.exceptions import *
from raya.tools.fsm import FSM

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.navigation import NAV_WAREHOUSE_MAP_NAME


class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app
        self.index_package = 0
        self.current_package = (
            self.app.locations[self.index_package], 
            self.app.floor[self.index_package]
        )

    async def check_if_robot_in_warehouse_floor(self):
        is_localized,_,_,map_name = await self.app.nav.get_status()
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
        
        if code == 9: # Waiting for obstacle to move
            await self.app.sound.play_sound(name='error')
