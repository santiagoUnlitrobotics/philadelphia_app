import cv2
import base64

from raya.tools.fsm import BaseActions
from raya.exceptions import RayaSoundErrorPlayingAudio

from src.app import RayaApplication
from src.static.navigation import NAV_WAREHOUSE_MAP_NAME, NAV_WAREHOUSE, NAV_CART_POINT
from src.static.ui import UI_SCREEN_FAILED, UI_SCREEN_LOCALIZING
from src.static.constants import *
from .helpers import Helpers


class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_SETUP_ACTIONS(self):
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        await self.app.nav.set_map(NAV_WAREHOUSE_MAP_NAME)


    async def enter_NAV_TO_WAREHOUSE(self):
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE,
                callback_feedback_async=self.helpers.nav_feedback_async,
            )
    
    
    async def enter_ATTACH_TO_CART_SKILL(self):
        await self.app.nav.navigate_to_position(
                **NAV_CART_POINT,
                callback_feedback_async=self.helpers.nav_feedback_async,
            )

    
    async def enter_NAV_TO_DELIVERY_POINT(self):
        delivery_point, _ = self.helpers.current_package
        delivery_location = {
            'x': delivery_point[0],
            'y': delivery_point[1],
            'angle': 90, 
        }
        await self.app.nav.navigate_to_position(
                **delivery_location,
                callback_feedback_async=self.helpers.nav_feedback_async,
            )


    async def enter_NAV_TO_WAREHOUSE_FLOOR_SKILL_RETURN(self):
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE,
                callback_feedback_async=self.helpers.nav_feedback_async,
            )


    async def aborted(self, error, msg):
        await self.app.ui.display_screen(
                **UI_SCREEN_FAILED,
                subtitle=f'ERROR {error}: {msg}'
            )
        await self.app.sound.play_sound(name='error')
