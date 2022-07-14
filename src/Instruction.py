from src.file import *


class Instruction:
    type_dict, opcode_dict, function_dict = read_instructions()

    def __init__(self, name: str, instruction_list: list, has_label_start: bool, has_label_final: bool, pos: int,
                 labels: dict):
        self.name = name
        self.opcode = name
        self.type = Instruction.type_dict[name]
        self.has_immediate = False
        self.has_label_start = has_label_start
        self.has_label_final = has_label_final
        # tratando os registradores
        if self.type != 'j':
            if has_label_start:
                offset = 1
            else:
                offset = 0
            if self.name == "jr":
                self.rs = instruction_list[1 + offset]
                self.rt = '0'  # Aqui eu posso colocar tanto $zero ou 0
                self.rd = '0'
            elif self.type == 'r':
                if name != "sll" and name != "srl":
                    self.rd = instruction_list[1 + offset]
                    self.rs = instruction_list[2 + offset]
                    self.rt = instruction_list[3 + offset]
                else:
                    self.rs = instruction_list[1 + offset]
                    self.rt = '0'
                    self.rd = instruction_list[2 + offset]
            elif self.type == 'i':
                if name == "lw" or name == "sw":
                    rs = instruction_list[-1]
                    rs = rs.split('(')[1].replace(')', '')
                    self.rs = rs
                else:
                    self.rs = instruction_list[2 + offset]
                if has_label_final:
                    self.immediate = str(labels[instruction_list[-1]] - pos - 1)
                self.rt = instruction_list[1 + offset]
        else:
            if has_label_final:
                self.immediate = str(labels[instruction_list[-1]])
        # function and shamt sem tratar o label no final
        if self.type == 'r':
            self.function = Instruction.function_dict[name]
            if name == 'sll' or name == "srl":
                self.has_immediate = True
                self.shamt = instruction_list[-1]
            else:
                self.shamt = '0'
        if (self.type == 'i' or self.type == 'j') and not self.has_label_final:
            immediate = instruction_list[-1]
            if name == "lw" or name == "sw":
                immediate = immediate.split("(")[0]
                self.immediate = immediate
            self.immediate = immediate

    def bits(self) -> str:
        """Returns full 32-bit instruction."""
        if self.type == 'r':
            return self.opcode + self.rs + self.rt + self.rd + self.shamt + self.function
        elif self.type == 'i':
            return self.opcode + self.rs + self.rt + self.immediate
        else:
            return self.opcode + self.immediate

    def __str__(self):
        text = ""
        text += f"Nome = {self.name}\n"
        text += f"Opcode = {self.opcode}\n"
        text += f"Tipo = {self.type}\n"

        if self.type != 'j' and not self.has_label_start:
            text += f"RS = {self.rs}\n"
            if self.name != "jr":
                text += f"RT = {self.rt}\n"
                if self.type == 'r':
                    text += f"RD = {self.rd}\n"

        if self.type == 'r':
            text += f"Shamt = {self.shamt}\n"
            text += f"Function = {self.function}"
        if self.type == 'i' or self.type == 'j':
            text += f"Endereço/imediato = {self.immediate}"

        return text
