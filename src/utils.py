from bitarray import bitarray

from src.Instruction import Instruction

'''def dec_to_bin(dec_value: str, size: int) -> str:
    """Receives a string of a decimal value and the number of bits for the output and returns its conversion formated."""
    dec_value_int = int(dec_value)

    if dec_value_int < 0:
        if dec_value_int < -2 ** (size - 1):
            raise ValueError("Valor imediato menor do que o tamanho suportado.")
        else:
            bin_value = format(dec_value_int, f"0{size + 1}b")[1:].replace("1", "x").replace("0", "1").replace("x", "0")
            neg_bin = ""
            changed = False
            for bit in bin_value[::-1]:
                if not changed:
                    if bit == "1":
                        neg_bin += "0"
                    else:
                        neg_bin += "1"
                        changed = True
                else:
                    neg_bin += bit
            return neg_bin[::-1]
    elif dec_value_int >= 2 ** size:
        raise ValueError("Valor imediato maior do que o tamanho suportado.")
    else:
        return format(dec_value_int, f"0{size}b")'''


def create_labels(list_instruction: list[str]) -> dict:
    """Generates an dictionary mapping each label of the input file to its corresponding line (starting from 0)."""
    labels = dict()
    for i, instruction in enumerate(list_instruction):
        if ":" in instruction[0]:
            labels[instruction[0].replace(':', "")] = i

    return labels


def check_instruction(list_instruction: list, pos: int, labels: dict) -> Instruction:
    """Generates and returns an object of the instruction."""
    last_word_instruction = list_instruction[-1]
    has_label_init = False
    has_label_final = False

    if ":" in list_instruction[0]:
        has_label_init = True
    if last_word_instruction.isalpha():
        has_label_final = True

    if not has_label_init:
        instruction_obj = Instruction(list_instruction[0], list_instruction, has_label_init, has_label_final, pos,
                                      labels)
    else:
        instruction_obj = Instruction(list_instruction[1], list_instruction, has_label_init, has_label_final, pos,
                                      labels)

    if instruction_obj.type == 'i':
        instruction_obj.has_immediate = True

    return instruction_obj


def transforming_instruction(list_instruction: list, labels: dict, txt: bool) -> list:
    """Generates the output file. If '-t' flag is used, then the output file is a 'txt'. Otherwise, it is a 'bin' file."""
    lista_objetos_instructions = list()
    instructions = list()
    str_instruction = ""
    if txt:
        with open("saida.txt", 'w') as file:
            for i, l in enumerate(list_instruction):
                instruction_obj = check_instruction(l, i, labels)  # Instrucao em forma de objeto
                for el in l:
                    if ":" in el:
                        el = el.split(":")[1]
                    str_instruction = str_instruction + el + " "
                instructions.append(str_instruction)
                str_instruction = ""
                lista_objetos_instructions.append(instruction_obj)  # Lista de objetos
                file.write(f"{instruction_obj.bits()}\n")
            file.close()
    else:
        with open("saida.bin", "wb") as file:
            output = bitarray(32 * len(list_instruction))
            for i, l in enumerate(list_instruction):
                instruction_obj = check_instruction(l, i, labels)

                lista_objetos_instructions.append(instruction_obj)
                for j, byte in enumerate(instruction_obj.bits()):
                    output[i * 32 + j] = int(byte)
            output.tofile(file)
            file.close()
    return lista_objetos_instructions, instructions


def to_read(txt: bool) -> None:
    """Prints each line of the corresponding output file."""
    if txt:
        with open("saida.txt", 'r') as file:
            print(file.read())
            file.close()
    else:
        with open("saida.bin", "rb") as file:
            byte = file.read(4)
            while byte:
                print(format(int.from_bytes(byte, byteorder="big"), f"032b"))
                byte = file.read(4)
            file.close()
