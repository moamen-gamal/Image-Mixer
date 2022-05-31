from PyQt5 import QtGui, QtWidgets
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as img
from numpy.fft import ifft2, fft2
from PyQt5.QtGui import QImage, QPixmap, qRgb
import logging


logging.basicConfig(filename = 'test.log', level = logging.DEBUG, format = '%(levelname)s:%(message)s')
mixerComponents = ['amplitude', 'phase', 'real', 'imaginary', 'unity Amplitude', 'zero Phase']
imgs = ['image 1', 'image 2']

gray_color_table = [qRgb(i, i, i) for i in range(256)]

def toQImage(im, copy=False):
    if im is None:
        return QImage()

    im = np.require(im, np.uint8, 'C')
    if im.dtype == np.uint8:
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                return qim.copy() if copy else qim

class image(object):
    shape = None
    def __init__(self, imgWidgets, imagePath):
        image = img.imread(imagePath, 0)
        if self.__class__.shape is not None:
            if not self.__class__.shape == image.shape:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('two images must be same size!')
                self.__del__()
        self.__class__.shape = image.shape
        self.inputImg = imgWidgets[0]
        self.outputImg = imgWidgets[1]
        self.outputSelector = imgWidgets[2]
        self.imagePath = imagePath

        fourier_coefficients = fft2(image)
        self.components = {}
        self.components['amplitude'] = np.abs(fourier_coefficients)
        self.components['phase'] = np.angle(fourier_coefficients)
        self.components['real'] = np.real(fourier_coefficients)
        self.components['imaginary'] = np.imag(fourier_coefficients)
        self.components['unity Amplitude'] = np.abs(fourier_coefficients)
        self.components['zero Phase'] = np.abs(fourier_coefficients)
        for i in range(self.__class__.shape[0]):
            for j in range(self.__class__.shape[1]):
                for k in range(self.__class__.shape[2]):
                    self.components['unity Amplitude'][i, j, k] = 1
                    self.components['zero Phase'][i, j, k] = 0

        self.display()

    def display(self):
        self.inputImg.setPixmap(QtGui.QPixmap(self.imagePath))
        self.outputImg.setPixmap(QtGui.QPixmap(toQImage(self.components[self.outputSelector.currentText()])))

class component(object):
    def __init__(self, img_selector, component_selector, ratio, slotFunction):
        self.ratio = ratio
        self.img_selector = img_selector
        self.component_selector = component_selector
        self.img_selector.activated.connect(slotFunction)
        self.component_selector.activated.connect(slotFunction)
        self.ratio.sliderReleased.connect(slotFunction)
        self.component_selector.addItems([component for component in mixerComponents])
        self.img_selector.addItems([img for img in imgs])
        self.previousItems = mixerComponents

    def setItems(self, items):
        if items != self.previousItems:
            logging.debug("previous items: ")
            for item in self.previousItems:
                logging.debug(item + ', ')
            logging.debug("new Items: ")
            for item in items:
                logging.debug(item + ', ')
            self.previousItems = items
            self.component_selector.clear()
            self.component_selector.addItems(items)
        else:
            pass

def mix(amplitude = None, phase = None, real = None, imaginary = None
        ,refAmplitude = None, refPhase = None, refReal = None, refImaginary = None, ratio1 = 100, ratio2 = 100):
    if amplitude is not None and phase is not None:
        limitIdx1 = int((len(amplitude) - 1) * (ratio1/100))
        limitIdx2 = int((len(phase) - 1) * (ratio2/100))
        # amplitude = np.append(amplitude[:limitIdx1, :, :], refAmplitude[limitIdx1 + 1:, :, :], 0)
        # phase = np.append(phase[:limitIdx2, :, :], refPhase[limitIdx2 + 1:, :, :], 0)
        amplitude = amplitude * (ratio1/100) + refAmplitude * (1 - (ratio1/100))
        phase = phase * (ratio2/100) + refPhase * (1 - (ratio2/100))
        return np.real(ifft2(np.multiply(amplitude, np.exp(1j*phase))))
    elif real is not None and imaginary is not None:
        limitIdx1 = int((len(real) - 1) * (ratio1/100))
        limitIdx2 = int((len(imaginary) - 1) * (ratio2/100))
        # real = np.append(real[:limitIdx1, :, :], refReal[limitIdx1 + 1:, :, :], 0)
        # imaginary = np.append(imaginary[:limitIdx2, :, :], refImaginary[limitIdx2 + 1:, :, :], 0)
        real = real * (ratio1/100) + refReal * (1 - (ratio1/100))
        imaginary = imaginary * (ratio2/100) + refImaginary * (1 - (ratio2/100))
        return np.real(ifft2(np.add(real, 1j * imaginary)))

class Mixer(object):
    def __init__(self, outputs, component1, component2, images, outputSelector):
        self.outputs = outputs
        self.component1 = component1
        self.component2 = component2
        self.images = images
        self.outputSelector = outputSelector
        self.component2.component_selector.setCurrentText('phase')
        self.display()

    def display(self):
        self.combinedImg = None
        if (self.component1.component_selector.currentText() == 'amplitude' or self.component1.component_selector.currentText() == 'unity Amplitude'):
            self.component2.setItems(['phase', 'zero Phase'])
            self.combinedImg = mix(amplitude= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   phase= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   refAmplitude = self.images[self.component2.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   refPhase = self.images[self.component1.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   ratio1 = self.component1.ratio.value(),
                                   ratio2 = self.component2.ratio.value())
        elif (self.component1.component_selector.currentText() == 'phase' or self.component1.component_selector.currentText() == 'zero Phase'):
            self.component2.setItems(['amplitude', 'unity Amplitude'])
            self.combinedImg = mix(phase= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   amplitude= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   refAmplitude = self.images[self.component1.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   refPhase = self.images[self.component2.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   ratio1 = self.component2.ratio.value(),
                                   ratio2 = self.component1.ratio.value())
        elif self.component1.component_selector.currentText() == 'real':
            self.component2.setItems(['imaginary'])
            self.combinedImg = mix(real= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   imaginary= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   refReal = self.images[self.component2.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   refImaginary = self.images[self.component1.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   ratio1 = self.component1.ratio.value(),
                                   ratio2 = self.component2.ratio.value())
        elif self.component1.component_selector.currentText() == 'imaginary':
            self.component2.setItems(['real'])
            self.combinedImg = mix(imaginary= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   real= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   refImaginary = self.images[self.component2.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   refReal = self.images[self.component1.img_selector.currentText()].components[self.component2.component_selector.currentText()],
                                   ratio1 = self.component2.ratio.value(),
                                   ratio2 = self.component1.ratio.value())

        if self.combinedImg is not None:
            self.outputs[self.outputSelector.currentText()].setPixmap(QtGui.QPixmap(toQImage(self.combinedImg)))
