# -*- coding: utf-8 -*-


'''
Created on Jun 23, 2011

@author: Mirco Tracolli
'''
import wx
import wx.stc as stc
from pdp8 import pdp8


class APP(wx.App):

    """
    Classe che rappresenta l'editor dei file assembly
    """

    def OnInit(self):
        """
        Inizializzazione del programma
        """
        self.editor = FileEditorFrame()
        self.emulatorram = FrameEmulatoreram(self.editor)
        self.controlli = FrameEmulatorecontrol(
            self.editor, self.emulatorram.ram)
        self.SetExitOnFrameDelete(True)
        self.editor.Show()
        self.emulatorram.Show()
        self.controlli.Show()
        return True


class FrameEmulatorecontrol(wx.Frame):

    """
    Classe che rappresenta il frame dell'emulatore
    """

    def __init__(self, edit, ram):
        """
        Inizializzazione del frame
        """
        super(FrameEmulatorecontrol, self).__init__(
            edit, -1, title="Pdp8 Emulator : Monitor & Controls", style=wx.DEFAULT_DIALOG_STYLE, size=wx.Size(520, 610))
        icon = wx.Icon("data/logopypdp8small.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.SetMinSize((520, 610))
        self.SetMaxSize((520, 610))
        self.CreateStatusBar()

        self.editor = edit
        self.ram = ram

        # Pannelli
        self.panpulsanti = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)

        # Pulsanti
        self.loadb = wx.Button(self.panpulsanti, 0, 'LOAD')
        self.stepb = wx.Button(self.panpulsanti, 1, 'Step')
        self.ministepb = wx.Button(self.panpulsanti, 2, 'miniStep')
        self.microstepb = wx.Button(self.panpulsanti, 3, 'microStep')
        self.setnstepb = wx.Button(self.panpulsanti, 4, 'Set n Step')
        self.setdelayb = wx.Button(self.panpulsanti, 5, 'Set Delay')
        self.startb = wx.Button(self.panpulsanti, 6, 'START')
        self.resetb = wx.Button(self.panpulsanti, 7, 'RESET')
        self.stopb = wx.Button(self.panpulsanti, 8, 'STOP')
        self.breakb = wx.Button(self.panpulsanti, 9, 'BREAK')
        self.continuab = wx.Button(self.panpulsanti, 10, 'CONTINUA')
        self.eseguib = wx.Button(self.panpulsanti, 11, 'ESEGUI')

        # In/out e microistruzioni
        self.inout = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(265, 100))
        self.inout.SetBackgroundColour("#000000")
        self.inout.SetForegroundColour("#00FF00")
        self.microistr = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(265, 150))
        self.nsteplabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(75, 25))
        self.delaylabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(75, 25))
        self.tempolabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(75, 25))
        self.pclabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(110, 25))
        self.pclabel.SetBackgroundColour("#FF0000")
        self.marlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(110, 25))
        self.marlabel.SetBackgroundColour("#FFFF00")
        self.mbrlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(140, 25))
        self.oprlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(35, 25))
        self.ilabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(25, 25))
        self.elabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(25, 25))
        self.aclabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(140, 25))
        self.acintlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(130, 25))
        self.achexlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(130, 25))
        self.slabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(30, 25))
        self.flabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(45, 25))
        self.rlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(45, 25))
        self.intlabel = wx.TextCtrl(
            self.panpulsanti, style=wx.TE_READONLY, size=(45, 25))

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titolo1 = wx.StaticText(self.panpulsanti, -1, "   IN/OUT")
        titolo1.SetFont(font)
        titolo2 = wx.StaticText(self.panpulsanti, -1, "   Microistruzioni")
        titolo2.SetFont(font)
        titolo3 = wx.StaticText(self.panpulsanti, -1, "     n Step")
        titolo3.SetFont(font)
        titolo4 = wx.StaticText(self.panpulsanti, -1, "      Delay")
        titolo4.SetFont(font)
        titolo5 = wx.StaticText(self.panpulsanti, -1, "      Tempo")
        titolo5.SetFont(font)
        titolo6 = wx.StaticText(self.panpulsanti, -1, "      Registri")
        titolo6.SetFont(font)
        titolo7 = wx.StaticText(self.panpulsanti, -1, " PC   ")
        titolo7.SetFont(font)
        titolo8 = wx.StaticText(self.panpulsanti, -1, " MAR   ")
        titolo8.SetFont(font)
        titolo9 = wx.StaticText(self.panpulsanti, -1, " MBR   ")
        titolo9.SetFont(font)
        titolo10 = wx.StaticText(self.panpulsanti, -1, "         OPR")
        titolo10.SetFont(font)
        titolo11 = wx.StaticText(self.panpulsanti, -1, "           I")
        titolo11.SetFont(font)
        titolo12 = wx.StaticText(self.panpulsanti, -1, "           E")
        titolo12.SetFont(font)
        titolo13 = wx.StaticText(self.panpulsanti, -1, " AC   ")
        titolo13.SetFont(font)
        titolo14 = wx.StaticText(self.panpulsanti, -1, " AC (INT)   ")
        titolo14.SetFont(font)
        titolo15 = wx.StaticText(self.panpulsanti, -1, " AC (HEX)   ")
        titolo15.SetFont(font)
        titolo16 = wx.StaticText(
            self.panpulsanti, -1, "   Unita' di controllo")
        titolo16.SetFont(font)
        titolo17 = wx.StaticText(self.panpulsanti, -1, "           S")
        titolo17.SetFont(font)
        titolo18 = wx.StaticText(self.panpulsanti, -1, "           F")
        titolo18.SetFont(font)
        titolo19 = wx.StaticText(self.panpulsanti, -1, "           R")
        titolo19.SetFont(font)
        titolo20 = wx.StaticText(self.panpulsanti, -1, "        Int.")
        titolo20.SetFont(font)

        # Sizers
        pulhor = wx.GridBagSizer(5, 5)
        pulhor.Add(self.loadb, (0, 0), (1, 1))
        pulhor.Add(self.stepb, (1, 0), (1, 1))
        pulhor.Add(self.ministepb, (1, 1), (1, 1))
        pulhor.Add(self.microstepb, (1, 2), (1, 1))
        pulhor.Add(self.setnstepb, (0, 1), (1, 1))
        pulhor.Add(self.setdelayb, (0, 2), (1, 1))
        pulhor.Add(self.startb, (2, 0), (1, 1))
        pulhor.Add(self.resetb, (2, 1), (1, 1))
        pulhor.Add(self.stopb, (2, 2), (1, 1))
        pulhor.Add(self.breakb, (3, 0), (1, 1))
        pulhor.Add(self.continuab, (3, 1), (1, 1))
        pulhor.Add(self.eseguib, (3, 2), (1, 1))
        pulhor.Add(
            wx.StaticLine(self.panpulsanti, -1, size=(265, 3)), (4, 0), (1, 3))
        pulhor.Add(titolo1, (5, 0), (1, 3))
        pulhor.Add(self.inout, (6, 0), (3, 3))
        pulhor.Add(titolo2, (9, 0), (1, 3))
        pulhor.Add(self.microistr, (10, 0), (3, 3))
        pulhor.Add(titolo3, (13, 0), (1, 1))
        pulhor.Add(self.nsteplabel, (13, 1), (1, 1))
        pulhor.Add(titolo4, (14, 0), (1, 1))
        pulhor.Add(self.delaylabel, (14, 1), (1, 1))
        pulhor.Add(titolo5, (15, 0), (1, 1))
        pulhor.Add(self.tempolabel, (15, 1), (1, 1))
        pulhor.Add(wx.StaticLine(
            self.panpulsanti, -1, size=(3, 545), style=wx.LI_VERTICAL), (0, 4), (16, 1))
        pulhor.Add(titolo6, (0, 5), (1, 3))
        pulhor.Add(self.pclabel, (1, 5), (1, 2))
        pulhor.Add(titolo7, (1, 7), (1, 1))
        pulhor.Add(self.marlabel, (2, 5), (1, 2))
        pulhor.Add(titolo8, (2, 7), (1, 1))
        pulhor.Add(self.mbrlabel, (3, 5), (1, 2))
        pulhor.Add(titolo9, (3, 7), (1, 1))
        pulhor.Add(self.oprlabel, (4, 6), (1, 1))
        pulhor.Add(titolo10, (4, 5), (1, 1))
        pulhor.Add(self.ilabel, (5, 6), (1, 1))
        pulhor.Add(titolo11, (5, 5), (1, 1))
        pulhor.Add(self.elabel, (6, 6), (1, 1))
        pulhor.Add(titolo12, (6, 5), (1, 1))
        pulhor.Add(self.aclabel, (7, 5), (1, 2))
        pulhor.Add(titolo13, (7, 7), (1, 1))
        pulhor.Add(self.acintlabel, (8, 5), (1, 2))
        pulhor.Add(titolo14, (8, 7), (1, 1))
        pulhor.Add(self.achexlabel, (9, 5), (1, 2))
        pulhor.Add(titolo15, (9, 7), (1, 1))
        pulhor.Add(
            wx.StaticLine(self.panpulsanti, -1, size=(200, 3)), (10, 5), (1, 3))
        pulhor.Add(titolo16, (11, 5), (1, 3))
        pulhor.Add(titolo17, (12, 5), (1, 1))
        pulhor.Add(self.slabel, (12, 6), (1, 1))
        pulhor.Add(titolo18, (13, 5), (1, 1))
        pulhor.Add(self.flabel, (13, 6), (1, 1))
        pulhor.Add(titolo19, (14, 5), (1, 1))
        pulhor.Add(self.rlabel, (14, 6), (1, 1))
        pulhor.Add(titolo20, (15, 5), (1, 1))
        pulhor.Add(self.intlabel, (15, 6), (1, 1))

        self.panpulsanti.SetSizer(pulhor)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panpulsanti, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

        # PDP 8
        self.CD = pdp8()
        self.delay = 100
        self.delaylabel.AppendText(str(self.delay))
        self.previstr = -1
        self.last = -1

        # Eventi
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_BUTTON, self.OnLoad, id=0)
        self.Bind(wx.EVT_BUTTON, self.OnStep, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnMiniStep, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnMicroStep, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnSetnStep, id=4)
        self.Bind(wx.EVT_BUTTON, self.OnSetDelay, id=5)
        self.Bind(wx.EVT_BUTTON, self.OnStart, id=6)
        self.Bind(wx.EVT_BUTTON, self.OnReset, id=7)
        self.Bind(wx.EVT_BUTTON, self.OnStop, id=8)
        self.Bind(wx.EVT_BUTTON, self.OnBreak, id=9)
        self.Bind(wx.EVT_BUTTON, self.OnContinua, id=10)
        self.Bind(wx.EVT_BUTTON, self.OnEsegui, id=11)

        # Status Iniziale
        self.OnReset(8)

    def OnBreak(self, event):
        """
        Aggiunge un break nel flusso di esecuzione del programma
        """
        dlg = wx.TextEntryDialog(
            self, "Inserire un indirizzo di memoria in esadecimale", "Breakpoints")
        if dlg.ShowModal() == wx.ID_OK:
            try:
                temp = self.CD.binario(int(dlg.GetValue(), 16)).zfill(12)
                self.CD.indmodifica = temp
                self.CD.breakpoint(temp)
                self.CD.modd = True
                self.AggiornaRAM()
                self.SetStatusText("Breakpoint inserito")
            except Exception:
                wx.MessageBox(
                    "Errore, indirizzo indicato non corretto!", style=wx.ICON_ERROR)
        dlg.Destroy()

    def OnContinua(self, event):
        """
        Riprense l'esecuzione del programma dopo
        un break
        """
        self.CD.startCD()
        self.OnEsegui()
        self.SetStatusText("Ripresa esecuzione dopo un break")

    def OnEsegui(self, event=11):
        """
        Esegue il programma fino all'arresto della macchina tramite
        l'istruzione HLT
        """
        while self.CD.S:
            self.CD.step(self)
            self.CD.microistruzionistep += self.CD.microistruzioni
            if not self.CD.F and not self.CD.R and self.CD.tempo == 0:
                self.previstr = self.last
                self.AggiornaALL()
                self.SetStatusText("Eseguo il programma")
                self.CD.microistruzionistep = ''
                break
        if self.CD.S:
            wx.CallLater(self.delay, self.OnEsegui)
        else:
            self.previstr = self.last
            self.CD.setnstep(1)
            self.SetStatusText("Programma terminato")
            self.AggiornaALL()

    def OnMiniStep(self, event=2):
        """
        Esegue un singolo ciclo della macchina
        """
        if self.CD.S:
            for x in range(0, 4):
                self.CD.step(self)
                self.CD.microistruzionistep += self.CD.microistruzioni
                self.CD.nstep = 1
                self.AggiornaALL()
                self.SetStatusText("Eseguito un miniStep")

    def OnMicroStep(self, event=3):
        """
        Esegue un microstep
        """
        if self.CD.S:
            self.CD.step(self)
            self.CD.microistruzionistep += self.CD.microistruzioni
            self.AggiornaALL()
            self.SetStatusText("Eseguito un microStep")

    def OnStep(self, event=1):
        """
        Esegue uno step
        """
        var = True
        if self.CD.S and self.CD.nstep > 0:
            while var and self.CD.S:
                self.CD.step(self)
                self.CD.microistruzionistep += self.CD.microistruzioni
                if not self.CD.F and not self.CD.R and self.CD.tempo == 0:
                    self.CD.nstep -= 1
                    self.previstr = self.last
                    self.AggiornaALL()
                    self.SetStatusText("Eseguito uno Step")
                    var = False
                    self.CD.microistruzionistep = ''
            if not self.CD.S:
                self.previstr = self.last
            if self.CD.nstep > 0:
                wx.CallLater(self.delay, self.OnStep)
            else:
                self.CD.setnstep(1)
        else:
            self.CD.setnstep(1)
            self.AggiornaALL()

    def OnReset(self, event):
        """
        Resetta il calcolatore didattico
        """
        self.CD = pdp8()
        self.previstr = -1
        self.last = -1
        self.inout.Clear()
        self.microistr.Clear()
        self.AggiornaALL()
        self.SetStatusText("Calcolatore Didattico resettato")

    def OnStop(self, event):
        """
        Spegne la macchina
        """
        self.CD.stopCD()
        self.AggiornaUC()
        self.SetStatusText("La macchina e' stata fermata")

    def OnStart(self, event):
        """
        Accende la macchina
        """
        self.CD.startCD()
        self.AggiornaUC()
        self.SetStatusText("La macchina e' stata avviata")

    def OnSetnStep(self, event):
        """
        Setta il numero di step da eseguire
        """
        dlg = wx.TextEntryDialog(
            self, "Inserire il numero di Step", "n Step", value='1')
        if dlg.ShowModal() == wx.ID_OK:
            try:
                if int(dlg.GetValue()) > 0:
                    self.CD.setnstep(int(dlg.GetValue()))
                    self.SetStatusText("Settato numero di step")
                else:
                    wx.MessageBox(
                        "Errore, numero step non corretto", style=wx.ICON_ERROR)
            except ValueError:
                wx.MessageBox(
                    "Errore, numero step non corretto", style=wx.ICON_ERROR)
        self.AggiornaUC()
        dlg.Destroy()

    def OnSetDelay(self, event):
        """
        Setta il tempo di aggiornamento
        """
        dlg = wx.TextEntryDialog(
            self, "Inserisci il tempo di aggiornamento \n Min = 10 millisecondi", "Set Delay", value='100')
        if dlg.ShowModal() == wx.ID_OK:
            try:
                if int(dlg.GetValue()) > 9:
                    self.delay = int(dlg.GetValue())
                    self.SetStatusText("Settato tempo di aggiornamento")
                else:
                    wx.MessageBox(
                        "Errore, tempo di aggiornamento non corretto", style=wx.ICON_ERROR)
            except ValueError:
                wx.MessageBox(
                    "Errore, tempo di aggiornamento non corretto", style=wx.ICON_ERROR)
        self.delaylabel.Clear()
        self.delaylabel.AppendText(str(self.delay))
        dlg.Destroy()

    def OnLoad(self, event):
        """
        Azione del pulsante LOAD
        """
        self.OnReset(event)
        testo = self.editor.testo.GetText()
        if len(testo.lstrip().rstrip()) == 0:
            wx.MessageBox("Nessun file assembly presente nell'editor.",
                          style=wx.CENTER | wx.ICON_EXCLAMATION | wx.OK)
        else:
            self.CD = pdp8()
            var = self.CD.carica(testo)
            if var is 1:
                self.AggiornaALL()
                self.SetStatusText("Caricamento del file assembly effettuato")
            else:
                self.SetStatusText("Errore nel caricamento del file assembly")

    def AggiornaALL(self):
        """
        Aggiorna l'emulatore
        """
        self.AggiornaRAM()
        self.AggiornaREG()
        self.AggiornaUC()
        self.AggiornaINOUTMICRO()

    def AggiornaINOUTMICRO(self):
        """
        Aggiorna il text di input output e
        delle micro-istruzioni
        """
        if self.CD.inout is not None:
            self.inout.AppendText(self.CD.inout)
        if self.CD.microistruzioni != '':
            self.microistr.AppendText(self.CD.microistruzionistep)

    def AggiornaUC(self):
        """
        Aggiorna l'unita' di controllo
        """
        if self.CD.S and not self.CD.breaks:
            self.slabel.SetBackgroundColour('#00FF00')
        elif not self.CD.S and self.CD.breaks:
            self.slabel.SetBackgroundColour('#0000F0')
            self.SetStatusText("Macchina in Pausa")
        else:
            self.slabel.SetBackgroundColour('#FF0000')

        self.flabel.Clear()
        self.rlabel.Clear()
        self.intlabel.Clear()
        self.tempolabel.Clear()
        self.nsteplabel.Clear()
        self.slabel.Clear()
        self.flabel.AppendText(str(int(self.CD.F)))
        self.rlabel.AppendText(str(int(self.CD.R)))
        self.intlabel.AppendText(str(self.CD.Interrupt))
        self.tempolabel.AppendText(str(self.CD.tempo))
        self.nsteplabel.AppendText(str(self.CD.nstep))
        self.slabel.AppendText(str(int(self.CD.S)))

    def AggiornaREG(self):
        """
        Aggiorna i registri
        """
        self.pclabel.Clear()
        self.pclabel.AppendText(self.CD.PC)
        self.marlabel.Clear()
        self.marlabel.AppendText(self.CD.MAR)
        self.mbrlabel.Clear()
        self.mbrlabel.AppendText(self.CD.MBR)
        self.oprlabel.Clear()
        self.oprlabel.AppendText(self.CD.OPR)
        self.ilabel.Clear()
        self.ilabel.AppendText(self.CD.I)
        self.elabel.Clear()
        self.elabel.AppendText(self.CD.E)
        self.aclabel.Clear()
        self.aclabel.AppendText(self.CD.AC)
        self.acintlabel.Clear()
        self.acintlabel.AppendText(str(self.CD.range(int(self.CD.AC, 2))))
        self.achexlabel.Clear()
        self.achexlabel.AppendText(
            str((hex(int(self.CD.AC, 2))[2:].upper())).zfill(4))

    def AggiornaRAM(self):
        """
        Aggiorna la RAM
        """

        for x in range(0, self.ram.GetItemCount()):
            if (255, 255, 255, 255) != self.ram.GetItemBackgroundColour(x):
                self.ram.SetItemBackgroundColour(x, '#FFFFFF')

        # Aggiornamento delle differenza (per evitare sfarfallii)
        if self.ram.GetItemCount() > 0 and len(self.CD.RAM) == self.ram.GetItemCount():
            if self.CD.modd:
                x = self.CD.indmodifica
                y = self.CD.RAM[x]
                for z in range(0, self.ram.GetItemCount()):
                    # Variabili necessarie per l'aggiornamento
                    ind = self.ram.GetItem(z, 0).GetText()
                    con = self.ram.GetItem(z, 3).GetText()
                    # Aggiornamento breakpoint
                    breakpoint = ''
                    if ind == x:
                        if self.CD.BREAKP.has_key(x) and self.CD.BREAKP[x]:
                            breakpoint = 'X'
                        else:
                            breakpoint = '-'
                        self.ram.SetStringItem(z, 1, breakpoint)
                        # Aggiornamento contenuto, opcode e val intero
                        if con != y:
                            stropcode = ''
                            for h, j in sorted(self.CD.Opcodes.iteritems()):
                                if j == y[1:4]:
                                    stropcode = h
                                    break
                                elif j == y and (j[:4] == '0111' or j[:4] == '1111'):
                                    stropcode = h
                                    break
                                else:
                                    stropcode = ''

                            self.ram.SetStringItem(z, 3, y)
                            self.ram.SetStringItem(z, 5, stropcode)
                            self.ram.SetStringItem(
                                z, 6, str(self.CD.range(int(y, 2))))
                            break
                self.CD.modd = False
        else:
            self.ram.DeleteAllItems()
            contenuto = self.CD.statusRAM()
            for x in contenuto:
                self.ram.Append(x)

        # Cerca PC e MAR
        temppc = -1
        tempmar = -2
        for x in range(0, self.ram.GetItemCount()):
            temp = self.ram.GetItem(x, 0).GetText()
            if temp == self.CD.PC:
                temppc = x
            if temp == self.CD.MAR:
                tempmar = x

        try:
            if temppc == tempmar:
                if self.previstr != -1:
                    self.ram.SetItemBackgroundColour(self.previstr, '#00FF00')
                self.ram.SetItemBackgroundColour(temppc, '#C0C0C0')
            elif tempmar == self.previstr:
                self.ram.SetItemBackgroundColour(tempmar, '#00F0F0')
                self.ram.SetItemBackgroundColour(temppc, '#FF0000')
            else:
                if tempmar != -2:
                    self.ram.SetItemBackgroundColour(tempmar, '#FFFF00')
                if self.previstr != -1:
                    self.ram.SetItemBackgroundColour(self.previstr, '#00FF00')
                if temppc != -1:
                    self.ram.SetItemBackgroundColour(temppc, '#FF0000')

        except Exception:
            pass

        self.last = temppc

        if temppc >=0:
            self.ram.EnsureVisible(temppc)

    def OnExit(self, event):
        """
        Chiude l'intero programma
        """
        self.editor.OnExit(event)


