# -*- coding: utf-8 -*-

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

from Tkinter import Scrollbar, TclError

class AutoScrollbar(Scrollbar):
    """ Una scrollbar che si nasconde se non necessaria.
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
        raise TclError, "Non si può utilizzare pack con questo widget"

    def place(self, **kw):
        raise TclError, "Non si può utilizzare place con questo widget"
