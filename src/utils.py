from src.Instruction import Instruction


def create_labels(list_instruction: list[str]) -> dict:
    """Generates an dictionary mapping each label of the input file to its corresponding line (starting from 0)."""
    labels = dict()
    for i, instruction in enumerate(list_instruction):
        if ":" in instruction[0]:
            labels[instruction[0].replace(':', "")] = i

    return labels


def check_instruction(instruction_in_form_list: list[str], pos: int, labels: dict,
                      instruction_string: str):
    """Generates and returns an object of the instruction."""
    last_word_instruction = instruction_in_form_list[-1]
    has_label_init = False
    has_label_final = False
    offset = 0

    if ":" in instruction_in_form_list[0]:
        has_label_init = True
        offset = 1
    if last_word_instruction.isalpha() or (last_word_instruction.isnumeric() and last_word_instruction.isalpha()):
        has_label_final = True

    if instruction_in_form_list[0 + offset] == "move":
        if has_label_init:
            instruction_in_form_list = [instruction_in_form_list[0], "add", instruction_in_form_list[2], "$zero",
                                        instruction_in_form_list[3]]
        else:
            instruction_in_form_list = ["add", instruction_in_form_list[1], "$zero", instruction_in_form_list[2]]
    if not has_label_init:
        instruction_obj = Instruction(
            instruction_in_form_list[0], offset, has_label_final, instruction_in_form_list, pos, instruction_string)
    else:
        instruction_obj = Instruction(
            instruction_in_form_list[1], offset, has_label_final, instruction_in_form_list, pos, instruction_string)
    return instruction_obj


def transforming_instruction(list_instruction: list, labels: dict) -> list:
    """Generates the output file. If '-t' flag is used, then the output file is a 'txt'. Otherwise, it is a 'bin' file."""
    lista_objetos_instructions = list()
    str_instruction = ""
    for i, l in enumerate(list_instruction):
        for el in l:
            if ":" in el:
                el = el.split(":")[1]
            str_instruction = str_instruction + el + " "
        instruction_obj = check_instruction(l, i, labels, str_instruction)  # Instrucao em forma de objeto
        str_instruction = ""
        lista_objetos_instructions.append(instruction_obj)  # Lista de objetos

    return lista_objetos_instructions


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
