from raya.application_base import RayaApplicationBase
from raya.application_base import RayaApplicationBase
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.leds_controller import LedsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController

from src.FMSs.main import MainFSM

class RayaApplication(RayaApplicationBase):

    async def setup(self):
        # Controllers
        self.nav:NavigationController = \
                await self.enable_controller('navigation')
        self.leds:LedsController  = \
                await self.enable_controller('leds')
        self.sound:SoundController = \
                await self.enable_controller('sound')
        self.ui:UIController = \
                await self.enable_controller('ui')
        self.fleet:FleetController = \
                await self.enable_controller('fleet')
        
        # FSMs
        self.fsm_main_task = MainFSM(
                log_transitions=True,
            )


    async def loop(self):
        await self.fsm_main_task.run_in_background()
        
        while self.fsm_main_task.is_running():
            await self.sleep(0.5)

        self.finish_app()


    async def finish(self):
        if self.fsm_main_task.was_successful():
            self.log.info('App correctly finished')
        else:
            # fsm_error[0]: error code, fsm_error[1]: error message
            fsm_error_code, fsm_error_msg = self.fsm_main_task.get_error()
            self.log.error(
                f'App finished with error [{fsm_error_code}]: {fsm_error_msg}'
            )

    # def get_arguments(self):
    #     self.target_location_name = self.get_argument(
    #             '--location',
    #             type=int,
    #             help='Number of the unit to send',
    #             required=True,
    #         )
    #     self.target_location_coordinates = self.get_argument(
    #             '--location',
    #             type=int,
    #             help='Number of the unit to send',
    #             required=True,
    #         )
