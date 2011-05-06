/ programma per l'ordinamento dei numeri memorizzati a partire

/ dalla parola di memoria 0. Attualmente il programma ordina

/ 10 numeri (comprendendo anche l'istruzione iniziale BUN come

/ numero da considerare nell'insieme da ordinare)

/ Se si vuole modificare il numero di interi da ordinare N

/ bisogna modificare la prima istruzione con 

/ BUN [N in esadecimale], e le inizializzazioni di 

/ COUNT (-N), IND (N) e TIME (-N)

        

ORG 0


	BUN A

	DEC 1

	DEC 3

	DEC 0

	DEC 34

	DEC 3

	DEC 5

	DEC 1

	DEC 8

	DEC 15



START2, LDA MAX

	STA OUTMIN

	LDA TIME

	STA COUNT


	BSA MIN512

	LDA OUTIND

	STA IN1SWAP

	LDA IND

	ADD TIME

	STA IN2SWAP

	BSA SWAP

	ISZ TIME

	BUN START2

	HLT

TIME,	DEC -10

MAX,	HEX 7FFF




MIN512,	DEC 0
START, 	LDA OUTMIN
	STA IN1SUB
        BSA ADDR
        STA IN2SUB
	BSA SUB
        SPA

	BUN NOMIN
        BSA UPD
NOMIN,	ISZ COUNT
	BUN START
	BUN MIN512 I
COUNT,  DEC -10
IND,    DEC 10
TMP,    DEC 0 
OUTMIN,	HEX 7FFF

OUTIND, DEC 0

UPD, 	DEC 0

        LDA IN2SUB
        STA OUTMIN
        LDA TMP

	STA OUTIND                
        BUN UPD I

ADDR,   DEC 0
        LDA COUNT
        ADD IND
        STA TMP
        LDA TMP I
        BUN ADDR I

SUB,	DEC 0	
	LDA IN2SUB
	CMA
	INC
	ADD IN1SUB
	STA OUTSUB
	BUN SUB I
IN1SUB,	DEC 0
IN2SUB,	DEC 0
OUTSUB, DEC 0

SWAP,	DEC 0

	LDA IN1SWAP I

	STA TEMP

	LDA IN2SWAP I

	STA IN1SWAP I

	LDA TEMP

	STA IN2SWAP I

	BUN SWAP I

IN1SWAP,DEC 0

IN2SWAP,DEC 0

TEMP,	DEC 0

        END

