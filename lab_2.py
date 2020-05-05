from steganography import core
from PIL import Image
from math import log10, sqrt
import cv2
import numpy as np
import pylab
from matplotlib import mlab


class lsb(core):

    def __init__(self):
        self.log('SUCCESS', ' === Lab2 LSB method initialized === ')

    def __get_availabel_space(self, image):
        img = Image.open(image)
        available_space = img.size[0] * img.size[1] * 3
        return available_space

    def __set_color(self, bit_string, pos, color):
        if pos >= len(bit_string):
            return color
        else:
            return (color // 2) * 2 + int(bit_string[pos])

    def PSNR(self, original, compressed):
        mse = np.mean((original - compressed) ** 2)
        if(mse == 0):
            return 100
        max_pixel = 255.0
        psnr = 20 * log10(max_pixel / sqrt(mse))
        return psnr

    def insert_text(self, image, text):
        img = Image.open(image)
        pixel_map = img.load()

        # Check image size to contain this text
        bit_string = self.str_to_bit(text) + '0000000'
        bit_string_len = len(bit_string)
        available_space = self.__get_availabel_space(image)

        if (bit_string_len > available_space):
            self.log('ERROR', 'This image is too small to contain this text: {bit_string_len} > {available_space}').format(bit_string_len=bit_string_len, available_space=self.__get_availabel_space(image))
            return False

        # Insert text to image
        cur_symbol = 0
        for x in range(img.size[0]):
            if cur_symbol >= bit_string_len:
                break
            for y in range(img.size[1]):
                info = pixel_map[x, y]
                pixel_map[x, y] = (
                    self.__set_color(bit_string, cur_symbol, info[0]),
                    self.__set_color(bit_string, cur_symbol + 1, info[1]),
                    self.__set_color(bit_string, cur_symbol + 2, info[2])
                )
                cur_symbol += 3

        img.save(image[0:len(image) - 4] + '_with_' + text[0:4] + '.bmp')
        return image[0:len(image) - 4] + '_with_' + text[0:4] + '.bmp'

    def get_secret_text(self, image, lang):
        img = Image.open(image)
        pixel_map = img.load()
        bit_string = ''
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                info = pixel_map[x, y]
                for i in range(3):
                    bit_string += str(info[i] % 2)

        return self.bit_str_to_text(bit_string, lang)

    def analys(self):
        text = 'analys'
        img = self.insert_text(
            image='lab_2/dog.bmp',
            text=text
        )
        original = cv2.imread("lab_2/dog.bmp")
        compressed = cv2.imread("lab_2/dog_with_anal.bmp", 1)
        PSNR_value = self.PSNR(original, compressed)
        print("PSNR value is " + str(PSNR_value) + " dB")

        xlist = []
        ylist = []
        for i in range(200):
            img = self.insert_text(
                image='lab_2/dog.bmp',
                text=text * i
            )
            if not(img):
                print('stopped: ' + i)
                break
            compressed = cv2.imread("lab_2/dog_with_anal.bmp", 1)
            PSNR_value = self.PSNR(original, compressed)
            xlist.append(i)
            ylist.append(PSNR_value)

        pylab.plot(xlist, ylist)
        pylab.savefig('lab_2/graph')


if __name__ == "__main__":

    # Init lsb class
    m_lsb = lsb()

    m_lsb.analys()

    m_lsb.get_secret_text(m_lsb.insert_text('lab_2/dog.bmp', 'hello'), 'en')
