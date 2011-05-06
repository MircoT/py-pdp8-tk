ORG 100 / Controlla la parità della parola nella locazione WOD
P, LDA WOD
CIL
STA WOD
SZE
BUN P2
P1, ISZ CNT
BUN P
LDA WOD
CIL
STA WOD
HLT
P2, LDA PAR
CMA
STA PAR
BUN P1
HLT
WOD, HEX 3
CNT, DEC -16
PAR, HEX 0
END
