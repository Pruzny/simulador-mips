addi $s0, $zero, 4
jal FUNC
addi $t6, $zero, 0
LOOP: beq $s0, $t0, ELSE
addi $t0, $t0, 1
j LOOP
ELSE: sw $t0, 4($zero)
j EXIT

FUNC: add $s2, $s0, $s0
addi $ra, $zero, 3
jr $ra

EXIT: addi $t7, $zero, 0