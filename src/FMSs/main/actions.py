import cv2
import base64

from raya.tools.fsm import BaseActions
from raya.exceptions import RayaSoundErrorPlayingAudio

from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *
from src.static.constants import *
from .helpers import Helpers


class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_LOCALIZING(self):
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        await self.app.nav.set_map(NAV_MAP_NAME)


    async def LOCALIZING_to_NAV_TO_CART(self):
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_CART_LOCATION)


    async def enter_NAV_TO_CART(self):
        await self.app.nav.navigate_to_position(
                **NAV_CART_LOCATION,
                wait=False,
                callback_feedback_async=self.helpers.nav_feedback_async,
            )


    async def enter_FAILED_FIRST_TRY_NAV_TO_CART(self):
        if self.helpers.sound_clear_the_way is None:
            await self.helpers.play_clear_the_way_sound()

    
    async def enter_RECOGNIZING_CART(self):
        await self.helpers.stop_clear_the_way_sound()


    # async def aborted(self, error, msg):
    #     await self.app.ui.display_screen(
    #             **UI_SCREEN_FAILED,
    #             subtitle=f'ERROR {error}: {msg}'
    #         )
    #     await self.app.sound.play_sound(name='error')
