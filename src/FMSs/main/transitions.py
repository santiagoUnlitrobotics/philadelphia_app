from raya.tools.fsm import BaseTransitions

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.constants import *
from .helpers import Helpers
from .errors import *


class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers

    async def SETUP_ACTIONS(self):
        if await self.app.nav.is_localized():
            self.set_state('NAV_TO_CART')
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
                self.set_state('ATTACH_TO_CART_SKILL')
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
        self.set_state('CONFIRMATION_ON_FLEET')

        
    async def CONFIRMATION_ON_FLEET(self):
        self.set_state('PACKAGE_DELIVERED')

        
    async def PACKAGE_DELIVERED(self):
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
        