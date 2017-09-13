#!/usr/bin/env python
#
# Copyright 2015 Airbus
# Copyright 2017 Fraunhofer Institute for Manufacturing Engineering and Automation (IPA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import rospy
import uuid
import os
from roslib.packages import get_pkg_dir
from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

from airbus_cobot_gui.account import Privilege, User
from airbus_cobot_gui.util import CobotGuiException, Parameters


from airbus_pyqt_extend.QtAgiCore import get_pkg_dir_from_prefix
from airbus_pyqt_extend.QtAgiGui import QAgiPopup

from airbus_cobot_gui.res import R


class DashboardPopup(QAgiPopup):
    
    def __init__(self,
                 parent,
                 popup_winpos=QAgiPopup.TopRight,
                 parent_winpos=QAgiPopup.BottomRight):
        
        QAgiPopup.__init__(self, parent)
        
        self.setRelativePosition(popup_winpos,
                                 parent_winpos)
        
        self._parent = parent
        
    def getParent(self):
        return self._parent
        
    def onCreate(self, param):
        pass
    
    def onTranslate(self, lng):
        pass
    
    def onDestroy(self):
        pass
    
    def closeEvent(self, event):
        self.onDestroy()

## @class WrapperDashboard
## @brief Base class for install base dashboard components.
class WrapperDashboard(QWidget):
    
    def __init__(self, context):
        QWidget.__init__(self)
        
        self._context = context
        self._name    = self.__class__.__name__
        
        self._param         = Parameters()
        self._popup_enabled = True
        self._access_rights = Privilege.OPERATOR
        
        self.setMinimumSize(QSize(35,35))
        self.setMaximumSize(QSize(600,35))
        
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(5)
        
        context.addUserEventListener(self.onUserChanged)
        context.addLanguageEventListner(self.onTranslate)
        context.addControlModeEventListener(self.onControlModeChanged)
        context.addEmergencyStopEventListner(self.onEmergencyStop)
        context.addCloseEventListner(self.onDestroy)
        
    def setup(self, dashboard_descriptor, param):
        
        xsetup = dashboard_descriptor.find('setup')
        
        if xsetup is not None:
            
            icon = xsetup.find('icon')
            
            if icon is not None:
                icon_path = get_pkg_dir_from_prefix(icon.text)
                if os.path.isfile(icon_path):
                    ico_label = QLabel(self)
                    ico_label.setPixmap(QPixmap(icon_path).scaled(60,60))
            
            access_rights = xsetup.find('access-rights')
            
            if access_rights is not None:
                self._access_rights = Privilege.TOLEVEL[access_rights.text]
            
        else:
            self.logErr("Cannot found '<setup>' into %s/dashboard_descriptor.xml"%self.getName())
            
        self._param = param
        self.onCreate(param)
    
    def getContext(self):
        return self._context
    
    def getLayout(self):
        return self._layout
    
    def getName(self):
        return self._name
    
    def getAccessRights(self):
        return self._access_rights
    
    def setPopupEnabled(self, state):
        self._popup_enabled = state
    
    def logInfo(self,):
        self._context.getLogger().info(msg)
        
    def logWarn(self, msg):
        self._context.getLogger().warn(msg)
        
    def logErr(self, msg):
        self._context.getLogger().err(msg)
    
    def onCreate(self, param):
        raise NotImplementedError("Need to surchage onCreate(self, param)")
    
    def onControlModeChanged(self, mode):
        raise NotImplementedError("Need to surchage onControlModeChanged(self, mode)")
        
    def onUserChanged(self, user_info):
        raise NotImplementedError("Need to surchage onUserChanged(self, user_info)")
    
    def onTranslate(self, lng):
        raise NotImplementedError("Need to surchage onTranslate(self, lng)")
    
    def onEmergencyStop(self, state):
        raise NotImplementedError("Need to surchage onEmergencyStop(self, state)")
    
    def onDestroy(self):
        raise NotImplementedError("Need to surchage onDestroy(self)")
        
    def onRequestPopup(self):
        return None
    
    def mousePressEvent(self, event):
        if self._popup_enabled is True:
            popup = self.onRequestPopup()
            if popup is not None:
                popup.onCreate(self._param)
                popup.onTranslate(self.getContext().getLanguage())
                popup.adjustSize()
                popup.show_()
    
    def closeEvent(self, event):
        self.onDestroy()

#End of file

