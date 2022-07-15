from src.file import *

LIST_PSEUDO = ["li", "la"]


class Instruction:
    type_dict, opcode_dict, function_dict = read_instructions()

    def __init__(self, name: str, has_label_start: int, has_label_final: bool, instruction_in_form_list: list[str],
                 pos: int, instruction_string: str):
        labels = Simulador.labels
        self.name = name
        self.opcode = name
        self.has_label_start = has_label_start
        self.has_label_final = has_label_final
        self.rt = instruction_in_form_list[1 + has_label_start]
        self.str = instruction_string
        self.stage = None

        if self.opcode in LIST_PSEUDO:
            self.type = "p"
            self.has_immediate = True
            self.rd = instruction_in_form_list[1 + has_label_start]
            self.immediate = instruction_in_form_list[2 + has_label_start]
        else:
            self.type = Instruction.type_dict[name]
            self.has_immediate = False
            match self.type:
                case "i":
                    if has_label_final:
                        self.immediate = str(labels[instruction_in_form_list[-1]] - pos - 1)
                    else:
                        immediate = instruction_in_form_list[-1]
                        if name == "lw" or name == "sw":
                            rs = instruction_in_form_list[-1]
                            rs = rs.split('(')[1].replace(')', '')
                            self.rs = rs
                            immediate = immediate.split("(")[0]
                            self.immediate = immediate
                        else:
                            self.rs = instruction_in_form_list[2 + has_label_start]
                        self.immediate = immediate
                    self.has_immediate = True
                case "r":
                    if name == "jr":
                        self.rs = instruction_in_form_list[1 + has_label_start]
                        self.rt = '0'
                        self.rd = '0'
                    if name != "sll" and name != "srl":
                        self.rd = instruction_in_form_list[1 + has_label_start]
                        self.rs = instruction_in_form_list[2 + has_label_start]
                        self.rt = instruction_in_form_list[3 + has_label_start]
                    else:
                        self.rs = instruction_in_form_list[1 + has_label_start]
                        self.rt = '0'
                        self.rd = instruction_in_form_list[2 + has_label_start]
                case "j":
                    if has_label_final:
                        self.immediate = str(labels[instruction_in_form_list[-1]])

    def bits(self) -> str:
        """Returns full 32-bit instruction."""
        if self.name != "la":
            if self.type == 'r':
                return self.opcode + self.rs + self.rt + self.rd
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

        if self.type == 'i' or self.type == 'j':
            text += f"Endereço/imediato = {self.immediate}"

        return text
