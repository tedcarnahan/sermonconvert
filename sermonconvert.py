#!/usr/bin/env python3

from sermonconvert.controller.App import App
import sys

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
