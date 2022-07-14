.data
input1: .asciiz "Digite a quantidade de valores "
input2: .asciiz "Por favor, insira um valor inteiro para calcularmos a media "
media: .asciiz "Media: "
.text

addi $s0, $zero, 0
addi $s1, $zero, 0
addi $s2, $zero, 0

li $v0, 4
la $a0, input1
syscall

li $v0, 5
syscall
move $s0, $v0

addi $t0, $zero, 0


FOR: bne $t0, $s0, EXIT
li $v0, 4
la $a0, input2
syscall
li $v0, 5
syscall

move $s2, $v0
add $s1, $s1, $s2
addi $t0, $t0, 1
j FOR

EXIT: li $v0, 4
la $a0, media
syscall

sub $a0, $s1, $s0
addi $v0, $zero, 1
syscall
