# -*- coding: utf-8 -*-


import sys
import tkinter.simpledialog as simpledialog
from tkinter.messagebox import showwarning, showerror


class pdp8(object):
    """
    Calcolatore didattico pdp8
    """

    def __init__(self, codice=None):
        """
        Inizializza i registri e le variabili di controllo S,F ed R
        """
        self.PC = "000000000000"
        self.I = "0"
        self.OPR = "000"
        self.E = "0"
        self.AC = "0000000000000000"
        self.MAR = "000000000000"
        self.MBR = "0000000000000000"
        self.S = False
        self.F = False
        self.R = False
        self.Interrupt = True
        self.START = "0"
        self.RAM = {}
        self.LABEL = {}
        self.BREAKP = {}
        self.breaks = False
        self.tempo = 0
        self.nstep = 1
        self.microistruzioni = ""
        self.inout = ""
        self.nextistr = ""
        self.previstr = ""
        self.halt = False
        self.Opcodes = {
            "CLA": "0111100000000000",
            "CLE": "0111010000000000",
            "CMA": "0111001000000000",
            "CME": "0111000100000000",
            "CIR": "0111000010000000",
            "CIL": "0111000001000000",
            "INC": "0111000000100000",
            "SPA": "0111000000010000",
            "SNA": "0111000000001000",
            "SZA": "0111000000000100",
            "SZE": "0111000000000010",
            "HLT": "0111000000000001",
            "INP": "1111100000000000",
            "OUT": "1111010000000000",
            "SKI": "1111001000000000",
            "SKO": "1111000100000000",
            "ION": "1111000010000000",
            "IOF": "1111000001000000",
            "AND": "000",
            "ADD": "001",
            "LDA": "010",
            "STA": "011",
            "BUN": "100",
            "BSA": "101",
            "ISZ": "110",
        }
        if codice is not None:
            self.carica(codice.lstrip())

    def breakpoint(self, stringa):
        """
        Aggiunge o toglie un breakpoint alla cella di memoria passata
        """
        if stringa in self.BREAKP:
            if self.BREAKP[stringa] == False:
                self.BREAKP[stringa] = True
            else:
                self.BREAKP[stringa] = False
        else:
            print("\n!!! ERROR : Cella di memoria non presente !!!\n")

    def step(self, root=None, codice=None):
        """
        Uno step equivale all'esecuzione dei seguenti cicli:
            - ciclo di fetch
            - ciclo di indirizzamento indiretto (se necessario)
            - ciclo di esecuzione
            - ciclo di interruzione (se necessario)
        """
        try:
            self.breaks = False
            if not self.F and not self.R:
                self.fetch()
            elif not self.F and self.R:
                self.indind()
            elif self.F and not self.R:
                self.execute()
            elif self.F and self.R:
                self.interrupt(root)
            if self.breaks:
                self.S = False
            if self.tempo < 3:
                self.tempo += 1
            else:
                self.tempo = 0
        except Exception as e:
            showwarning(
                "Attenzione", "Controllare il codice assembly!", parent=codice.master
            )
            showerror("Errore", f"{e}", parent=codice.master)
            self.S = False

    def interrupt(self, root):
        """
        Input da tastiera ed output su video di caratteri ASCII (da 0 a 127)
        """
        if self.MBR == self.Opcodes["INP"] and self.Interrupt:  # INP
            if self.tempo == 0:
                self.microistruzioni += "\n"
                self.microistruzioni += "INP --- \n"
                self.microistruzioni += "NOP \n"
            elif self.tempo == 1:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 2:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 3:
                temp = ""
                to = 128
                while len(temp) != 1 or to > 127 and temp == None:
                    if root != None:
                        temp = simpledialog.askstring("Inserisci", "CHAR", parent=root)
                    else:
                        temp = str(input("Inserisci un carattere"))
                    if len(temp) == 1:
                        to = ord(temp)
                    elif temp == "":
                        to = ord(chr(13))  ## Ritorno carrello
                        break
                self.AC = self.binario(to).zfill(16)
                self.F = False
                self.R = False
                self.microistruzioni += "F<- 0 , R <- 0 \n"
                self.microistruzioni += "----- \n"
        elif self.MBR == self.Opcodes["OUT"] and self.Interrupt:  # OUT
            if self.tempo == 0:
                self.microistruzioni += "\n"
                self.microistruzioni += "OUT --- \n"
                self.microistruzioni += "NOP \n"
            elif self.tempo == 1:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 2:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 3:
                temp = chr(int(self.AC, 2))
                if temp == "\r":
                    temp = "\n"
                self.inout += temp
                self.F = False
                self.R = False
                self.microistruzioni += "F<- 0 , R <- 0 \n"
                self.microistruzioni += "----- \n"
        elif self.MBR == self.Opcodes["ION"]:
            if self.tempo == 0:
                self.microistruzioni += "\n"
                self.microistruzioni += "ION --- \n"
                self.microistruzioni += "NOP \n"
            elif self.tempo == 1:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 2:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 3:
                self.Interrupt = True
                self.F = False
                self.R = False
                self.microistruzioni += "F<- 0 , R <- 0 \n"
                self.microistruzioni += "----- \n"
        elif self.MBR == self.Opcodes["IOF"]:
            if self.tempo == 0:
                self.microistruzioni += "\n"
                self.microistruzioni += "IOF --- \n"
                self.microistruzioni += "NOP \n"
            elif self.tempo == 1:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 2:
                self.microistruzioni += "NOP \n"
            elif self.tempo == 3:
                self.Interrupt = False
                self.F = False
                self.R = False
                self.microistruzioni += "F<- 0 , R <- 0 \n"
                self.microistruzioni += "----- \n"
        else:
            self.F = False
            self.R = False

    def _HLT(self):
        """
        Arresta il sistema
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec HLT --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            self.S = False
            self.microistruzioni += "S<- 0 \n"
            self.microistruzioni += "----- \n"

    def _AND(self):
        """
        And logico tra AC e la cella indirizzata
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec AND : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) \n"
        elif self.tempo == 1:
            self.MBR = self.RAM[self.MAR]
            self.microistruzioni += "MBR <- M \n"
        elif self.tempo == 2:
            temp = ""
            for x in range(0, len(self.AC)):
                temp += self.strand(self.AC[x], self.MBR[x])
            self.AC = temp
            self.microistruzioni += "AC <- AC AND MBR \n"
        elif self.tempo == 3:
            self.F = False
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _LDA(self):
        """
        Carica in AC il contenuto della cella indirizzata
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec LDA : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) \n"
        elif self.tempo == 1:
            self.AC = "000000000000000"
            self.MBR = self.RAM[self.MAR]
            self.microistruzioni += "MBR <- M, AC <- 0 \n"
        elif self.tempo == 2:
            self.AC = self.binario(
                self.range(int(self.AC, 2) + self.range(int(self.MBR, 2)))
            ).zfill(16)
            self.microistruzioni += "AC <- AC + MBR \n"
        elif self.tempo == 3:
            self.F = False
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _STA(self):
        """
        Salva nella cella indirizzata il contenuto di AC
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec STA : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) \n"
        elif self.tempo == 1:
            self.MBR = self.AC
            self.microistruzioni += "MBR <- AC \n"
        elif self.tempo == 2:
            self.RAM[self.MAR] = self.MBR
            self.microistruzioni += "M <- MBR \n"
        elif self.tempo == 3:
            self.F = False
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _BUN(self):
        """
        Salto incondizionato alla cella idirizzata
        """
        if self.tempo == 0:
            self.PC = self.MBR[4:]
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec BUN : --- \n"
            self.microistruzioni += "PC <- MBR(AD) \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            self.F = False
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _BSA(self):
        """
        Salvataggio del PC nella cella indirizzata e salto alla cella
        successiva a quella indirizzata
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            temp = self.MBR[:4]
            temp += self.PC
            self.MBR = temp
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec BSA : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) , MBR(AD) <- PC \n"
        elif self.tempo == 1:
            self.RAM[self.MAR] = self.MBR
            self.microistruzioni += "M <- MBR \n"
        elif self.tempo == 2:
            temp = self.range(int(self.MAR, 2)) + 1
            self.PC = self.binario(temp).zfill(12)
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.microistruzioni += "PC <- MAR+1 \n"
        elif self.tempo == 3:
            self.F = False
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _ISZ(self):
        """
        Incrementa di 1 il contenuto della cella indirizzata e se il
        risultato è 0, salta l'istruzione successiva
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec ISZ : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) \n"
        elif self.tempo == 1:
            self.MBR = self.RAM[self.MAR]
            self.microistruzioni += "MBR <- M \n"
        elif self.tempo == 2:
            temp = self.range(int(self.MBR, 2)) + 1
            self.MBR = self.binario(self.range(temp)).zfill(16)
            self.microistruzioni += "MBR <- MBR + 1 \n"
        elif self.tempo == 3:
            self.RAM[self.MAR] = self.MBR
            if int(self.MBR, 2) == 0:
                temp = int(self.PC, 2)
                temp += 1
                self.PC = self.binario(temp).zfill(12)
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.F = False
            if int(self.MBR, 2) == 0:
                self.microistruzioni += "PC <- PC + 1 , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _INC(self):
        """
        Incrementa di 1 il contenuto di AC esteso con E
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec INC : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            temp = self.binario(self.range(int(self.E + self.AC, 2)) + 1)
            if len(temp) == 17:
                self.E = temp[0]
                self.AC = temp[1:]
            else:
                self.AC = temp.zfill(16)
            self.F = False
            self.microistruzioni += "E-AC <- E-AC + 1 , "
            self.microistruzioni += "F<- 0 \n"
            self.microistruzioni += "----- \n"

    def _ADD(self):
        """
        Somma tra AC e la cella indirizzata, con la segnalazione di overflow tramite il registro E
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec ADD : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) \n"
        elif self.tempo == 1:
            self.MBR = self.RAM[self.MAR]
            self.microistruzioni += "MBR <- M \n"
        elif self.tempo == 2:
            temp = int(self.AC, 2) + int(self.MBR, 2)
            if temp > 0:
                temp = bin(temp)[2:].zfill(17)
            else:
                temp = bin(temp)[3:].zfill(17)
            if (self.AC[0] == "1" and self.MBR[0] == "1" and int(temp, 2) < 98304) or (
                self.AC[0] == "0" and self.MBR[0] == "0" and int(temp, 2) > 32767
            ):
                self.E = "1"
            self.AC = temp[1:]
            self.microistruzioni += "E-AC <- AC + MBR \n"
        elif self.tempo == 3:
            self.F = False
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _CLA(self):
        """
        Azzera il contenuto dell'accumulatore AC
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec CLA : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            self.AC = "0000000000000000"
            self.F = False
            self.microistruzioni += "AC <- 0 , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _CLE(self):
        """
        Azzera il contenuto del registro E
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec CLE : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            self.E = "0"
            self.F = False
            self.microistruzioni += "E <- 0 , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _CMA(self):
        """
        Complementa logicamente il contenuto dell'accumulatore AC
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec CMA : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            temp = ""
            for x in range(0, len(self.AC)):
                if self.AC[x] == "0":
                    temp += "1"
                else:
                    temp += "0"
            self.AC = temp
            self.F = False
            self.microistruzioni += "AC <- AC' , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _CME(self):
        """
        Complementa logicamente il contenuto del registro E
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec CME : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            if self.E == "0":
                self.E = "1"
            else:
                self.E = "0"
            self.F = False
            self.microistruzioni += "E <- E' , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _CIR(self):
        """
        Sposta verso destra i bit in E-AC
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec CIR : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            tempe = self.E
            tempac = self.AC
            self.E = tempac[-1]
            self.AC = tempe + tempac[:-1]
            self.F = False
            self.microistruzioni += "E-AC <- bit1 - E - (AC \ bit1) , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _CIL(self):
        """
        Sposta verso sinistra i bit in E-AC
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec CIL : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            tempe = self.E
            tempac = self.AC
            self.E = tempac[0]
            self.AC = tempac[1:] + tempe
            self.F = False
            self.microistruzioni += "E-AC <- AC-E , "
            self.microistruzioni += "F<- 0 \n"
            self.microistruzioni += "----- \n"

    def _SPA(self):
        """
        Salta l'istruzione successiva se il contenuto di AC è positivo o pari a 0
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec SPA : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            if self.AC[0] == "0":
                tp = int(self.PC, 2) + 1
                self.PC = self.binario(tp).zfill(12)
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.F = False
            self.microistruzioni += "if(AC(1)=0) : PC <- PC+1 , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _SNA(self):
        """
        Salta l'istruzione successiva se il contenuto di AC < 0
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec SNA : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            temp = self.range(int(self.AC, 2))
            if temp < 0:
                tp = int(self.PC, 2) + 1
                self.PC = self.binario(tp).zfill(12)
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.F = False
            self.microistruzioni += "if(AC<0) : PC <- PC+1 , "
            self.microistruzioni += "F<- 0 \n"
            self.microistruzioni += "----- \n"

    def _SZA(self):
        """
        Salta l'istruzione successiva se il contenuto di AC = 0
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec SZA : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            temp = self.range(int(self.AC, 2))
            if temp == 0:
                tp = int(self.PC, 2) + 1
                self.PC = self.binario(tp).zfill(12)
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.F = False
            self.microistruzioni += "if(AC=0) : PC <- PC+1 , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def _SZE(self):
        """
        Salta l'istruzione successiva se il contenuto di E = 0
        """
        if self.tempo == 0:
            self.microistruzioni += "\n"
            self.microistruzioni += "Exec SZE : --- \n"
            self.microistruzioni += "NOP \n"
        elif self.tempo == 1:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            if self.E == "0":
                tp = int(self.PC, 2) + 1
                self.PC = self.binario(tp).zfill(12)
            line = 0
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            self.F = False
            self.microistruzioni += "if(E=0) : PC <- PC+1 , "
            self.microistruzioni += "F <- 0 \n"
            self.microistruzioni += "----- \n"

    def execute(self):
        """
        Esecuzione dell'operazione. Se non presente, F torna a 0 per
        eseguire il fetch dell'istruzione successiva.
        """
        if self.I == "1" and self.OPR == "111":
            self.R = True
        elif self.I == "0" and self.OPR == "111":
            if self.MBR == self.Opcodes["HLT"]:
                self._HLT()
            elif self.MBR == self.Opcodes["CLA"]:
                self._CLA()
            elif self.MBR == self.Opcodes["CLE"]:
                self._CLE()
            elif self.MBR == self.Opcodes["CMA"]:
                self._CMA()
            elif self.MBR == self.Opcodes["CME"]:
                self._CME()
            elif self.MBR == self.Opcodes["CIR"]:
                self._CIR()
            elif self.MBR == self.Opcodes["CIL"]:
                self._CIL()
            elif self.MBR == self.Opcodes["INC"]:
                self._INC()
            elif self.MBR == self.Opcodes["SPA"]:
                self._SPA()
            elif self.MBR == self.Opcodes["SNA"]:
                self._SNA()
            elif self.MBR == self.Opcodes["SZA"]:
                self._SZA()
            elif self.MBR == self.Opcodes["SZE"]:
                self._SZE()
        else:
            if self.OPR == self.Opcodes["AND"]:
                self._AND()
            elif self.OPR == self.Opcodes["ADD"]:
                self._ADD()
            elif self.OPR == self.Opcodes["LDA"]:
                self._LDA()
            elif self.OPR == self.Opcodes["STA"]:
                self._STA()
            elif self.OPR == self.Opcodes["BUN"]:
                self._BUN()
            elif self.OPR == self.Opcodes["BSA"]:
                self._BSA()
            elif self.OPR == self.Opcodes["ISZ"]:
                self._ISZ()
            else:
                self.F = False

    def indind(self):
        """
        Ciclo di indirizzamento indiretto
        """
        if self.tempo == 0:
            self.MAR = self.MBR[4:]
            self.microistruzioni += "\n"
            self.microistruzioni += "Indirizzamento indiretto : --- \n"
            self.microistruzioni += "MAR <- MBR(AD) \n"
        elif self.tempo == 1:
            self.MBR = self.RAM[self.MAR]
            self.microistruzioni += "MBR <- M \n"
        elif self.tempo == 2:
            self.microistruzioni += "NOP \n"
        elif self.tempo == 3:
            self.F = True
            self.R = False
            self.microistruzioni += "F <- 1 , R <- 0 \n"
            self.microistruzioni += "----- \n"

    def fetch(self):
        """
        Ciclo di fetch
        """
        if self.tempo == 0:
            if self.BREAKP[self.PC] == True:
                self.breaks = True
            self.MAR = self.PC
            line = 1
            for x in sorted(self.RAM):
                if x == self.PC:
                    self.nextistr = line
                    break
                line += 1
            if int(self.PC, 2) == self.START:
                self.previstr = self.nextistr - 1
            self.microistruzioni += "\n"
            self.microistruzioni += (
                "++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            )
            self.microistruzioni += "Fetch :  \n"
            self.microistruzioni += "MAR <- PC \n"
        elif self.tempo == 1:
            temp = int(self.PC, 2)
            temp += 1
            self.PC = self.binario(temp).zfill(12)
            self.MBR = self.RAM[self.MAR]
            self.microistruzioni += "MBR <- M , PC <- PC+1 \n"
        elif self.tempo == 2:
            self.OPR = self.MBR[1:4]
            self.I = self.MBR[0]
            self.microistruzioni += "OPR <- MBR(OP) , I <- MBR(I) \n"
        elif self.tempo == 3:
            if self.I == "1" and self.OPR != "111":
                self.R = True
                self.microistruzioni += "R <- 1 \n"
            else:
                self.F = True
                self.microistruzioni += "F <- 1 \n"

    def carica(self, codice, master):
        """
        Carica il codice assembly in memoria.
        Non si conta l'ultimo END, che corrisponde al fine programma.
        La funzione ritorna 1 se il caricamento va a buon fine, None altrimenti.
        """
        self.halt = False  # warning se l'istruzione HLT non viene trovata

        temp = codice.rstrip()
        temp = temp.split("\n")
        for x in range(0, len(temp)):
            temp[x] = self.purgestr(temp[x])
        self.purge(temp)
        cod = []

        ### elimino commenti
        for x in temp:
            var = x.split("/")
            cod.append(var[0].rstrip())

        self.purge(cod)
        ### START
        temp = cod[0].split()
        tempRAM = {}

        if temp[0] == "ORG":
            if int(str(temp[1]), 16) > -1 and int(str(temp[1]), 16) < 4096:
                self.START = int(str(temp[1]), 16)
                self.PC = self.binario(self.START).zfill(12)
                cod.pop(0)
            else:
                showwarning(
                    "Errore di caricamento",
                    "ORG di inizio file non corretto",
                    parent=master.codice.master,
                )
                return None
        else:
            self.START = 0
            self.PC = self.binario(self.START).zfill(12)

        ### Elimino END
        try:
            end = cod.index("END")
            if end == len(cod) - 1:
                cod.pop(end)
                self.purge(cod)
            else:
                raise Exception
        except Exception:
            showwarning(
                "Errore di caricamento",
                "Fine codice (END) non trovato!",
                parent=master.codice.master,
            )
            return None

        origin = self.START
        count = 0
        ### RAM temporanea
        for x in range(0, len(cod)):
            temp = cod[x]
            if temp[:3] == "ORG":
                tt = temp.split()
                if int(str(tt[1]), 16) < 4096 and int(str(tt[1]), 16) > -1:
                    self.START = int(str(tt[1]), 16)
                    count = 0
                    continue
                else:
                    showwarning(
                        "Errore di caricamento",
                        "ORG non corretto",
                        parent=master.codice.master,
                    )
                    return None
            tempRAM[self.START + count] = temp
            count += 1

        self.START = origin
        ### LABEL
        for x, y in sorted(tempRAM.items()):
            if y.find(",") >= 0:
                temp = y.split(",")
                self.purge(temp)
                self.LABEL[self.purgestr(temp[0].lstrip())] = self.binario(x).zfill(12)
                tempRAM[x] = temp[1]

        ### RAM
        for x, y in sorted(tempRAM.items()):
            self.RAM[self.binario(x).zfill(12)] = y

        ### DEC e HEX e decodifica codici
        try:
            for x, y in sorted(self.RAM.items()):
                temp = y.split(" ")
                self.purge(temp)
                for z in range(0, len(temp)):
                    temp[z] = self.purgestr(temp[z])
                if len(temp) == 0:
                    continue
                elif temp[0].lstrip() == "DEC":
                    self.RAM[x] = self.binario(self.range(int(temp[1]))).zfill(16)
                elif temp[0] == "HEX":
                    self.RAM[x] = self.binario(self.range(int(temp[1], 16))).zfill(16)
                elif len(temp) == 2:
                    if len(temp[0]) != 3:
                        raise Exception
                    else:
                        self.RAM[x] = "0" + self.decode(temp[0]) + self.decode(temp[1])
                elif len(temp) == 3:
                    if len(temp[0]) != 3:
                        raise Exception
                    else:
                        self.RAM[x] = "1" + self.decode(temp[0]) + self.decode(temp[1])
                else:
                    self.RAM[x] = self.decode(temp[0].lstrip())
        except Exception:
            showwarning(
                "Errore di caricamento",
                "Correggere : " + str(y),
                parent=master.codice.master,
            )
            return None

        for x, y in sorted(self.RAM.items()):
            self.BREAKP[x] = False
            if len(x) > 12 or len(y) > 16:
                return None
            if len(y) != 16:
                self.RAM[x] = y.zfill(16)

        self.nstep = 1

        if not self.halt:
            showwarning(
                "Attenzione !!!",
                """Istruzione assembly HLT non presente!!!
                        \nQuesto può portare ad un errore il programma, per esempio a causa di un ciclo infinito;
                        \nQuindi si potrebbe uscire inaspettatamente dall'applicazione.""",
                parent=master.master,
            )
        return 1

    def decode(self, x):
        """
        Ritorna una stringa binaria corrispondente al comando passato
        """
        if x in self.LABEL:
            return str(self.LABEL[x])
        elif x in self.Opcodes:
            if x == "HLT" and self.halt is False:
                self.halt = True
            return str(self.Opcodes[x])
        else:
            if len(x) != 0:
                return self.binario(self.range(int(str(x), 16))).zfill(12)

    def setnstep(self, n):
        """
        Setta il numero di cicli da eseguire
        """
        self.nstep = n

    def startCD(self):
        """
        Avvia il Calcolatore Didattico
        """
        self.S = True

    def stopCD(self):
        """
        Arresta il calcolatore di dattico
        """
        self.S = False

    def __str__(self):
        """
        Stampa a video lo stato del Calcolatore Didattico
        """
        stringa = ""
        stringa += self.statusRAM()
        stringa += self.statusREG()
        stringa += self.label()
        stringa += self.uc()
        return stringa

    def statusRAM(self):
        """
        Ritorna una stringa con lo stato della RAM
        """
        stringa = ""
        strlabel = ""
        stropcode = ""
        stringa += (
            "Ind BIN"
            + "\t\t"
            + "B"
            + "\t"
            + "Ind HEX"
            + "\t\t"
            + "Cod Istr."
            + "\t\t "
            + "LABEL"
            + "\t"
            + "Opcode"
            + "\t"
            + "Val DEC"
            + "\n"
        )
        stringa += (
            "--------------------------------------------------------------------------------"
            + "\n"
        )
        temp = """%s\t\t%s\t%s\t\t%s\t%s\t\t%s\t%s\n"""
        for x, y in sorted(self.RAM.items()):
            if x in self.BREAKP and self.BREAKP[x]:
                breakpoint = "X"
            else:
                breakpoint = "-"
            for z, t in sorted(self.LABEL.items()):
                if t == x:
                    strlabel = z
                    break
                else:
                    strlabel = ""
            for h, j in sorted(self.Opcodes.items()):
                if j == y[1:4]:
                    stropcode = h
                    break
                elif j == y and (j[:4] == "0111" or j[:4] == "1111"):
                    stropcode = h
                    break
                else:
                    stropcode = ""
            stringa += temp % (
                x,
                breakpoint,
                self.esadecimale(int(str(x), 2)),
                y,
                strlabel,
                stropcode,
                str(self.range(int(y, 2))),
            )
        stringa += (
            "--------------------------------------------------------------------------------"
            + "\n"
        )
        return stringa

    def statusREG(self):
        """
        Ritorna una stringa con lo stato dei registri
        """
        stringa = ""
        stringa += "\n" + "--- REGISTRI ----------------------------" + "\n"
        stringa += "PC\t= " + str(self.PC) + "\n"
        stringa += "I\t= " + str(self.I) + "\tOPR\t= " + str(self.OPR) + "\n"
        stringa += "E\t= " + str(self.E) + "\tAC\t= " + str(self.AC) + "\n"
        stringa += "MAR\t= " + str(self.MAR) + "\n"
        stringa += "MBR\t= " + str(self.MBR) + "\n"
        stringa += "------------------------------------------" "\n"
        return stringa

    def label(self):
        """
        Ritorna una stringa con i label memorizzati
        """
        stringa = ""
        stringa += "\n" + "--- LABELS ------------" + "\n"
        for x, y in sorted(self.LABEL.items()):
            stringa += str(x) + " = " + str(y) + "\n"
        stringa += "-----------------------" "\n"
        return stringa

    def uc(self):
        """
        Ritorna una stringa con lo stato dell'unita' di controllo
        """
        stringa = ""
        stringa += "\n" + "--- UC ------" + "\n"
        stringa += "S =\t" + str(self.S) + "\n"
        stringa += "F =\t" + str(self.F) + "\n"
        stringa += "R =\t" + str(self.R) + "\n"
        stringa += "Int =\t" + str(self.Interrupt) + "\n"
        stringa += "-------------" "\n"
        return stringa

    @staticmethod
    def purge(lista):
        """
        Rimuove dalla lista caratteri indesiderati
        """
        vuoti = lista.count("")
        spazi = lista.count(" ")
        tab = lista.count("\t")
        newline = lista.count("\n")

        for x in range(0, vuoti):
            lista.remove("")
        for x in range(0, spazi):
            lista.remove(" ")
        for x in range(0, tab):
            lista.remove("\t")
        for x in range(0, newline):
            lista.remove("\n")
        for x in range(0, len(lista)):
            lista[x] = lista[x].lstrip()

    @staticmethod
    def purgestr(stringa):
        """
        Rimuove dalla stringa caratteri indesiderati
        """
        stringa = stringa.strip("\t")
        stringa = stringa.strip(" ")
        stringa = stringa.strip("")
        stringa = stringa.strip("\n")
        stringa = stringa.strip("\r")
        return stringa

    @staticmethod
    def range(i):
        """
        Converte i nell'intervallo di rappresentabilità degli interi
        """
        temp = i % 65536
        if i > 32767:
            return temp - 65536
        else:
            return temp

    @staticmethod
    def binario(x):
        """
        Coverte un numero intero in una stringa binaria e
        ritorna una stringa binaria senza '0b' in testa
        """
        if x < 0:
            temp = bin(65536 + x)
        else:
            temp = bin(x)
        return temp[2:]

    @staticmethod
    def esadecimale(x):
        """
        Converte un numero intero in una stringa esadecimale e
        ritorna una stringa esadecimale senza '0x' in testa
        """
        temp = hex(x)
        return temp[2:]

    @staticmethod
    def strand(a, b):
        """
        Ritorna l'and tra i caratteri binari a e b
        """
        if a == "1" and b == "1":
            return "1"
        else:
            return "0"


def run():
    example = """ 	ORG 205
CLA
CLE
ADD 20A
CIR
LOL , STA 20A
AND 418 I
BUN 205
HLT
END
        """
    CD = pdp8(example)


if __name__ == "__main__":
    sys.exit(run())
