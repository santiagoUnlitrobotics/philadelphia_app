from raya.exceptions import *
from raya.tools.fsm import FSM

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.sound import SOUND_CLEAR_THE_WAY


class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app
        self.sound_clear_the_way_buffer_id = None


    def ui_result_callback(self, data):
        self.last_ui_result = data


    async def nav_feedback_async(self, code, msg, distance_to_goal, speed):
        self.app.log.debug(
            f'nav_feedback_async: {code}, {msg}, {distance_to_goal}, {speed}'
        )
        
        if code == 9: # Waiting for obstacle to move
            await self.app.sound.play_sound(name='error')


    async def play_clear_the_way_sound(self):
        self.sound_clear_the_way_buffer_id = await self.app.sound.play_sound(
            **SOUND_CLEAR_THE_WAY, 
            wait=False
        )


    async def stop_clear_the_way_sound(self): 
        try:
            await self.app.sound.cancel_sound(
                buffer_id=self.sound_clear_the_way_buffer_id
            )
        except RayaSoundErrorPlayingAudio:
            pass


    async def sound_feedback_async(self, code, msg):
        self.app.log.debug(f'sound_feedback_async: {code}, {msg}')
        