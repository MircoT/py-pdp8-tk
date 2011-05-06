ORG 100 / Somma (S) tra X e Y e  calcolo del traboccamento (T)
LDA X
ADD Y
STA S
LDA X
CIL
CLA
CIR
ADD Y
SPA
HLT
CLA
CIR
ADD S
SNA
HLT
LDA T
CMA
STA T
HLT
X, HEX 7000
Y, HEX 1000
S, HEX 0
T, HEX 0
END


