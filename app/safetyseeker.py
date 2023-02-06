from kivy.app import App
from os import path, makedirs
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp, ThemeManager
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.uix.behaviors import ToggleButtonBehavior
import time

from kivy.utils import QueryDict, rgba
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock


from kivy.core.window import Window

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/Users/junjiecai/Desktop/aisingapore/api')

from api import db

from .process import process

Builder.load_file('views/adminpage.kv')
Builder.load_file('views/mainpage.kv')
Builder.load_file('views/scanpage.kv')
Builder.load_file('views/dashboard.kv')

BUTTON_SIZE = 20
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
BACKGROUND =  "#D3D3D3"

class ScanPage(Screen):
    """
    This class provides the ScanPage for the workers to scan their outfit and check in.
    """
    def __init__(self, **kwargs):
        super(ScanPage, self).__init__(**kwargs)
        self._folder = './.tmp'
        self._res = False
    
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d")
        target = self._folder + '/' + timestr
        if not path.isdir(target):
            makedirs(target)
        file_location = (target + "/{}.png").format(self.ids['nric'].text)
        camera.export_to_png(file_location)
        self._res = process(file_location, self.manager._db.get_id(self.ids['nric'].text), target)
        self.manager._db.add_checkin(timestr, self.ids['nric'].text, self._res)
        if self._res:
            self.manager.current = 'main'
        else:
            self.show_pop_up()
    
    def show_pop_up(self):
        alert = Popup(title='Test popup',
            content=Button(text='PPE not located!\nPlease try again.'),
            size_hint=(None, None), size=(400, 400))
        alert.open()
        Clock.schedule_interval(lambda x: alert.dismiss(), 2)

class DashboardPage(Screen):
    """
    This class provides the dashboard page for the managers to monitor the workers and check in.
    """
    def __init__(self, **kwargs):
        super(DashboardPage, self).__init__(**kwargs)

    def fill_workers(self):
        for person in self.manager._all_workers:
            img_path = '.tmp/{}/{}.png'.format(self.manager._date, person[1])
            timestr = time.strftime("%Y%m%d")
            if self.manager._db.is_user_checked_in(timestr, person[1]):
                print('checked in')
                self.ids.worker_grid.add_widget(WorkerView(source=img_path,name=person[0], occupation=person[2], colour="green"))
            elif path.exists(img_path):
                self.ids.worker_grid.add_widget(WorkerView(source=img_path,name=person[0], occupation=person[2], colour="red"))
            else:
                self.ids.worker_grid.add_widget(WorkerView(source='{}'.format("/Users/junjiecai/Desktop/aisingapore/assets/imgs/mia.jpeg") ,name=person[0], occupation=person[2], colour="red"))

    def fill_name(self):
        self.ids.message_bar.text = "Welcome {}".format(self.manager._admin[0])
    
    def on_enter(self, *args):
        """
        This function is called when the user enters the dashboard page.
        """
        print(self.ids)
        print("entered dashboard")
        self.fill_workers()
        self.fill_name()
        return super().on_enter(*args)


class AdminPage(Screen):
    """
    This class provides the interface for the manager to login into their account.
    """
    def __init__(self, **kwargs):
        super(AdminPage, self).__init__(**kwargs)

    def logger(self):
        self.ids.welcome_label.text = f'Sup {self.ids.user.text}!'
        password = self.ids.password.text
        username = self.ids.user.text
        id = self.manager._db.authenticate_admin(username, password)
        if id != '-1':
            self.manager._id = id
            self.manager._admin = self.manager._db.get_info(id)
            self.manager.current = "dashboard"
            self.manager._date = time.strftime("%Y%m%d")
            self.manager._all_workers = self.manager._db.get_all_workers(id)
        else:
            print("Fail to login")

    def clear(self):
        self.ids.welcome_label.text = "WELCOME"		
        self.ids.user.text = ""		
        self.ids.password.text = ""


class MainPage(Screen):
    """
    This class provides the starting page for the users.
    """
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)

class SafetySeekerApp(MDApp):
    # Creating the standard colours for the application
    colors = QueryDict()
    colors.primary = rgba("#2D9CDB")
    colors.secondary = rgba("#16213E")
    colors.success = rgba("#1FC98E")
    colors.warning = rgba("#F2C94C")
    colors.danger = rgba("#EB5757")
    colors.grey_dark = rgba("#c4c4c4")
    colors.grey_light = rgba("#f5f5f5")
    colors.black = rgba("#a1a1a1")
    colors.white = rgba("#ffffff")

    # Creating the standard font size for the application
    fonts = QueryDict()
    fonts.size = QueryDict()
    fonts.size.h1 = dp(24)
    fonts.size.h2 = dp(22)
    fonts.size.h3 = dp(18)
    fonts.size.h4 = dp(16)
    fonts.size.h5 = dp(14)
    fonts.size.h6 = dp(12)

    def build(self):
        theme_cls = ThemeManager()
        theme_cls.primary_palette = "Teal"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(AdminPage(name='admin'))
        sm.add_widget(ScanPage(name='scan'))
        sm.add_widget(DashboardPage(name='dashboard'))
        sm._db = db.Database('api/safetyseeker.db')
        sm._id = 0
        sm._all_workers = []
        return sm

class NavTab(ToggleButtonBehavior, BoxLayout):
    """
    Creating the standard tab format for the navigation view.
    """
    text = StringProperty("")
    icon = StringProperty("")
    icon_active = StringProperty("")
    def __init__(self, **kw):
        super(NavTab, self).__init__(**kw)

class WorkerView(BoxLayout):
    """
    Creating the standard worker display for the manager.
    """
    source = StringProperty("")
    name = StringProperty("")
    occupation = StringProperty("")
    colour = StringProperty("")
    def __init__(self, **kw):
        super(WorkerView, self).__init__(**kw)