ORG 100

BSA SEARCH
IN_STRING, STRING
IN_CHAR, DEC 88
OUT, DEC 0
HLT

SEARCH, HEX 0
LDA SEARCH I
STA P
ISZ SEARCH
LDA SEARCH I
STA CHAR
ISZ SEARCH
BUN LOOP
// DATA
P, HEX 0
COUNT, HEX 0
CHAR, DEC 0
LOOP, LDA P I
// fine stringa
SZA
BUN CHECK
BUN FINE
// controlla carattere
CHECK, CMA
INC
ADD CHAR
SZA
BUN NEXT

ISZ COUNT

NEXT, ISZ P
BUN LOOP

FINE, 
LDA COUNT
STA SEARCH I
ISZ SEARCH
BUN SEARCH I


STRING, DEC 94
DEC 88
DEC 68
DEC 67
DEC 88
DEC 88
DEC 9
DEC 0

END