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

li $v0, 4
la $a0, valor
syscall
li $v0, 7
syscall

add.d $f2 $f2 $f0

la $a0, nota
la $a1, notaquant
la $a2, notavalor
jal calculatipo
la $a0, moeda
la $a1, moedaquant
la $a2, moedavalor
jal calculatipo

li $v0, 10
syscall

calculavalor: 
ldc1 $f6, 0($a2)
addi $t4, $zero, 0
LOOP2:
c.lt.d $f2, $f6
bc1t END2
sub.d $f2, $f2, $f6
addi $t4, $t4, 1
j LOOP2
END2:
move $v0, $t4
jr $ra

calculatipo:
move $t1, $a1
move $t3, $ra
la $t0, quantidade
lw $t0, 0($t0)
addi $t2, $zero, 0
li $v0, 4
syscall
LOOP3:
beq $t2, $t0, END3
jal calculavalor
move $a0, $v0
li $v0, 1
syscall
li $v0, 4
move $a0, $t1
syscall
ldc1 $f12, 0($a2)
li $v0, 3
syscall
li $v0, 4
la $a0, linha
syscall
addi $t2, $t2, 1
addi $a2, $a2, 8
j LOOP3
END3:
jr $t3
