import json

class Device(object):

    LUT = []
    
    @staticmethod
    def load_devices(fname):
        file = open(fname, "r") 
        Device.LUT = json.load(file)
        file.close()

    @staticmethod
    def get_device(x):
        return Device.LUT[x]
    
    @staticmethod
    def get_devices():
        return Device.LUT

class User(object):
    
    LUT = []
    
    @staticmethod
    def load_users(fname):
        file = open(fname, "r") 
        User.LUT = json.load(file)
        file.close()

    @staticmethod
    def get_user(x):
        return User.LUT[x]

    @staticmethod
    def get_users():
        return User.LUT