class FrameEmulatoreram(wx.Frame):

    """
    Classe che rappresenta il frame dell'emulatore
    """

    def __init__(self, edit):
        """
        Inizializzazione del frame
        """
        super(FrameEmulatoreram, self).__init__(
            edit, -1, title="Pdp8 Emulator : RAM", style=wx.DEFAULT_DIALOG_STYLE, size=(585, 560))
        icon = wx.Icon("data/logopypdp8small.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.SetMinSize((585, 560))
        self.SetMaxSize((600, 600))
        self.CreateStatusBar()
        self.PushStatusText("Info celle RAM : Val HEX | ADD HEX")

        self.editor = edit

        # Pannello
        self.panram = wx.Panel(self)

        # RAM
        self.ram = wx.ListCtrl(self.panram, -1, style=wx.LC_REPORT |
                               wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL, size=(580, 500))
        self.ram.InsertColumn(0, "Ind BIN", wx.LIST_FORMAT_CENTER, 110)
        self.ram.InsertColumn(1, "Break", wx.LIST_FORMAT_CENTER, 50)
        self.ram.InsertColumn(2, "Ind HEX", wx.LIST_FORMAT_CENTER, 65)
        self.ram.InsertColumn(3, "Contenuto BIN", wx.LIST_FORMAT_CENTER, 145)
        self.ram.InsertColumn(4, "LABEL", wx.LIST_FORMAT_CENTER, 60)
        self.ram.InsertColumn(5, "Opcode", wx.LIST_FORMAT_CENTER, 60)
        self.ram.InsertColumn(6, "Val DEC", wx.LIST_FORMAT_CENTER, 70)

        # Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panram, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Eventi
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)

    def OnSelected(self, event):
        """
        Stampa il contenuto in esadecimale dell'indirizzo selezionato
        e la parte indirizzo (ADD = address) del contenuto 
        della cella selezionata
        """
        riga = event.GetIndex()
        contenuto = self.ram.GetItem(riga, 3).GetText()
        self.PushStatusText("Contenuto HEX = " + str(hex(int(contenuto, 2))[2:].upper().zfill(
            4)) + " | ADD (HEX) = " + str(hex(int(contenuto[4:], 2))[2:].upper().zfill(3)))

    def OnExit(self, event):
        """
        Chiude l'intero programma
        """
        self.editor.OnExit(event)


