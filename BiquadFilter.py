import numpy as np
import warnings

"""
reference : https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html
author : Robert Bristow-Johnson
editors : Raymond Toy, Doug Schepers (previously W3C)
copyright : CC BY 4.0

library reconstruction : Jinyong Kim
email : jy9886.kim@samsung.com / jdragon0@naver.com
"""

class BiquadEQ:
    def __init__(self,fs,fc,gain,Q,filterType,globalGain):
        self.fs = fs
        self.fc = fc
        self.gain = gain
        self.Q = Q
        self.filterType = filterType
        self.globalGain = globalGain

    def getSOS(self):
        self.__sos = self.filter2SOS()
        self.__sos[0,0:3] = self.__sos[0,0:3]*10**(self.globalGain/20)
        return self.__sos

    def filter2SOS(self):
        sos = np.zeros((len(self.fc),6))
        for i in range(len(self.fc)):
            if self.filterType[i] == "lowpass":
                sos[i] = self.lowpass(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "highpass":
                sos[i] = self.highpass(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "bandpass":
                sos[i] = self.bandpass(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "bandstop":
                sos[i] = self.bandstop(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "lowshelf":
                sos[i] = self.lowshelf(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "highshelf":
                sos[i] = self.highshelf(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "peak":
                sos[i] = self.peak(self.fs,self.fc[i],self.gain[i],self.Q[i])
            elif self.filterType[i] == "allpass":
                sos[i] = self.allpass(self.fs,self.fc[i],self.gain[i],self.Q[i])
            else:
                sos[i] = np.array([1, 0, 0, 1, 0, 0])
                warnings.warn("Some filter types seem unclear.")
        return sos


    def reset(self,fs,fc,gain,Q,filterType,globalGain):
        self.fs = fs
        self.fc = fc
        self.gain = gain
        self.Q = Q
        self.filterType = filterType
        self.globalGain = globalGain

    def lowpass(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)

        b0 = (1-np.cos(omega))/2  
        b1 = 1-np.cos(omega)  
        b2 = (1-np.cos(omega))/2
        a0 = 1+alpha 
        a1 = -2*np.cos(omega) 
        a2 = 1-alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0
    
    def highpass(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)

        b0 = (1+np.cos(omega))/2
        b1 = -1-np.cos(omega)
        b2 = (1+np.cos(omega))/2
        a0 = 1+alpha 
        a1 = -2*np.cos(omega) 
        a2 = 1-alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0
    
    def bandpass(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)
        
        b0 = alpha
        b1 = 0
        b2 = -alpha
        a0 = 1+alpha
        a1 = -2*np.cos(omega)
        a2 = 1-alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0
    
    def bandstop(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)
        
        b0 = 1
        b1 = -2*np.cos(omega)
        b2 = 1
        a0 = 1+alpha
        a1 = -2*np.cos(omega)
        a2 = 1-alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0
    
    def lowshelf(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)
        
        b0 = A*((A+1)-(A-1)*np.cos(omega)+2*np.sqrt(A)*alpha)
        b1 = 2*A*((A-1)-(A+1)*np.cos(omega))
        b2 = A*((A+1)-(A-1)*np.cos(omega)-2*np.sqrt(A)*alpha)
        a0 = (A+1)+(A-1)*np.cos(omega)+2*np.sqrt(A)*alpha
        a1 = -2*((A-1)+(A+1)*np.cos(omega))
        a2 = (A+1)+(A-1)*np.cos(omega)-2*np.sqrt(A)*alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0

    def highshelf(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)
        
        b0 = A*((A+1)+(A-1)*np.cos(omega)+2*np.sqrt(A)*alpha)
        b1 = -2*A*((A-1)+(A+1)*np.cos(omega))
        b2 = A*((A+1)+(A-1)*np.cos(omega)-2*np.sqrt(A)*alpha)
        a0 = (A+1)-(A-1)*np.cos(omega)+2*np.sqrt(A)*alpha
        a1 = 2*((A-1)-(A+1)*np.cos(omega))
        a2 = (A+1)-(A-1)*np.cos(omega)-2*np.sqrt(A)*alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0

    def peak(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)
        
        b0 = 1+alpha*A
        b1 = -2*np.cos(omega)
        b2 = 1-alpha*A
        a0 = 1+alpha/A
        a1 = -2*np.cos(omega)
        a2 = 1-alpha/A
        return np.array([b0, b1, b2, a0, a1, a2])/a0
    
    def allpass(self,fs,fc,gain,Q):
        omega = 2*np.pi*fc/fs
        alpha = np.sin(omega)/2/Q
        A = 10**(gain/40)
        
        b0 = 1-alpha
        b1 = -2*np.cos(omega)
        b2 = 1+alpha
        a0 = 1+alpha
        a1 = -2*np.cos(omega)
        a2 = 1-alpha
        return np.array([b0, b1, b2, a0, a1, a2])/a0





