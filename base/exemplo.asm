addi $s0, $zero, 4
addi $t0, $zero, 0
LOOP: beq $s0, $t0, ELSE
addi $t0, $t0, 1
j LOOP
ELSE: sw $t0, 4($zero)
