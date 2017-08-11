#!/usr/bin/env python3

import sermonconvert.controller.App
import sys

if __name__ == '__main__':
    app = sermonconvert.controller.App
    sys.exit(app.exec_())
