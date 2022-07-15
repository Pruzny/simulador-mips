from src.file import *
from src.interface import Info
from src.pipeline_execution.Simulador import Simulador

LIST_PSEUDO = ["li", "la"]
SIZE = 4


def dec_to_hex(dec_value: int) -> str:
    """Receives a positive decimal value and returns its hex conversion with the correct length of bytes."""
    dec_value_int = int(dec_value)

    if dec_value_int < 0:
        if dec_value_int < -16 ** (SIZE - 1):
            raise ValueError("Valor imediato menor do que o tamanho suportado.")
    elif dec_value_int >= 16 ** SIZE:
        raise ValueError("Valor imediato maior do que o tamanho suportado.")
    else:
        return format(dec_value_int, f"0{SIZE}x")


def hex_to_dec(hex_value: str) -> int:
    """Receives a hex value and returns its decimal conversion."""
    return int(hex_value, 16)


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
        self.result = ""

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

    def calculate(self) -> None:
        match self.name:
            case "add":
                self.result = dec_to_hex(hex_to_dec(Info.REGS[self.rs]) + hex_to_dec(Info.REGS[self.rt]))
            case "addi":
                self.result = dec_to_hex(hex_to_dec(Info.REGS[self.rs]) + int(self.immediate))
            case "and":
                self.result = ""
                for bit1, bit2 in zip(Info.REGS[self.rs], Info.REGS[self.rt]):
                    self.result += "1" if bit1 != "0" and bit2 != "0" else "0"
            # case "beq":
            #
            # case "bne":
            #
            case "j":
                pc = int(self.immediate)
                Simulador.instructions_queue = Simulador.instructions_queue[:pc - 1] + Simulador.instructions[pc:]
            # case "jal":
            #
            # case "jr":
            #
            # case "lw":
            #
            case "or":
                self.result = ""
                for bit1, bit2 in zip(Info.REGS[self.rs], Info.REGS[self.rt]):
                    self.result += "1" if bit1 != "0" or bit2 != "0" else "0"
            case "sll":
                self.result = Info.REGS[self.rs][int(self.immediate):] + "0" * int(self.immediate)
            case "srl":
                self.result = "0" * int(self.immediate) + Info.REGS[self.rs][:int(self.immediate)]
            # case "sw":
            #
            case "sub":
                value = hex_to_dec(Info.REGS[self.rs]) + hex_to_dec(Info.REGS[self.rt])
                self.result = dec_to_hex(value) if value >= 0 else dec_to_hex(0)

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
