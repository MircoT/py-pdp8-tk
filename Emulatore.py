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


from Tkinter import Frame, LabelFrame, Text, Scrollbar, Button, Label,\
RIDGE, W, E, N, S, FLAT, CENTER, SUNKEN, END, INSERT
from tkSimpleDialog import askinteger, askstring
from tkMessageBox import askquestion, showinfo , YES, WARNING

from pdp8 import pdp8

class Emulatore(object):
    """
    Interfaccia grafica per l'emulatore del pdp8
    """
    def __init__(self,master,codice,calcolatore,emulatore):
        """
        Inizializza i frame per l'interfaccia dell'emulatore
        """
        self.CD = calcolatore
        self.codice = codice
        self.delay = 100
        self.master = Frame(master)
        self.root = emulatore

        ## Memoria Ram
        self.ram = LabelFrame(self.master, text = 'Memoria RAM', relief = RIDGE, borderwidth = 5, labelanchor = 'n', pady = 5)
        self.ram.rowconfigure(0, weight=1)
        self.ram.columnconfigure(0, weight=1)
        self.ram.grid(row = 0, column = 0,rowspan = 3, columnspan = 5, sticky = W+E+N+S)

        ## Controlli
        self.controlli = Frame(self.master, padx = 10, pady = 10)
        self.controlli.grid(row = 0, column = 5,rowspan = 1)

        ## Status CD
        self.registri = LabelFrame(self.master, text = 'REGISTRI', relief = RIDGE, borderwidth = 5, labelanchor = 'n',padx = 25,pady = 10)
        self.registri.grid(row = 0, column = 6,rowspan = 1, sticky = W+E+N+S)
        self.unita = LabelFrame(self.master, text = 'UC', relief = RIDGE, borderwidth = 5, labelanchor = 'n', padx = 10, pady = 10)
        self.unita.grid(row = 2, column = 6, rowspan = 1, sticky = N)

        ## Var
        self.variabili = Frame(self.master)
        self.variabili.grid(row = 2, column = 5)
        self.nstep = LabelFrame(self.variabili, text = 'Num. Step', relief = RIDGE, borderwidth = 5, labelanchor = 'n')
        self.nstep.grid(row = 0, column = 5,sticky = W+E)
        self.delays = LabelFrame(self.variabili, text = 'Delay', relief = RIDGE, borderwidth = 5, labelanchor = 'n')
        self.delays.grid(row = 1, column = 5,sticky = W+E)
        self.tempo = LabelFrame(self.variabili, text = 'Tempo', relief = RIDGE, borderwidth = 5, labelanchor = 'n')
        self.tempo.grid(row = 1, column = 6,sticky = W+E)

        ### Unita' di controllo
        self.unitas = LabelFrame(self.unita, text = 'S', labelanchor = 's', padx = 10)
        self.unitas.grid(row = 0, column = 0, sticky = N)
        self.unitaf = LabelFrame(self.unita, text = 'F', labelanchor = 's', padx = 10)
        self.unitaf.grid(row = 0, column = 1, sticky = N)
        self.unitar = LabelFrame(self.unita, text = 'R', labelanchor = 's', padx = 10)
        self.unitar.grid(row = 0, column = 2, sticky = N)
        self.unitaint = LabelFrame(self.unita, text = 'Int.', labelanchor = 's', padx = 10)
        self.unitaint.grid(row = 0, column = 3, sticky = N)

        ### Registri
        self.programc = LabelFrame(self.registri, text = 'PC',relief = FLAT, labelanchor = 'e', padx = 5)
        self.programc.grid(row = 0, column = 0, sticky = W+E)
        self.mar = LabelFrame(self.registri, text = 'MAR',relief = FLAT, labelanchor = 'e', padx = 5)
        self.mar.grid(row = 1, column = 0, sticky = W+E)
        self.mbr = LabelFrame(self.registri, text = 'MBR',relief = FLAT, labelanchor = 'e', padx = 5)
        self.mbr.grid(row = 2, column = 0, sticky = W+E)
        self.lac = LabelFrame(self.registri, text = 'AC',relief = FLAT, labelanchor = 'e', padx = 5)
        self.lac.grid(row = 3, column = 0, sticky = W+E)
        self.vare = LabelFrame(self.registri, text = 'E',relief = FLAT, labelanchor = 'e', padx = 5)
        self.vare.grid(row = 4, column = 0, sticky = W+E)
        self.lopr = LabelFrame(self.registri, text = 'OPR',relief = FLAT, labelanchor = 'e', padx = 5)
        self.lopr.grid(row = 5, column = 0, sticky = W+E)
        self.vari = LabelFrame(self.registri, text = 'I',relief = FLAT, labelanchor = 'e', padx = 5)
        self.vari.grid(row = 6, column = 0, sticky = W+E)

        ## Microistruzioni
        self.micro = LabelFrame(self.master, text = 'Microistruzioni eseguite', relief = RIDGE, borderwidth = 5, labelanchor = 'n', pady = 5)
        self.micro.rowconfigure(0, weight=1)
        self.micro.columnconfigure(0, weight=1)
        self.micro.grid(row = 3, column = 4,rowspan = 5, columnspan = 5, sticky = W+E+N+S)

        ## Inout
        self.inout = LabelFrame(self.master, text = 'Input & Output', relief = RIDGE, borderwidth = 5, labelanchor = 'n', pady = 5)
        self.inout.rowconfigure(0, weight=1)
        self.inout.columnconfigure(0, weight=1)
        self.inout.grid(row = 3, column = 0, columnspan = 4, sticky = W+E+N+S)
        
        self.create_widgets()

    def create_widgets(self):
        """
        Crea il layout del programma, finestra dell'emulatore
        """
        ## Memoria RAM
        self.Visualizza = Text(self.ram, width = 80)
        self.Visualizzascrollbar = Scrollbar(self.ram)
        self.Visualizzascrollbar.config(command = self.Visualizza.yview)
        self.Visualizza.config(yscrollcommand = self.Visualizzascrollbar.set)
        self.Visualizzascrollbar.grid(row = 0, column = 1, sticky = N+S)
        self.Visualizza.grid(row = 0, column = 0, sticky = W)

        ## INOUT
        self.Visualizzainout = Text(self.inout, width = 62, height = 7, fg = 'green', bg = 'black')
        self.Visualizzascrollbar_inout = Scrollbar(self.inout)
        self.Visualizzascrollbar_inout.config(command = self.Visualizzainout.yview)
        self.Visualizzainout.config(yscrollcommand = self.Visualizzascrollbar_inout.set)
        self.Visualizzascrollbar_inout.grid(row = 0, column = 1, sticky = N+S)
        self.Visualizzainout.grid(row = 0, column = 0, sticky = W)

        ## Mircroistruzioni
        self.Visualizzamicro = Text(self.micro, width = 55, height = 7)
        self.Visualizzascrollbar_m = Scrollbar(self.micro)
        self.Visualizzascrollbar_m.config(command = self.Visualizzamicro.yview)
        self.Visualizzamicro.config(yscrollcommand = self.Visualizzascrollbar_m.set)
        self.Visualizzascrollbar_m.grid(row = 0, column = 1, sticky = N+S)
        self.Visualizzamicro.grid(row = 0, column = 0, sticky = W)

        ### Pulsanti
        self.butload = Button(self.controlli, text = 'LOAD', anchor = CENTER, width = 15, command = self.loading, bg = 'SkyBlue')
        self.butload.grid(row = 0, column = 0)
        self.butstep = Button(self.controlli, text = 'Step', anchor = CENTER, width = 15, command = self.step, bg = 'linen')
        self.butstep.grid(row = 1, column = 0)
        self.butminstep = Button(self.controlli, text = 'miniStep', anchor = CENTER, width = 15, command = self.mini_step, bg = 'linen')
        self.butminstep.grid(row = 2, column = 0)
        self.butstep = Button(self.controlli, text = 'microStep', anchor = CENTER, width = 15, command = self.micro_step, bg = 'linen')
        self.butstep.grid(row = 3, column = 0)
        self.butsetstep = Button(self.controlli, text = 'Set n Step', anchor = CENTER, width = 15, command = self.setnstep, bg = 'linen')
        self.butsetstep.grid(row = 4, column = 0)
        self.butsetdelay = Button(self.controlli, text = 'Set Delay', anchor = CENTER, width = 15, command = self.setdelay, bg = 'linen')
        self.butsetdelay.grid(row = 5, column = 0)
        self.butstart = Button(self.controlli, text = 'START', anchor = CENTER, width = 15, command = self.start, bg = 'DarkOliveGreen3')
        self.butstart.grid(row = 6, column = 0)
        self.butreset = Button(self.controlli, text = 'RESET', anchor = CENTER, width = 15, command = self.resetCD, bg = 'Orange3')
        self.butreset.grid(row = 7, column = 0)
        self.butstop = Button(self.controlli, text = 'STOP', anchor = CENTER, width = 15, command = self.stop, bg = 'IndianRed')
        self.butstop.grid(row = 8, column = 0)
        self.butbreak = Button(self.controlli, text = 'BREAK', anchor = CENTER, width = 15, command = self.breakpoint, bg = 'Magenta2')
        self.butbreak.grid(row = 9, column = 0)
        self.butcontinue = Button(self.controlli, text = 'CONTINUA', anchor = CENTER, width = 15, command = self.continua, bg = 'Magenta2')
        self.butcontinue.grid(row = 10, column = 0)
        self.butesegui = Button(self.controlli, text = 'ESEGUI', anchor = CENTER, width = 15, command = self.esegui, bg = 'Yellow')
        self.butesegui.grid(row = 11, column = 0)

        ### Labels
        self.labelprogramc = Label(self.programc, text = '00000000000', relief = SUNKEN, bg = 'red')
        self.labelprogramc.grid()
        self.labelmar = Label(self.mar, text = '00000000000', relief = SUNKEN, bg = 'yellow')
        self.labelmar.grid()
        self.labelmbr = Label(self.mbr, text = '000000000000000', relief = SUNKEN)
        self.labelmbr.grid()
        self.labelac = Label(self.lac, text = '000000000000000', relief = SUNKEN)
        self.labelac.grid()
        self.labelvari = Label(self.vari, text = '0', relief = SUNKEN)
        self.labelvari.grid()
        self.labelvare = Label(self.vare, text = '0', relief = SUNKEN)
        self.labelvare.grid()
        self.labelopr = Label(self.lopr, text = '000', relief = SUNKEN)
        self.labelopr.grid()
        self.labelucs = Label(self.unitas, text = '0')
        self.labelucs.grid()
        self.labelucf = Label(self.unitaf, text = '0')
        self.labelucf.grid()
        self.labelucr = Label(self.unitar, text = '0')
        self.labelucr.grid()
        self.labelucint = Label(self.unitaint, text = '0')
        self.labelucint.grid()
        self.labelnstep = Label(self.nstep, text = '1')
        self.labelnstep.grid()
        self.labeldelay = Label(self.delays, text = str(self.delay))
        self.labeldelay.grid()
        self.labeltempo = Label(self.tempo, text = str(self.CD.tempo))
        self.labeltempo.grid()
    
    def continua(self):
        """
        Continua l'esecuzione dopo un break
        """
        self.CD.S = True
        self.esegui()
    
    def micro_step(self):
        """
        Esegue il metodo step del calcolatore didattico ed aggiorna
        """
        if self.CD.S:
            self.CD.step(self.root,self.codice)
            if self.CD.tempo == 0 and not self.CD.F and not self.CD.R:
                self.CD.previstr = self.CD.nextistr
            self.aggiornaall()
    
    def step(self):
        """
        Esegue il metodo step del calcolatore didattico ed aggiorna
        """
        var = True
        if self.CD.S and self.CD.nstep > 0:
            while var and self.CD.S:
                self.CD.step(self.root,self.codice)
                if not self.CD.F and not self.CD.R and self.CD.tempo == 0:
                    self.CD.nstep -= 1
                    self.aggiornaall()
                    self.CD.previstr = self.CD.nextistr
                    var = False
            if self.CD.nstep > 0:
                self.butstep.after(self.delay, self.step)
            else :
                self.CD.setnstep(1)
        else :
            self.CD.setnstep(1)
            self.aggiornaall()
    
    def esegui(self):
        """
        Esegue il programma fino all'arresto della macchina tramite
        l'istruzione HLT
        """
        while self.CD.S:
            self.CD.step(self.root,self.codice)
            if not self.CD.F and not self.CD.R and self.CD.tempo == 0:
                self.aggiornaall()
                self.CD.previstr = self.CD.nextistr
                break
        if self.CD.S:
            self.butesegui.after(self.delay, self.esegui)
        else :
            self.CD.setnstep(1)
            self.aggiornaall()
    
    def mini_step(self):
        """
        Esegue un singolo ciclo della macchina
        """
        if self.CD.S:
            for x in range(0,4):
                self.CD.step(self.root,self.codice)
                self.CD.nstep = 1
                self.aggiornaall()
            if self.CD.F is False and self.CD.R is False:
                self.CD.previstr = self.CD.nextistr
            
    def cerca_istr_prev(self):
        """
        Evidenzia di VERDE l'ultima istruzione eseguita
        """
        if self.CD.PC == '000000000000':
            return
        try:
            if self.CD.previstr == '' and int(self.CD.PC,2) == self.CD.START:
                return
            else:
                pospc = str(3.0 + self.CD.previstr)
                self.Visualizza.tag_add("PISTR", str(pospc[:-1]+'16'),  str(pospc[:-1]+'end'))
                self.Visualizza.tag_config("PISTR", background = "green")
                self.Visualizza.see(pospc)
        except TypeError:
            pass ## Errore che si ottiene durante il reset del CD

    # NOTA : METODO NON NECESSARIO NEL PROGRAMMA FINALE
    #def cerca_istr_corr(self):
    #    """
    #    Evidenzia di verde l'istruzione che si dovrà eseguire
    #    """
    #    if self.CD.PC == '000000000000':
    #        return
    #    try:
    #        if int(self.CD.PC,2) == self.CD.START:
    #            ## Inizio esecuzione del programma
    #            ## Il PC e l'istruzione da eseguire sono allo stesso 'livello'
    #            pos = str(3.0)
    #            self.Visualizza.tag_add("ISTR", str(pos[0]+'.16'), str(pos[:-1]+'end'))
    #            self.Visualizza.tag_config("ISTR", background = "green")
    #        else:
    #            pospc = str(3.0 + self.CD.nextistr)
    #            self.Visualizza.tag_add("ISTR", str(pospc[:-1]+'16'),  str(pospc[:-1]+'end'))
    #            self.Visualizza.tag_config("ISTR", background = "green")
    #            self.Visualizza.see(pospc)
    #    except TypeError:
    #        pass ## Errore che si ottiene durante il reset del CD

    def cerca_MAR(self):
        """
        Evidenzia di giallo l'indirizzo puntato dal MAR
        """
        try:
            pos = 3.0
            stringa = self.Visualizza.get(str(pos),'end')
            while stringa[:12] != self.CD.MAR and int(pos) < len(self.CD.RAM)+3 and len(self.CD.RAM)>0:
                pos += 1
                stringa = self.Visualizza.get(str(pos),'end')
            if int(pos) >= len(self.CD.RAM)+3:
                return
            self.Visualizza.tag_add("MAR", pos, str(float(pos)+0.12))
            self.Visualizza.tag_config("MAR", background = "yellow")
        except TypeError:
            pass ## Errore che si ottiene durante il reset del CD

    def cerca_PC(self):
        """
        Evidenzia di rosso l'indirizzo puntato da PC
        """
        try:
            pos = 3.0
            stringa = self.Visualizza.get(str(pos),'end')
            while stringa[:12] != self.CD.PC and int(pos) < len(self.CD.RAM)+3 and len(self.CD.RAM)>0:
                pos += 1
                stringa = self.Visualizza.get(str(pos),'end')
            if int(pos) >= len(self.CD.RAM)+3:
                return
            self.Visualizza.tag_add("PC", pos, str(float(pos)+0.12))
            self.Visualizza.tag_config("PC", background = "red")
        except TypeError:
            pass ## Errore che si ottiene durante il reset del CD
    
    

    def aggiornaout(self):
        """
        Aggiorna micro e input/output
        """
        self.aggiornamicro()
        self.aggiornainout()

    def aggiornamicro(self):
        """
        Aggiorna le microistruzioni eseguite
        """
        self.Visualizzamicro.delete(1.0, END)
        stringa = self.CD.microistruzioni
        self.Visualizzamicro.insert(INSERT,stringa)
        self.Visualizzamicro.see(END)

    def aggiornainout(self):
        """
        Aggiorna gli input ed output di sistema
        """
        self.Visualizzainout.delete(1.0, END)
        stringa = self.CD.inout
        self.Visualizzainout.insert(INSERT,stringa)
        self.Visualizzainout.see(END)

    def aggiornaram(self):
        """
        Aggiorna lo stato della RAM
        """
        self.Visualizza.delete(1.0 , END)
        stringa = self.CD.statusRAM()
        self.Visualizza.insert(INSERT,stringa)
        self.cerca_MAR()
        self.cerca_PC()
        self.cerca_istr_prev()
        #self.cerca_istr_corr() #Non più necessaria nella versione finale

    def aggiornareg(self):
        """
        Aggiorna lo stato dei Registri
        """
        self.labelprogramc.config(text = self.CD.PC)
        self.labelmar.config(text = self.CD.MAR)
        self.labelmbr.config(text = self.CD.MBR)
        self.labelac.config(text = self.CD.AC)
        self.labelvare.config(text = self.CD.E)
        self.labelvari.config(text = self.CD.I)
        self.labelopr.config(text = self.CD.OPR)

    def aggiornauc(self):
        """
        Aggiorna lo stato dell'unita' di controllo
        """
        if self.CD.S and not self.CD.breaks:
            self.labelucs.config(text = self.CD.S, bg = 'green')
            self.unitas.config(bg = 'green')
        elif not self.CD.S and self.CD.breaks:
            self.labelucs.config(text = self.CD.S, bg = 'Magenta2')
            self.unitas.config(bg = 'Magenta2')
        else :
            self.labelucs.config(text = self.CD.S, bg = 'red')
            self.unitas.config(bg = 'red')
        self.labelucf.config(text = self.CD.F)
        self.labelucr.config(text = self.CD.R)
        self.labelucint.config(text = self.CD.Interrupt)
        self.labeltempo.config(text = self.CD.tempo)

    def aggiornaall(self):
        """
        Aggiorna tutto
        """
        self.aggiornaram()
        self.aggiornareg()
        self.aggiornauc()
        self.aggiornamicro()
        self.aggiornaout()
        self.labelnstep.config(text = self.CD.nstep)

    def loading(self):
        """
        Carica il contenuto del codice assembly decodificandolo in binario
        nella RAM
        """
        contenuto = self.codice.Inserisci.get(1.0, END)
        if len(contenuto)>1:
                self.resetCD()
                if  self.CD.carica(contenuto.decode('ascii','ignore'),self) is not None:
                    self.CD.S = 0
                    self.aggiornaall()

    def resetCD(self):
        """
        Resetta il calcolatore didattico
        """
        self.CD = pdp8()
        self.aggiornaall()

    def start(self):
        """
        Mette la variabile Start (S) ad 1, cioe' True
        """
        self.CD.S = True
        if self.CD.breaks == True:
                self.CD.breaks = False
        self.aggiornauc()

    def stop(self):
        """
        Mette la variabile Start (S) ad 0, cioe' False
        """
        self.CD.S = False
        self.aggiornauc()

    def setnstep(self):
        """
        Setta, in base al valore passato, il numero di cicli da eseguire
        """
        temp = askinteger("Num Step", "Numero di step da eseguire", initialvalue = 1, minvalue = 1, parent = self.root)
        if temp is None:
            self.CD.setnstep(1)
        else:
            self.CD.setnstep(temp)
            self.labelnstep.config(text = self.CD.nstep)

    def setdelay(self):
        """
        Setta, in base al valore passato, il ritardo di esecuzione.
        Il valore è espresso in millisecondi, di default = 1000
        """
        temp = askinteger("Set Delay", "Ritardo in millisecondi", initialvalue = 100, minvalue = 1, parent = self.root)
        if temp is not None:
            self.delay = temp
            self.labeldelay.config(text = self.delay)
    
    def breakpoint(self):
        """
        Setta o elimina i breakpoint dal programma caricato in memoria
        """
        temp = askstring("Cella di memoria", "Indirizzo esadecimale",parent = self.root)
        if temp is not None:
            temp = self.CD.binario(int(temp,16)).zfill(12)
            self.CD.breakpoint(temp)
            self.aggiornaram()
    
    def exit(self):
        """
        Esce dal programma
        """
        if askquestion('Exit','Sicuro di voler uscire?', parent = self.master) == YES:
            self.codice.master.quit()
            self.codice.master.destroy()
        else:
            showinfo('Suggerimento', """Forse e' meglio fare una pausa!""", icon = WARNING, parent = self.master)
