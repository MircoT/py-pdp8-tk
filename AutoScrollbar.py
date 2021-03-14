# -*- coding: utf-8 -*-


from tkinter import Scrollbar, TclError


class AutoScrollbar(Scrollbar):

    """Una scrollbar che si nasconde se non necessaria.
    Funziona solo se si usa la grid geometry.
    fonte : http://effbot.org/zone/tkinter-autoscrollbar.htm
    """

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove è attualmente assente da Tkinter.
            # Il metodo tk.call viene infatti richiamato sull'oggetto
            # scrollbar
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise (TclError, "Non si può utilizzare pack con questo widget")

    def place(self, **kw):
        raise (TclError, "Non si può utilizzare place con questo widget")
