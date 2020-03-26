class core:
    logPath = "./logs/main_log.log"

    def log(self, type, msg):
            LOG_TYPE = {
                'TEST': '\033[36mTEST:\033[0m',
                'SUCCESS': '\033[32mSUCCESS:\033[0m',
                'ERROR': '\033[31mERROR:\033[0m',
                'WARNING': '\033[35mWARNING:\033[0m',
            }

            self.logfile = open(self.logPath, 'a')
            self.logfile.write(LOG_TYPE[type] + ' ' + str(msg) + '\n\r')
            self.logfile.close()
            print(LOG_TYPE[type] + ' ' + str(msg))

    def str_to_bit(self, string):
        bit_string = ''
        for i in string :
            bit_string += ''.join(format(ord(i), 'b'))

        return bit_string

    def bit_str_to_int(self, bit_str):
        i = len(bit_str)-1
        result = 0
        while i >= 0 :
            result += int(bit_str[i]) * pow(2,(len(bit_str)-i-1))
            i -= 1

        return result

    def bit_str_to_text(self, bit_string, lang):

        secret_text = ''

        if ( lang == 'en' ):
            char_bit_len = 7
        else:
            char_bit_len = 8

        for i in range(char_bit_len, len(bit_string), char_bit_len):
            if ((bit_string[i-char_bit_len:i]) == '0000000'):
                break
            secret_text += chr(self.bit_str_to_int(bit_string[i-char_bit_len:i]))

        return secret_text
