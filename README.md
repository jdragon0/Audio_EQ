# FilterPlot
Easily visualize data with Bode plots using fir (impulse response) or iir (sos format) filter

fs = 48000

fc = np.array([100,200,400,800])

gain = np.array([-10,10,10,10])

Q = np.array([1,1,1,1])

filterType = np.array(["peak","peak","peak","peak"])

totalGain = 10

myfilter = filter.BiquadEQ(fs,fc,gain,Q,filterType,totalGain)

sos1 = myfilter.getSOS()

FilterPlot.sosBodePlot(fs,1,24000,2**10,sos1)



![Figure_1](https://github.com/user-attachments/assets/d091c9b4-7e9d-4066-b884-50e16b158a34)