class FileEditorFrame(wx.Frame):

    """
    Classe che rappresenta il frame dell'editor
    """

    def __init__(self):
        """
        Inizializzazione del frame
        """
        super(FileEditorFrame, self).__init__(
            None, -1, "Assembly File Editor", style=wx.CENTER | wx.DEFAULT_FRAME_STYLE)
        icon = wx.Icon("data/logopypdp8small.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.SetMinSize((400, 500))
        self.file = None

        # Testo con marcatura delle parole chiave
        self.testo = stc.StyledTextCtrl(self, id=wx.ID_FILE1, style=0)
        self.testo.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.testo.SetMarginMask(1, 0)
        self.testo.SetMarginWidth(1, 30)

        self.testo.SetKeyWords(
            0, "I ORG END DEC HEX AND ADD LDA STA BUN BSA ISZ CLA CLE CMA CME CIR CIL INC SPA SZA SNA SZE HLT INP OUT ION IOF")
        self.testo.SetLexer(stc.STC_LEX_PYTHON)
        self.testo.SetMarginLeft(5)
        self.Centre()

        car = {'sansm': 'DejaVu Sans Mono',
               'mono': 'CurierNew',
               'serif': 'DejaVu Serif',
               'size': 13,
               'size2': 10
               }

        self.testo.StyleSetSpec(
            stc.STC_P_DEFAULT, "fore:#A0A0A0,face:%(serif)s,size:%(size)d" % car)
        self.testo.StyleSetSpec(
            stc.STC_P_NUMBER, "fore:#E00000,face:%(mono)s,bold,size:%(size2)d" % car)
        self.testo.StyleSetSpec(
            stc.STC_P_WORD, "fore:#0000D0,face:%(mono)s,bold,size:%(size2)d" % car)
        self.testo.StyleSetSpec(
            stc.STC_P_OPERATOR, "fore:#DDAA00,face:%(mono)s,size:%(size)d" % car)
        self.testo.StyleSetSpec(
            stc.STC_STYLE_LINENUMBER, "fore:#696969,face:%(sansm)s,size:%(size2)d" % car)

        # menu
        self._SetupMenus()

        # sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.testo, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Eventi
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.DoSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=wx.ID_HELP)
        self.Bind(wx.EVT_MENU, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnLegenda, id=5)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnAbout(self, event):
        """
        Finestra di dialogo delle informazioni
        """
        info = wx.AboutDialogInfo()

        descrizione = """pdp8Emulator e' un simulatore del calcolatore didattico pdp8 pensato per essere eseguito su qualsiasi sistema operativo e collaudato con python 2.6 & 2.7 e wxPython 2.8.12.0 (gtk2-unicode).
        
Contact: m.tracolli@gmail.com
        
Collaborators : Walter Valentini
        """
        licenza = """The MIT License (MIT)

Copyright (c) 2015 Mirco

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without 
restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE."""
        info.SetIcon(wx.Icon("data/logopypdp8.png", wx.BITMAP_TYPE_PNG))
        info.SetName("pdp8Emulator")
        info.SetVersion("2.0")
        info.SetDescription(descrizione)
        info.SetCopyright("Copyright (C) 2011 Mirco Tracolli")
        info.SetWebSite("http://code.google.com/p/py-pdp8-tk/")
        info.SetLicence(licenza)
        info.AddDeveloper("Mirco Tracolli")
        wx.AboutBox(info)

    def OnLegenda(self, event):
        """
        Finestra di dialogo della legenda
        """
        legenda = """Colore rosso = cella puntata dal PC
        
Colore giallo = cella puntata dal MAR

Colore verde = ultima istruzione eseguita

Colore azzurro = cella puntata dal MAR ed ultima istruzione eseguita coincidono

Colore grigio = cella puntata da MAR e PC coincidono (puo' avvenire in caso di break)

Colore blu su S = Macchina in pausa"""

        wx.MessageBox(legenda, style=wx.CENTER | wx.ICON_INFORMATION | wx.OK)

    def OnHelp(self, event):
        """
        Finestra di dialogo delle istruzioni
        """
        istruzioni = """LOAD = Carica il file assembly nella memoria del Calcolatore Didattico (CD).

STEP = Avanza del numero di step indicato (di default 1). Uno step equivale all'esecuzione di una singola istruzione.

mini STEP = Esegue un singolo ciclo in base alle variabili F ed R dell'unità di controllo.

micro STEP = Esegue ogni singola microistruzione.

Set n STEP = Setta il numero di step.

Set Delay = Setta il tempo di aggiornamento del CD.

START = Avvia il CD, ma non l'esecuzione del codice. Per eseguire il codice, utilizzare step o esegui una volta avviata la macchina.

RESET = Resetta il CD allo stato iniziale (vengono automaticamente azzerati i contenuti dei registri, della memoria e delle variabili di controllo).

STOP = Ferma il CD e quindi anche l'esecuzione del codice.

BREAK = Aggiunge o toglie un break alla cella indicata in esadecimale. La macchina si fermera' quando il PC arrivera' sulla suddetta cella.
Quindi non ha nessun effetto se messo sulla cella che contiene l'indirizzo di ritorno da un sottoprogramma quando si utilizza BSA.

CONTINUA = Continua l'esecuzione del programma dopo un break. Equivale a premere in sequenza START ed ESEGUI.

ESEGUI = Esegue il codice fino all'istruzione HLT, che arresta la macchina."""

        wx.MessageBox(
            istruzioni, style=wx.CENTER | wx.ICON_INFORMATION | wx.OK)

    def _SetupMenus(self):
        """
        Creazione del menu
        """
        menubar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_NEW, "Nuovo\tCtrl+N")
        menu.Append(wx.ID_OPEN, "Apri\tCtrl+O")
        menu.Append(wx.ID_CLEAR, "Cancella testo")
        menu.AppendSeparator()
        menu.Append(wx.ID_SAVE, "Salva\tCtrl+S")
        menu.Append(wx.ID_SAVEAS, "Salva come\tCtrl+Shift+S")
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, "Esci\tCtrl+Q")
        menubar.Append(menu, "Azioni")

        info = wx.Menu()
        info.Append(wx.ID_ABOUT, "pdp8Emulator")
        info.Append(wx.ID_HELP, "Istruzioni")
        info.Append(5, "Legenda")
        menubar.Append(info, "Info")
        self.SetMenuBar(menubar)

    def OnOpen(self, event):
        """
        Gestione dell'apertura dei file
        """
        if event.GetId() == wx.ID_OPEN:
            self.DoOpen()
        else:
            event.Skip()

    def OnSave(self, event):
        """
        Gestione del salvataggio del file aperto
        """
        eventid = event.GetId()
        if eventid == wx.ID_SAVE:
            if self.file:
                self.Save(self.file)
            else:
                self.DoSaveAs(event)
        else:
            event.Skip()

    def OnExit(self, event):
        """
        Gestione dell'uscita dal programma
        """
        if self.testo.GetModify():
            messaggio = (
                "Le ultime modifiche non sono state salvate. \n\n Si vuole salvare il file attuale?")
            stile = wx.YES_NO | wx.ICON_WARNING | wx.CENTER
            risultato = wx.MessageBox(
                messaggio, "Salvare i cambiamenti?", style=stile)

            if risultato == wx.YES:
                if self.file is None:
                    self.DoSaveAs(event)
                else:
                    self.Save(self.file)

        self.DestroyChildren()
        self.Destroy()

    def DoOpen(self):
        """
        Apertura di un file
        """
        tipifile = "Assembly Files (*.asm)|*.asm|File di Testo (*.txt)|*.txt|Tutti i Files (*)|*"
        dialogo = wx.FileDialog(
            self, message="Apri file", wildcard=tipifile, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialogo.ShowModal() == wx.ID_OK:
            percorso = dialogo.GetPath()
            with open(percorso, "rb") as handle:
                testo = handle.read()
                self.testo.ClearAll()
                self.testo.AddText(testo)
                self.file = percorso
                self.testo.SetSavePoint()

        dialogo.Destroy()

    def DoSaveAs(self, event):
        """
        Salvataggio con nome di un file
        """
        tipifile = "Assembly Files (*.asm)|*.asm|File di Testo (*.txt)|*.txt|Tutti i Files (*)|*"
        dialogo = wx.FileDialog(self, message="Salva come", defaultFile=".asm",
                                wildcard=tipifile, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialogo.ShowModal() == wx.ID_OK:
            percorso = dialogo.GetPath()
            self.Save(percorso)
            self.file = percorso
        dialogo.Destroy()

    def Save(self, percorso):
        """
        Salvataggio del file corrente
        """
        with open(percorso, "wb") as handle:
            testo = self.testo.GetText()
            handle.write(testo)
            self.testo.SetSavePoint()

    def OnNew(self, event):
        """
        Crea un nuovo file
        """
        if self.file is not None:
            if self.testo.GetModify():
                messaggio = (
                    "Le ultime modifiche non sono state salvate. \n\n Si vuole salvare il file attuale?")
                stile = wx.YES_NO | wx.ICON_WARNING | wx.CENTER
                risultato = wx.MessageBox(
                    messaggio, "Salvare i cambiamenti?", style=stile)

                if risultato == wx.YES:
                    if self.file is None:
                        self.DoSaveAs(event)
                    else:
                        self.Save(self.file)

        self.file = None
        self.testo.ClearAll()

    def OnClear(self, event):
        """
        Cancella complemtamente il testo visualizzato
        """
        self.testo.ClearAll()
