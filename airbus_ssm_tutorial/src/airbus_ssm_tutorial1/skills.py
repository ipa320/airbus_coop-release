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
from airbus_ssm_core import ssm_state
        
class Input(ssm_state.ssmState):
    '''@SSM
    Description :  Get a keyboard input and return an outcome accordingly.
    User-data : 
    - input : the keyboard input if it's an interger.
    Outcome :
    - Test  : if the input is an integer
    - Out   : if the input is 'q'
    - Retry : if the input is not an integer or 'q'
    '''
	
    def __init__(self):
        ssm_state.ssmState.__init__(self,outcomes=["Test","Out","Retry"], 
                                    io_keys=["input"])
        
        
    def execution(self, ud):
        print("Prime Tester ('q' to print all prime number found) :")
        input = raw_input()
        if(input == 'q'):
            return 'Out'
        else:
            try:
                ud.input = int(input)
                return "Test"
            except:
                print("[Error] Couldn't convert "+str(input) +" into an int !")
                return "Retry"
                
class isPrime(ssm_state.ssmState):
    '''@SSM
    Description : Test if the input number is prime and add it a the prime_list if it is
    User-data : 
    - input : the tested number
    - prime_list : the list of all the prime number_found
    Outcome :
    - Return  : atfer the test even if the input number is not prime
    '''
    def __init__(self):
        ssm_state.ssmState.__init__(self,outcomes=["Return"], 
                                    io_keys=["input","prime_list"])
    def is_prime(self, a):
        return all(a % i for i in xrange(2, a))
    
    def execution(self, ud):
        ## Test if it's prime_list is not initialised
        if ud.prime_list is None:
            ud.prime_list = []
        
        if(self.is_prime(ud.input)):
            print(str(ud.input) + " is a prime number.")
            ud.prime_list.append(ud.input)
        else:
            print(str(ud.input) + " is not a prime number.")
            
        return "Return"
            
            
class Primes(ssm_state.ssmState):
    '''@SSM
    Description : Print the list of all the prime numbers found and give a list of possible actions
    User-data : 
    - prime_list : the list of all the prime number found
    Outcome :
    - Continue  : if the input is 'c'
    - Reset     : if the input is 'r'
    - Off       : if the input is 'q'
    '''
    def __init__(self):
        ssm_state.ssmState.__init__(self,outcomes=["Reset","Off", "Continue"], 
                                    io_keys=["prime_list"])
        
    
    def execution(self, ud):
        ## Test if it's prime_list is not initialised
        if ud.prime_list is None:
            ud.prime_list = []
            print("Prime list is empty.")
        else:
            print("Prime list :")
            for i_prime in ud.prime_list:
                print(str(i_prime))
        while(1):
            print("'c' to continue")
            print("'r' to reset")
            print("'q' to quit\n")
            input = raw_input("input : ")
            if(input == 'c'):
                return "Continue"
            elif(input == 'r'):
                ud.prime_list = []
                return 'Reset'
            elif(input == 'q'):
                return 'Off'
            else:
                print("Input not recognize")
    
        
