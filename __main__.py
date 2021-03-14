#!/usr/bin/env python
# -*- coding: utf-8 -*-

# per eseguire il programma:
# > python pypdp8tk/


from sys import exit
from tkinter import Tk, Toplevel, Canvas, N, S, E, W, NW, HORIZONTAL

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
    scrollbar1.grid(row=0, column=1, sticky=N + S)
    scrollbar2 = AutoScrollbar(emulatore, orient=HORIZONTAL)
    scrollbar2.grid(row=1, column=0, sticky=E + W)

    finestra = Canvas(
        emulatore, yscrollcommand=scrollbar1.set, xscrollcommand=scrollbar2.set
    )
    finestra.grid(row=0, column=0, sticky=N + S + E + W)

    scrollbar1.config(command=finestra.yview)
    scrollbar2.config(command=finestra.xview)

    emulatore.grid_rowconfigure(0, weight=1)
    emulatore.grid_columnconfigure(0, weight=1)

    emul = Emulatore(finestra, edit, CD, emulatore)

    finestra.create_window(0, 0, anchor=NW, window=emul.master)

    emul.master.update_idletasks()

    finestra.config(scrollregion=finestra.bbox("all"))

    principale.protocol("WM_DELETE_WINDOW", edit.exit)
    emulatore.protocol("WM_DELETE_WINDOW", emul.exit)

    principale.mainloop()
    emulatore.mainloop()


if __name__ == "__main__":
    exit(run())
