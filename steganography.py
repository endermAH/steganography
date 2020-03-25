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
