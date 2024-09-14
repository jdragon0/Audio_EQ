# Simple description
Easily visualize data with Bode plots using fir (impulse response) or iir (sos format) filter

# Test.py 
```
fs = 48000
fc = np.array([100,200,400,800])
gain = np.array([-10,10,10,10])
Q = np.array([1,1,1,1])
filterType = np.array(["peak","peak","peak","peak"])
totalGain = 10

myfilter = filter.BiquadEQ(fs,fc,gain,Q,filterType,totalGain)
sos1 = myfilter.getSOS()

fs = 48000
fc = np.array([50,100,200,400,800,1600])
gain = np.array([10,-10,10,7,4,4])
Q = np.array([1,1,1,1,1,1])
filterType = np.array(["peak","peak","peak","peak","peak","peak"])
totalGain = 10

myfilter.reset(fs,fc,gain,Q,filterType,totalGain)
sos2 = myfilter.getSOS()

FilterPlot.sosBodePlot(fs,1,24000,2**10,sos1,sos2)
```

# Result
![Figure_1](https://github.com/user-attachments/assets/2a54e41f-26de-4c48-90b1-4107b3cdbd89)
