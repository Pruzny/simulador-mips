.data

valor: .asciiz "Valor: "
nota: .asciiz "NOTAS:\n"
notaquant: .asciiz " nota(s) de R$ "
moeda: .asciiz "MOEDAS:\n"
moedaquant: .asciiz " moeda(s) de R$ "
resultado: .asciiz "Resultado: "
linha: .asciiz "\n"
notavalor: .double 100, 50, 20, 10, 5, 2
moedavalor: .double 1, 0.5, 0.25, 0.10, 0.05, 0.01
quantidade: .word 6

.text

ADD $V0, $ZERO, $AT
SUB $A1,$V1,$A0
AND $T0,$A2,$A3
TESTE: OR $T3,$T1,$T2
SLL $T6,$T4,31
SRL $S2,$S0,31
JR $T0
ADDI $T8,$S6,-32768
LW $K1,32767($T9)
AEW: SW $FP,-32768($GP)
BEQ $RA,$T7,AEW
BNE $T1,$T2,POW
J TESTE
POW: JAL AEW
