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

def mix_amb_ang(photo1,photo2 ,ratio1,ratio2 ):
    amb1=np.abs(photo1)
    amb2=np.abs(photo2)
    amblitude=amb2
    x,y,z=amb1.shape
    for i in range (int(x*ratio1)):
        for g in range(y):
            for k in range (z):
                amblitude[i,g,k]=amb1[i,g,k]
    
    ang1=np.angle(photo1)
    ang2=np.angle(photo2)
    fangle=ang1
    x,y,z=ang1.shape
    for i in range (int(x*(1-ratio2)),x):
        for g in range(y):
            for k in range (z):
                fangle[i,g,k]=ang2[i,g,k]

    combined1 = np.multiply(amblitude, np.exp(1j*fangle))

    return combined1

    
def make_amb1 (photo1,photo2,ratio):
    phase1=np.angle(photo1)
    phase2=np.angle(photo2)
    fphase=phase2
    x,y,z=fphase.shape
    for i in range (int(x*ratio)):
        for g in range(y):
            for k in range (z):
                fphase[i,g,k]=phase1[i,g,k]


    combined2 = np.multiply(amplarray, np.exp(1j*fphase))

    return combined2
def make_phase0 (photo1,photo2,ratio):
    amblitude1=np.abs(photo1)
    amblitude2=np.abs(photo2)
    famblitude =amblitude2
    x,y,z=famblitude.shape
    for i in range (int(x*ratio)):
        for g in range(y):
            for k in range (z):
                famblitude[i,g,k]=amblitude1[i,g,k]

    combined3 = np.multiply(famblitude, np.exp(1j*anglearrar))
    return combined3

def join_real_imag(photo1,photo2,ratio1,ratio2):
    real1=np.real(photo1)
    real2=np.real(photo2)
    freal=real2
    x,y,z=real2.shape
    for i in range (int(x*ratio1)):
        for g in range(y):
            for k in range (z):
                freal[i,g,k]=real1[i,g,k]

    ima1=np.imag(photo1)
    ima2=np.imag(photo2)
    fimage=ima1
    x,y,z=ima1.shape
    for i in range (int(x*(1-ratio2)),x):
        for g in range(y):
            for k in range (z):
                fimage[i,g,k]=ima2[i,g,k]


    combined4=freal +1j * fimage

    return combined4

#combined1=mix_amb_ang(photo2,photo1,1,1)
#combined2 = make_amb1 (photo2,photo2,.5) 
combined3=make_phase0(photo1,photo2,1) 
#combined4= join_real_imag (photo1,photo2,.5,.9)
# getting the real pixel values of the output image in the spatial domain
imgCombined = np.real(ifft2(combined3))

# rescaling the image to 0's and 1's
imgCombined = [ element/256 for element in imgCombined]

plt.imshow(imgCombined)
plt.show()