/ Scifta di 10 posizioni OP e le cifre meno significative di OP vanno a finire
/ nelle cifre più significative di RIS
/ Soluzione OP = 0010110000000000
/ Soluzione RIS = 0000000101000000
ORG 100
LOP, CLE
LDA OP
CIL
STA OP
LDA RIS
CIR
STA RIS
ISZ CNT
BUN LOP
HLT
OP, HEX A00B
CNT, DEC -10
RIS, DEC 0
END
