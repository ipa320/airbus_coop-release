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
import inspect


def stdmsg(frame_desc=[], msg="Unknow"):
    
    if str(frame_desc[1]) == "<module>":
        frame_desc[1] = "__main__"
    
    msg = '[MSG]:%s [FILE]:%s [IN]:%s() [LINE]:%s'%(msg,
                                                   str(frame_desc[0]),
                                                   str(frame_desc[1]),
                                                   str(frame_desc[2]))
    return msg

## @package: exception
##
## @version 1.0
## @author  Matignon Martin
## @date    Last modified 30/04/2014

## @class CobotGuiException
## @brief Object for create an exception.
class CobotGuiException(Exception):
    
    def __init__(self, msg):
        self.msg = msg
        
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        filepyname = info.filename.split('/')
        
        rospy.logerr(stdmsg([filepyname[-1],info.function,info.lineno],msg))
        
    def __str__(self):
        return repr(self.msg)
    
if __name__ == "__main__":
    
    rospy.init_node('utt_airbus_cobot_gui_exception')
    
    try:
        x = 5/0
    except Exception as e:
        raise CobotGuiException(e)
    
