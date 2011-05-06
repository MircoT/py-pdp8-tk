#!/usr/bin/env python
# -*- coding: utf-8 -*-

# per eseguire il programma:
# > python pypdp8tk/

#------------------------------------------------------------------------#
# Copyright (C) 2011  Mirco Tracolli                                     #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#                                                                        #
#  Contact: m.tracolli@gmail.com                                         #
#                                                                        #
#  Collaborators: Walter Valentini                                       #
#________________________________________________________________________#

from sys import exit
from Tkinter import Tk, Toplevel, Canvas, N, S, E, W, NW, HORIZONTAL

from pdp8 import pdp8
from AutoScrollbar import AutoScrollbar
from Emulatore import Emulatore
from Editor import Editor

def run():
    """
    Esegue l'emulatore del pdp8
    """
    CD = pdp8()
    principale = Tk()
    principale.title("Pdp8 Emulator : Assembly Editor")
    emulatore = Toplevel()
    emulatore.title("Pdp8 Emulator")
    emulatore.geometry("1015x589")
    
    edit = Editor(principale, CD)
    
    scrollbar1 = AutoScrollbar(emulatore)
    scrollbar1.grid(row = 0, column = 1, sticky = N+S)
    scrollbar2 = AutoScrollbar(emulatore, orient = HORIZONTAL)
    scrollbar2.grid(row = 1, column = 0, sticky = E+W)
    
    finestra = Canvas (emulatore,
                     yscrollcommand = scrollbar1.set,
                     xscrollcommand = scrollbar2.set)
    finestra.grid(row = 0, column = 0, sticky = N+S+E+W)
    
    scrollbar1.config(command = finestra.yview)
    scrollbar2.config(command = finestra.xview)
    
    emulatore.grid_rowconfigure(0, weight = 1)
    emulatore.grid_columnconfigure(0, weight = 1)
    
    emul = Emulatore(finestra,edit,CD,emulatore)
    
    finestra.create_window(0, 0, anchor = NW, window = emul.master)
    
    emul.master.update_idletasks()
    
    finestra.config(scrollregion = finestra.bbox("all"))
    
    principale.protocol("WM_DELETE_WINDOW", edit.exit)
    emulatore.protocol("WM_DELETE_WINDOW", emul.exit)
    
    principale.mainloop()
    emulatore.mainloop()
    

if __name__ == '__main__':
    exit(run())
