import argparse
import re
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


    def parse_location_list(self, arg):
        try:
            # Use regex to find all tuples in the format (float, float)
            tuple_regex = re.compile(r'\(([^)]+)\)')
            tuples = tuple_regex.findall(arg)
            # Convert the extracted tuples from strings to tuples of floats
            tuple_list = [tuple(map(float, item.split(','))) for item in tuples]
            return tuple_list
        except ValueError as e:
            raise argparse.ArgumentTypeError(f"Invalid format for locations: {arg}. Expected format: (float,float),(float,float),...")


    def parse_floor_list(self, arg):
        return [item.strip() for item in arg.split(',')]

    
    def get_arguments(self):
        self.locations = self.get_argument(
                '--locations',
                type=self.parse_location_list,
                help='Locations to deliver the packages, ex: --locations "\(1.0,2.0\),\(3.0,4.0\)"',
                required=True,
            )
        self.floor = self.get_argument(
                '--floor',
                type=self.parse_floor_list,
                help='Floors to deliver the packages, ex: --floor "floor1,floor2"',
                required=True,
            )
        
        self.log.info('App is running with there args:')
        self.log.info(f'Locations: {self.locations}')
        self.log.info(f'Floors: {self.floor}')
