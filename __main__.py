# -*- coding: utf-8 -*-


"""
Created on Jun 23, 2011

@author: Mirco Tracolli
"""

from wxGUI import APP
from sys import exit


def run():
    App = APP(False)

    App.MainLoop()


if __name__ == "__main__":
    exit(run())
