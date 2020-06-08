from steganography import core
from PIL import Image
import math
import cv2
import numpy as np
import pylab


class dct(core):

    block_size = 8
    banned_factors = []
    inserting_factors = block_size ** 2 - len(banned_factors)

    def __init__(self):
        self.log('SUCCESS', ' === Lab3 DCT method initialized === ')

    def __get_available_space(self, image):
        """ Get available space from image """
        img = Image.open(image)
        available_space = (img.size[0] / 8) * (img.size[1] / 8) * self.inserting_factors
        return available_space

    @staticmethod
    def PSNR(original, compressed):
        """ Get PSNR and RMSE using """
        mse = np.mean((original - compressed) ** 2)
        if mse == 0:
            return 100
        max_pixel = 255.0
        PSNR = 20 * math.log10(max_pixel / math.sqrt(mse))
        RMSE = mse ** 0.5
        return PSNR, RMSE

    def get_sygma(self, value):
        """ Calculate sygma value """
        if value == 0:
            return 1.0 / (self.block_size ** 0.5)
        else:
            return (2.0 / self.block_size) ** 0.5

    def get_factor(self, block, x, y):
        """ Get block and cords and return dkp factor """
        Fx = self.get_sygma(x)
        Fy = self.get_sygma(y)
        # print(Fx + Fy)
        for m in range(8):
            for l in range(8):
                sum += block[l][m] * math.cos((math.pi * (2 * m + 1) * x)/(2*self.block_size)) * math.cos((math.pi * (2 * l + 1) * y)/(2*self.block_size))

        factor = Fx * Fy * sum
        return factor

    def get_factor_block(self, block):
        """ Get block and convert in to factor block """
        factor_block = [[], [], [], [], [], [], [], []]
        for y in range(8):
            for x in range(8):
                factor_block[y].append(self.get_factor(block, x, y))

        return factor_block

    def get_color(self, factor_block, x, y):
        """ Get colour map from factor map """
        Fx = self.get_sygma(x)
        Fy = self.get_sygma(y)
        # print(Fx + Fy)
        sum = 0
        for l in range(8):
            for m in range(8):
                sum += self.get_sygma(l) * self.get_sygma(m) * factor_block[l][m] * math.cos((math.pi * (2 * x + 1) * m) / (2 * self.block_size)) * math.cos((math.pi * (2 * y + 1) * l) / (2 * self.block_size))

        factor = sum
        return int(round(factor))

    def get_color_block(self, factor_block):
        """ Get block and convert in to factor block """
        color_block = [[], [], [], [], [], [], [], []]
        for y in range(8):
            for x in range(8):
                color_block[y].append(self.get_color(factor_block, x, y))

        return color_block

    @staticmethod
    def split_image(image):
        """ Get image and split it to array """
        img = Image.open(image)
        width_in_blocks = img.size[0] / 8
        height_in_blocks = img.size[1] / 8
        pixel_map = img.load()
        splited_image = []
        for y in range(height_in_blocks):
            for x in range(width_in_blocks):
                splited_image.append([])
                for j in range(8):
                    splited_image[len(splited_image)-1].append([])
                    for i in range(8):
                        item = pixel_map[x*8 + i, y*8 + j]
                        splited_image[len(splited_image)-1][len(splited_image[len(splited_image)-1])-1].append(item[2]-128)

        return splited_image

    @staticmethod
    def __set_factor(bit_string, pos, factor):
        """ Calculate new factor and return it """
        if pos >= len(bit_string):
            return factor
        else:
            new_factor = float("%s.%s" % (((int(str(factor).split('.')[0]) >> 1 << 1) + int(bit_string[pos])),  str(factor).split('.')[1]))
            return new_factor

    def insert_to_block(self, block, bit_str, start_pos):
        """ Generate nef factor block """
        cur_pos = start_pos
        f_number = 0
        inserted_block = [[], [], [], [], [], [], [], []]
        for y in range(8):
            for x in range(8):
                if f_number not in self.banned_factors:
                    old_value = block[y][x]
                    inserted_block[y].append(self.__set_factor(bit_str, cur_pos, old_value))
                    cur_pos += 1
                    # if cur_pos < len(bit_str):
                    #     self.log("TEST", "Bit: %s, Set %s -> %s" % (bit_str[cur_pos-1], old_value, inserted_block[y][x]))
                f_number += 1
        return cur_pos, inserted_block

    def insert_text(self, image, text):
        """ Get text and picture and insert it to text """
        img = Image.open(image)
        width_in_blocks = img.size[0] / 8
        height_in_blocks = img.size[1] / 8
        pixel_map = img.load()

        # Check image size to contain this text
        bit_string = self.str_to_bit(text) + '0000000'
        self.log("TEST", "Bit string: %s" % bit_string)
        bit_string_len = len(bit_string)
        available_space = self.__get_available_space(image)

        if bit_string_len > available_space:
            self.log('ERROR',
                     'This image is too small to contain this text: {bit_string_len} > {available_space}').format(
                bit_string_len=bit_string_len, available_space=available_space)
            return False

        splited_image = self.split_image(image)
        new_blocks = []
        cur_pos = 0
        for block in splited_image:
            factor_block = self.get_factor_block(block)
            cur_pos, inserted_block = self.insert_to_block(factor_block, bit_string, cur_pos)
            color_block = self.get_color_block(inserted_block)
            new_blocks.append(color_block)
            if cur_pos < 128:
                self.log("TEST", "======= factor_block =======")
                print(factor_block)
                self.log("TEST", "====== inserted_block ======")
                print(inserted_block)
                self.log("TEST", "====== restored_block ======")
                print(self.get_factor_block(color_block))
                self.log("TEST", "====== color_block ======")
                print(color_block)

        width_counter = 0
        height_counter = 0
        cur_symbol = 0
        for block in new_blocks:
            for y in range(8):
                for x in range(8):
                    info = pixel_map[x + 8*width_counter, y + 8*height_counter]
                    pixel_map[x + 8*width_counter, y + 8*height_counter] = (
                        info[0],
                        info[1],
                        int(round(block[y][x])) + 128
                    )
                    cur_symbol += 1
            width_counter = width_counter + 1 if width_counter < (width_in_blocks - 1) else 0
            height_counter = height_counter + 1 if width_counter == 0 else height_counter

        img.save(image[0:len(image) - 4] + '_with_' + text[0:4] + '.bmp')
        return image[0:len(image) - 4] + '_with_' + text[0:4] + '.bmp'

    def get_text(self, image, lang):
        """ Get image and get secret text """
        splited_image = self.split_image(image)
        bit_str = ""
        test_counter = 0
        for block in splited_image:
            factor_block = test.get_factor_block(block)
            if test_counter < 2:
                self.log("TEST", "=== COLOR BLOCK ===")
                print(block)
                self.log("TEST", "=== FACTOR BLOCK ===")
                test_counter += 1
                print(factor_block)
            cur_pos = 0
            for y in range(8):
                for x in range(8):
                    if cur_pos not in self.banned_factors:
                        factor = factor_block[y][x]
                        bit = int(str(factor).split('.')[0]) % 2
                        bit_str += str(bit)
                        # if test_counter < 2:
                        #     self.log("TEST", "Get %s from %s" % (bit, factor_block[y][x]))
                    cur_pos += 1
        self.log("TEST", "Bit string from image: %s" % bit_str)
        text = self.bit_str_to_text(bit_str, lang)
        return text

    def analys(self):
        """ Analyse algorithm """
        text = 'anal'
        img = self.insert_text(
            image='lab_3/dog.bmp',
            text=text
        )
        original = cv2.imread("lab_3/dog.bmp")
        compressed = cv2.imread(img, 1)
        PSNR_value, RMSE_value = self.PSNR(original, compressed)
        self.log("SUCCESS", "PSNR value is " + str(PSNR_value) + " dB")
        self.log("SUCCESS", "RMSE value is " + str(RMSE_value) + " dB")

        xlist = []
        ylist = []
        for i in range(200):
            img = self.insert_text(
                image='lab_3/dog.bmp',
                text=text * i,
            )
            if not(img):
                print('stopped: %s' % i)
                break
            print("="),
            compressed = cv2.imread(img, 1)
            PSNR_value, RMSE_value = self.PSNR(original, compressed)
            xlist.append(i)
            ylist.append(PSNR_value)

        pylab.plot(xlist, ylist)
        pylab.savefig('lab_3/graph')


if __name__ == "__main__":
    test = dct()
    test.log("SUCCESS", test.get_text(test.insert_text('lab_3/dog.bmp', 'hello'), 'en'))
    # test.analys()