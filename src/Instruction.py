from file import *
from src.interface import Info
from src.pipeline_execution.Simulador import Simulador

LIST_PSEUDO = ["li", "la"]
SIZE = 4


def dec_to_hex(dec_value: int, size: int = SIZE) -> str:
    """Receives a positive decimal value and returns its hex conversion with the correct length of bytes."""
    dec_value_int = int(dec_value)

    if dec_value_int < 0:
        if dec_value_int < -16 ** (size - 1):
            raise ValueError("Valor imediato menor do que o tamanho suportado.")
    elif dec_value_int >= 16 ** size:
        raise ValueError("Valor imediato maior do que o tamanho suportado.")
    else:
        return format(dec_value_int, f"0{size}x")


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
        self.rd = None
        self.rs = None
        self.rt_value = None
        self.rs_value = None
        self.immediate = None
        self.result = ""
        self.hazard_rs = ""
        self.hazard_rt = ""

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
                        self.immediate = str(Simulador.labels[instruction_in_form_list[-1]] - pos - 1)
                        self.rs = instruction_in_form_list[2 + has_label_start]
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
                    self.rd = self.rt
                case "r":
                    if name == "jr":
                        self.rs = instruction_in_form_list[1 + has_label_start]
                        self.rt = '$zero'
                        self.rd = '$zero'
                    elif name != "sll" and name != "srl":
                        self.rd = instruction_in_form_list[1 + has_label_start]
                        self.rs = instruction_in_form_list[2 + has_label_start]
                        self.rt = instruction_in_form_list[3 + has_label_start]
                    else:
                        self.rs = instruction_in_form_list[1 + has_label_start]
                        self.rt = '$zero'
                        self.rd = instruction_in_form_list[2 + has_label_start]
                        self.immediate = instruction_in_form_list[3 + has_label_start]
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

    def check_hazard(self) -> None:
        if self.hazard_rs == "ForwardA":
            self.rs_value = Simulador.list_registers_pipeline[2].instruction.result
            self.hazard_rs = ""
        if self.hazard_rt == "ForwardB":
            self.rt_value = Simulador.list_registers_pipeline[2].instruction.result
            self.hazard_rt = ""
        if self.hazard_rs == "ForwardC":
            self.rs_value = Simulador.list_registers_pipeline[3].instruction.result
            self.hazard_rs = ""
        if self.hazard_rt == "ForwardD":
            self.rt_value = Simulador.list_registers_pipeline[3].instruction.result
            self.hazard_rt = ""

    def id(self):
        if self.name != "j" and self.name != "jal":
            if self.rs is not None:
                self.rs_value = Info.REGS[self.rs]
            if self.rt is not None:
                self.rt_value = Info.REGS[self.rt]
            self.check_hazard()
            if self.name == "beq":
                self.result = self.rs_value == self.rt_value
            if self.name == "bne":
                self.result = self.rs_value != self.rt_value

    def calculate(self) -> None:
        self.check_hazard()
        try:
            match self.name:
                case "add":
                    self.result = dec_to_hex(hex_to_dec(self.rs_value) + hex_to_dec(self.rt_value), 8)
                case "addi":
                    self.result = dec_to_hex(hex_to_dec(self.rs_value) + int(self.immediate), 8)
                case "and":
                    self.result = ""
                    for bit1, bit2 in zip(self.rs_value, self.rt_value):
                        self.result += "1" if bit1 != "0" and bit2 != "0" else "0"
                case "jr":
                    self.result = hex_to_dec(self.rs_value)
                case "lw":
                    self.result = Info.DATA[dec_to_hex(hex_to_dec(self.rs_value), 4)]
                case "or":
                    self.result = ""
                    for bit1, bit2 in zip(self.rs_value, self.rt_value):
                        self.result += "1" if bit1 != "0" or bit2 != "0" else "0"
                case "sll":
                    offset = int(self.immediate) if 0 <= int(self.immediate) <= 8 else 8
                    self.result = self.rs_value[offset:] + "0" * int(offset)
                case "srl":
                    offset = int(self.immediate) if 0 <= int(self.immediate) <= 8 else 8
                    self.result = "0" * offset + self.rs_value[:8 - offset]
                case "sub":
                    value = hex_to_dec(self.rs_value) - hex_to_dec(self.rt_value)
                    self.result = dec_to_hex(value, 8) if value >= 0 else dec_to_hex(0, 8)
                case "li":
                    self.result = dec_to_hex(int(self.immediate), 8)
        except Exception as ex:
            raise ex
            print(f"Ocorreu um erro ao  calcular a instrucao {self.name}, Verifique o codigo, principalmente, verifique os registradores")


    def mem(self) -> None:
        self.check_hazard()
        match self.name:
            case "lw":
                self.result = Info.DATA[dec_to_hex(hex_to_dec(self.rs_value) + int(self.immediate), 4)]
            case "sw":
                Info.DATA[dec_to_hex(hex_to_dec(self.rs_value) + int(self.immediate), 4)] = self.rt_value

    def wb(self) -> None:
        match self.name:
            case "sw":
                pass
            case "lw":
                Info.REGS[self.rt] = self.result
            case _:
                match self.type:
                    case "i":
                        if self.name != "beq" and self.name != "bne":
                            Info.REGS[self.rt] = self.result
                    case "r":
                        if self.name != "jr":
                            Info.REGS[self.rd] = self.result

    def __str__(self):
        text = ""

        if self.name is not None:
            text += f"Nome = {self.name} "
        if self.opcode is not None:
            text += f"Opcode = {self.opcode} "
        if self.type is not None:
            text += f"Tipo = {self.type} "
        if self.rs is not None:
            text += f"RS = {self.rs} "
        if self.rt is not None:
            text += f"RT = {self.rt} "
        if self.rd is not None:
            text += f"RD = {self.rd} "
        if self.immediate is not None:
            text += f"Endereço/imediato = {self.immediate}"

        return text
