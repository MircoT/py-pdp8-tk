ORG 100
LDA NUM
STA X
BSA DIV

LDA Q
CMA
INC
STA NUM

BSA PRINT

LDA TMP
STA Y
LDA R
STA X
CLA
STA Q
STA R

BSA DIV

LDA Q
SPA
LDA INITH
STA HEAD
BUN PRINTR

HLT

PRINTR, LDA R
CMA
INC
STA NUM
BSA PRINT
HLT

// Print -----
PRINT, DEC 0
INITP, LDA HEAD I
ADD DIFF
ADD NUM
SZA
BUN AFT
BUN FINEP

AFT, LDA HEAD
INC
STA HEAD
BUN INITP

FINEP, LDA HEAD I
OUT
BUN PRINT I



NUM, DEC 39  / NUM TO PRINT
DIFF, DEC -48
N0, DEC 48
N1, DEC 49
N2, DEC 50
N3, DEC 51
N4, DEC 52
N5, DEC 53
N6, DEC 54
N7, DEC 55
N8, DEC 56
N9, DEC 57
TOT, DEC -10
HEAD, N0
INITH, N0
// -----


DIV, DEC 0
LDA Y
CMA
INC
STA Y
DCICLE, LDA X
ADD Y
SPA
BUN FINED
STA X
BSA INCQ
LDA X
BUN DCICLE

FINED, LDA X
ADD Y
SPA
BUN CHECK
CHECK, SNA
BSA ZERO
LDA X
STA R
BUN DIV I

ZERO, DEC 0
STA R
BSA INCQ
BUN DIV I

INCQ, DEC 0
LDA Q
INC
STA Q
BUN INCQ I

X, DEC 0
Y, DEC 10
TMP, DEC 10
Q, DEC 0
R, DEC 0
BUN DIV I
END