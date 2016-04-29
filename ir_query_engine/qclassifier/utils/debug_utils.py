class DebugPrintMixin(object):

    def debug_print(self, output):
        if self.debug:
            print output
