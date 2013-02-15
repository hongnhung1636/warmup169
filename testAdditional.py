"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib


class TestAdditional(testLib.RestTestCase):
    #this class includes 10 test cases for unittest
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
        
    def TestEmptyUsername1(self):
        #check login with no username
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
       
    def testLongUsername2(self):
        #check login with too long username
        respData = self.makeRequest("/users/add", method="POST", data = { '1'*129 : '', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME) 
    
    def testUserNotExit3(self):
        #login with username that does not exit
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
    
    def testUserAlreadyExit4(self):
        #signup with user already exits
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 1,errCode = testLib.RestTestCase.SUCCESS)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : 'pass'} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_USER_EXISTS) 
    
    def testEmptyPass5(self):
        #check login with empty password
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : ''} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)
    
    def testLongPass6(self):
        #login with too long password   
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : '1'*129} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)
    
    def testWrongPass7(self):
        #login with wrong password
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 1,errCode = testLib.RestTestCase.SUCCESS) 
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user', 'password' : 'pass'} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testCheckCount8(self):
        #check for update count through many time of login
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 1,errCode = testLib.RestTestCase.SUCCESS)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 2,errCode = testLib.RestTestCase.SUCCESS)  
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 3,errCode = testLib.RestTestCase.SUCCESS)   

    def testReset9(self):
        #check for reset
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 1, errCode = testLib.RestTestCase.SUCCESS) 
        respData = self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.SUCCESS)        
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)  
        
    def testAddMoreLogin10(self):
        #check if the system allow to signup for more than 1 user
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : 'password'} )
        self.assertResponse(respData, count = 1,errCode = testLib.RestTestCase.SUCCESS) 
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'pass'} )
        self.assertResponse(respData, count = 1, errCode = testLib.RestTestCase.SUCCESS)

        

            
if __name__ == '__main__':
        unittest.main()
    
