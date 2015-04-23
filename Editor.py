# -*- coding: utf-8 -*-


from Tkinter import LabelFrame, Scrollbar, Menu, Text,\
    RIDGE, W, E, N, S, WORD, INSERT, END, HORIZONTAL
from tkFileDialog import askopenfilename, asksaveasfilename
from tkMessageBox import askquestion, showinfo, YES, WARNING


class Editor(object):

    """
    Finestra per l'editor di condice assembly
    """

    def __init__(self, master, calcolatore):
        """
        Inizializza i frame della finestra dell'Editor
        """
        self.master = master
        self.CD = calcolatore
        # Codice Assembly
        self.codice = LabelFrame(
            self.master, text='Codice Assembly', relief=RIDGE, borderwidth=5, labelanchor='n', pady=5)
        self.codice.rowconfigure(0, weight=1)
        self.codice.columnconfigure(0, weight=1)
        self.codice.grid(
            row=1, column=0, rowspan=3, columnspan=5, sticky=W + E + N + S)

        self.menubar = Menu(self.master)
        self.create_widgets(self.menubar)

    def create_widgets(self, menubar):
        """
        Crea il layout del programma, finestra dell'Editor
        """
        # Menu
        self.filemenu = Menu(menubar, tearoff=0)
        self.filemenu.add_command(label='Apri', command=self.aprifile)
        self.filemenu.add_command(label='Salva', command=self.salvafile)
        self.filemenu.add_command(label='Cancella', command=self.cancella)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Esci', command=self.exit)
        menubar.add_cascade(label='Opzioni', menu=self.filemenu)
        self.master.config(menu=self.menubar)

        self.helpmenu = Menu(menubar, tearoff=0)
        self.helpmenu.add_command(label='Informazioni', command=self.infor)
        self.helpmenu.add_command(label='Legenda', command=self.leg)
        self.helpmenu.add_command(label='Guida', command=self.guida)
        menubar.add_cascade(label='Aiuto', menu=self.helpmenu)

        # Codice Assembly
        self.Inserisci = Text(self.codice, width=50, height=30, wrap=WORD)
        self.Inserisciscrollbar = Scrollbar(self.codice)
        self.Inserisciscrollbar.config(command=self.Inserisci.yview)
        self.Inserisci.config(yscrollcommand=self.Inserisciscrollbar.set)
        self.Inserisciscrollbar.grid(row=0, column=1, sticky=N + S)
        self.Inserisci.grid(row=0, column=0, sticky=W)

    def exit(self):
        """
        Esce dal programma
        """
        if askquestion('Exit', 'Sicuro di voler uscire?') == YES:
            self.master.quit()
            self.master.destroy()
        else:
            showinfo(
                'Suggerimento', """Forse e' meglio fare una pausa!""", icon=WARNING)

    def aprifile(self):
        """
        Apre un file assembly e lo mostra a video per essere modificato
        """
        path = askopenfilename(title='Apri codice assembly',
                               filetypes=[('Assembly', '.asm'), ('Testo', '.txt'), ('All', '*')])
        if path != '':
            file = open(path, 'r')
            temp = file.read()
            self.Inserisci.delete(1.0, END)
            self.Inserisci.insert(INSERT, temp.decode('ascii', 'ignore'))
            file.close()

    def cancella(self):
        """
        Cancella l'attuale file assembly caricato
        """
        if askquestion('Cancella', 'Si vuole cancellare tutto il codice assembly?') == YES:
            self.Inserisci.delete(1.0, END)

    def salvafile(self):
        """
        Salva il file assembly su cui si sta lavorando
        """
        contenuto = self.Inserisci.get(1.0, END)
        contenuto = contenuto.encode('ascii', 'ignore')
        path = asksaveasfilename(title='Salva codice assembly',
                                 defaultextension=[
                                     ('Assembly', '.asm'), ('Testo', '.txt'), ('All', '*')],
                                 filetypes=[('Assembly', '.asm'), ('Testo', '.txt'), ('All', '*')])

        print path
        if path != '':
            file = open(path, 'w')
            file.write(str(contenuto))
            file.close()

    @staticmethod
    def infor():
        """
        Visualizza le informazioni riguardante il programma
        """
        nome = """pdp8 emulator"""
        stringa = """
    Pdp8 Emulator
    
    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    Version = 1.6.2
    
    Tested with = python 2.6 & 2.7
    -------------------------------------------------------------------
        
    The MIT License (MIT)

    Copyright (c) 2015 Mirco

    Permission is hereby granted, free of charge, to any person 
    obtaining a copy of this software and associated documentation 
    files (the "Software"), to deal in the Software without 
    restriction, including without limitation the rights to use, 
    copy, modify, merge, publish, distribute, sublicense, and/or 
    sell copies of the Software, and to permit persons to whom the 
    Software is furnished to do so, subject to the following 
    conditions:

    The above copyright notice and this permission notice shall 
    be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
    KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
    OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
    -------------------------------------------------------------------
        
    Contact: m.tracolli@gmail.com

    Collaborators : Walter Valentini
    """
        showinfo(nome, stringa)

    @staticmethod
    def leg():
        """
        Visualizza le informazioni riguardanti colori
        """
        nome = """pdp8 Legenda"""
        stringa = """
        Rosso = indirizzo puntato da PC
        Giallo = indirizzo puntato da MAR
        Verde = ultima istruzione eseguita
        """
        showinfo(nome, stringa)

    @staticmethod
    def guida():
        """
        Piccola guida
        """
        nome = """pdp8 Guida"""
        stringa = """
    LOAD = Carica il assembly nella memoria del Calcolatore
            Didattico (CD).
    
    STEP = Avanza del numero di step indicato (di default 1).
            Uno step equivale all'esecuzione di una singola istruzione.
    
    mini STEP = Esegue un singolo ciclo in base alle variabili
            F ed R dell'unità di controllo.
            
    micro STEP = Esegue ogni singola microistruzione.
            
    Set n STEP = Setta il numero di step.
        
    Set Delay = Setta il tempo di aggiornamento del CD.
        
    START = Avvia il CD, ma non l'esecuzione del codice. Per
            eseguire il codice, utilizzare step o esegui una
            volta avviata la macchina.
            
    RESET = Resetta il CD allo stato iniziale.
        
    STOP = Ferma il CD e quindi anche l'esecuzione del codice.
    
    BREAK = Aggiunge o toglie un break alla cella indicata
            in esadecimale.
    
    CONTINUA = Continua l'esecuzione del programma dopo un break.
               Equivale a premere in sequenza START ed ESEGUI.
            
    ESEGUI = Esegue il codice fino all'istruzione HLT, che
            arresta la macchina.
        """
        showinfo(nome, stringa)
