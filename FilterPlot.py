import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss
import scipy.fft 
import scipy.interpolate

def sosBodePlot(fs,fstart,fend,num,*soss):
    fx = np.logspace(np.log10(fstart),np.log10(fend),num)
    fig,axs = plt.subplots(2,1)
    fig.tight_layout()
    for sos in soss:
        _,h = ss.sosfreqz(sos,fx,False,fs)
        db = 20*np.log10(np.abs(h))
        deg = np.angle(h)/np.pi*180
        axs[0].semilogx(fx,db,linewidth=1)
        axs[1].semilogx(fx,deg,linewidth=1)
    axs[0].set_title("Magnitude(dB)")
    axs[0].grid(which='major',axis='both',linestyle='-',linewidth=0.5)
    axs[0].grid(which='minor',axis='both',linestyle=':',linewidth=0.5)
    axs[1].set_title("Phase(degree)")
    axs[1].grid(which='major',axis='both',linestyle='-',linewidth=0.5)
    axs[1].grid(which='minor',axis='both',linestyle=':',linewidth=0.5)
    plt.show()

def fftBodePlot(fs,fstart,fend,num,*ffts):
    fxlog = np.logspace(np.log10(fstart),np.log10(fend),num)
    fig,axs = plt.subplots(2,1)
    fig.tight_layout()
    for fft in ffts:
        n = fft.size
        fx =  scipy.fft.fftfreq(n)*fs
        f = scipy.interpolate.interp1d(fx,fft,fill_value="extrapolate")
        fft_log = f(fxlog)
        db = 20*np.log10(np.abs(fft_log))
        deg = np.angle(fft_log)/np.pi*180
        axs[0].semilogx(fxlog,db,linewidth=1)
        axs[1].semilogx(fxlog,deg,linewidth=1)
    axs[0].set_title("Magnitude(dB)")
    axs[0].grid(which='major',axis='both',linestyle='-',linewidth=0.5)
    axs[0].grid(which='minor',axis='both',linestyle=':',linewidth=0.5)
    axs[1].set_title("Phase(degree)")
    axs[1].grid(which='major',axis='both',linestyle='-',linewidth=0.5)
    axs[1].grid(which='minor',axis='both',linestyle=':',linewidth=0.5)
    plt.show()
    return
