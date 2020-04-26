from steganography import core
from PIL import Image


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


if __name__ == "__main__":

    # Init lsb class
    m_lsb = lsb()
    img = m_lsb.insert_text(
        image='lab_2/dog.bmp',
        text='Hiolesa'
    )
    secret_text = m_lsb.get_secret_text(image=img, lang='en')
    print(secret_text)
