from matplotlib import image
from matplotlib import pyplot as plt                                                                           
import numpy as np
from numpy.fft import ifft2, fft2, fftshift
import cmath

# load image as pixel array
image1 = image.imread('images/photo1.jpeg', 0)
image2 = image.imread('images/photo2.jpeg', 0)


# FT of the first image
photo1 = fft2(image1)

# shifting FT matrix
fshift1 = fftshift(photo1)

# getting phase and magnitude spectrums
phase_spectrumA = np.angle(fshift1)
magnitude_spectrumA = np.abs(fshift1)

# FT of the second image
photo2 = fft2(image2)

# shifting FT matrix
fshift2 = fftshift(photo2)

# getting phase and magnitude spectrums
phase_spectrumB = np.angle(fshift2)
magnitude_spectrumB = 20*np.log(np.abs(fshift2))


# combining phase, magnitude spectrums into output image 
# (YOU CAN EDIT HERE TO DECIDE WHAT TO COMBINE)
amplarray=np.abs(photo1)
x,y,z=amplarray.shape
for i in range (x):
    for g in range(y):
        for k in range (z):
            amplarray[i,g,k]=1
anglearrar=np.angle(photo1)
x,y,z=amplarray.shape
for i in range (x):
    for g in range(y):
        for k in range (z):
            anglearrar[i,g,k]=0
def mix_amb_ang(make1,amb ,angle,ratio1 ):
    combined1 = np.multiply(np.abs(amb), np.exp(1j*np.angle(angle)))
    p=make1
    for i in range (int(x*ratio1)):
        for g in range(y):
            for k in range (z):
                 p[i,g,k]=combined1[i,g,k]
    
    return p
def make_amb1 (make2,angle2,ratio2):
    combined2 = np.multiply(amplarray, np.exp(1j*np.angle(angle2)))
    o=make2
    for i in range (int(x*ratio2)):
        for g in range(y):
            for k in range (z):
                 o[i,g,k]=combined2[i,g,k]
    return o
def make_phase0 (make3,amblitude,ratio3 ):
    combined3 = np.multiply(np.abs(amblitude), np.exp(1j*anglearrar))
    r=make3
    for i in range (int(x*ratio3)):
        for g in range(y):
            for k in range (z):
                 r[i,g,k]=combined3[i,g,k]
    return r
def join_real_imag(make4,real,ima,ratio4):
    combined4=np.real(real) +1j *np.imag(ima)
    l=make4
    for i in range (int(x*ratio4)):
        for g in range(y):
            for k in range (z):
                 l[i,g,k]=combined4[i,g,k]

    return l

#combined1=mix_amb_ang(photo2,photo1,photo2,.5)
#combined2 = make_amb1 (photo1,photo1,.5) 
#combined3=make_phase0(photo2,photo2,.5) 
combined4= join_real_imag (photo1,photo1,photo2,.5)
# getting the real pixel values of the output image in the spatial domain
imgCombined = np.real(ifft2(combined4))

# rescaling the image to 0's and 1's
imgCombined = [ element/256 for element in imgCombined]

plt.imshow(imgCombined)
plt.show()