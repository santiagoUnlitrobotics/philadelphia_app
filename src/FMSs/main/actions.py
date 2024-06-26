from raya.tools.fsm import BaseActions

from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *
from src.static.constants import *
from src.static.fleet import *
from src.static.leds import *
from src.static.sound import *
from .helpers import Helpers
from raya.enumerations import POSITION_UNIT, ANGLE_UNIT


class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_SETUP_ACTIONS(self):
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        await self.app.nav.set_map(NAV_WAREHOUSE_MAP_NAME)


    async def enter_NAV_TO_WAREHOUSE_FLOOR_SKILL(self):
        floor = self.helpers.current_package[1]
        UI_SCREEN_NAV_TO_WAREHOUSE_FLOOR['subtitle'] = \
            f'Navigating to warehouse floor {floor}' 
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE_FLOOR)


    async def enter_NAV_TO_WAREHOUSE(self):
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )
    
    
    async def enter_ATTACH_TO_CART_SKILL(self):
        await self.app.ui.display_screen(**UI_SCREEN_ATTACHING_TO_CART)
        self.app.create_task(
            name='task_approaching_to_cart_audio', 
            afunc=self.helpers.task_approaching_to_cart_audio
        )
        await self.app.nav.navigate_to_position(
                **NAV_CART_POINT,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )
    
    async def exit_ATTACH_TO_CART_SKILL(self):
        self.app.cancel_task('task_approaching_to_cart_audio')
        self.app.sound.cancel_all_sounds()
        self.app.leds.turn_off_all()


    async def enter_NAV_TO_DELIVERY_FLOOR_SKILL(self):
        floor = self.helpers.current_package[1]
        UI_SCREEN_NAV_TO_PACKAGE_FLOOR['subtitle'] = \
            f'Delivering package on the floor: {floor}' 
        
        package , floor = self.helpers.current_package
        point = {
            'x': package[0],
            'y': package[1],
            'angle': package[2],
            'pos_unit': POSITION_UNIT.PIXELS, 
            'ang_unit': ANGLE_UNIT.DEGREES,
        }
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_PACKAGE_FLOOR)
        await self.app.nav.navigate_to_position(
                **point,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def enter_NOTIFY_ORDER_ARRIVED(self):
        await self.app.leds.animation(
            **LEDS_NOTIFY_ORDER_ARRIVED, 
            wait=False
        )
        await self.app.sound.play_sound(
            **SOUND_NOTIFY_ORDER_ARRIVED,
            wait=True,
        )
        self.app.leds.turn_off_all()


    async def enter_WAIT_FOR_CHEST_CONFIRMATION(self):
        await self.app.ui.display_screen(**UI_SCREEN_DELIVERING_ARRIVE)


    async def exit_WAIT_FOR_CHEST_CONFIRMATION(self):
        self.app.sound.cancel_all_sounds()
        self.app.leds.turn_off_all()


    async def enter_CONFIRMATION_ON_FLEET(self):
        await self.app.ui.display_screen(
            **UI_SCREEN_DELIVERING_CONFIRMATION_ON_FLEET
        )

  
    async def exit_CONFIRMATION_ON_FLEET(self):
        self.app.sound.cancel_all_sounds()
        self.app.leds.turn_off_all()

    
    async def enter_PACKAGE_DELIVERED(self):
        await self.app.ui.display_screen(
            **UI_SCREEN_DELIVERING_CONFIRMATION_ON_FLEET
        )    


    async def enter_NAV_TO_DELIVERY_POINT(self):
        UI_SCREEN_DELIVERING_PACKAGE['subtitle'] = \
            f'Delivering package {self.helpers.index_package + 1} \
                of {len(self.app.locations)}'

        await self.app.ui.display_screen(**UI_SCREEN_DELIVERING_PACKAGE)
        delivery_point, _ = self.helpers.current_package
        delivery_location = {
            'x': delivery_point[0],
            'y': delivery_point[1],
            'angle': 90, 
        }
        await self.app.nav.navigate_to_position(
                **delivery_location,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def enter_NAV_TO_WAREHOUSE_FLOOR_SKILL_RETURN(self):
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE_RETURN)
        await self.app.leds.animation(
            **LEDS_ALL_PACKAGES_DELIVERED,
            wait=False
        )
        await self.app.sound.play_sound(
            **SOUND_ALL_PACKAGES_DELIVERED,
            wait=True,
        )
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )

    async def enter_DE_ATTACH_CART_SKILL(self):
        await self.app.ui.display_screen(**UI_SCREEN_DEATTACHING_TO_CART)


    async def enter_NOTIFY_ALL_PACKAGES_STATUS(self):
        await self.app.ui.display_screen(**UI_SCREEN_DELIVERING_SUCESS)
        await self.app.sound.play_sound(name='success', wait=True)


    async def enter_REQUEST_FOR_HELP(self):
        await self.app.ui.display_screen(**UI_SCREEN_FAILED)
        await self.app.sound.play_sound(name='error')


    async def enter_RELEASE_CART(self):
        await self.app.ui.display_screen(**UI_SCREEN_RELEASE_CART)
        

    async def aborted(self, error, msg):
        await self.app.ui.display_screen(
                subtitle=f'ERROR {error}: {msg}',
                **UI_SCREEN_FAILED
            )
        await self.app.sound.play_sound(name='error')


    async def enter_MAX_RETRIES_ON_NOTIFICATION(self):
        await self.app.ui.display_screen(**UI_TRIES_ON_NOTIFICATION)


    async def enter_PACKAGE_NOT_DELIVERED(self):
        await self.app.ui.display_screen(**UI_PACKAGE_NOT_DELIVERED)


    async def enter_PACKAGE_NOT_CONFIRMED(self):
        await self.app.ui.display_screen(**UI_PACKAGE_NOT_CONFIRMED)
