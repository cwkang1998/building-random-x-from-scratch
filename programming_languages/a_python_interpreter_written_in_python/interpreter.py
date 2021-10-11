from typing import Dict, Union


class Interpreter:
    def __init__(self):
        self.stack = []
        self.environment = {}

    def LOAD_VALUE(self, number: int) -> None:
        self.stack.append(number)

    def ADD_TWO_VALUES(self) -> None:
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def PRINT_ANSWER(self) -> None:
        answer = self.stack.pop()
        print(answer)

    def STORE_NAME(self, name: str) -> None:
        val = self.stack.pop()
        self.environment[name] = val

    def LOAD_NAME(self, name: str) -> None:
        val = self.environment[name]
        self.stack.append(val)

    def parse_argument(
        self,
        instruction: str,
        argument: int,
        what_to_execute: Dict
    ) -> Union[int, str]:
        '''Understand what the argument to each instruction means.'''
        numbers = ['LOAD_VALUE']
        names = ['LOAD_NAME', 'STORE_NAME']

        if instruction in numbers:
            argument = what_to_execute['numbers'][argument]
        elif instruction in names:
            argument = what_to_execute['names'][argument]

        return argument

    def execute(self, what_to_execute: Dict) -> None:
        instructions = what_to_execute['instructions']
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(
                instruction,
                argument,
                what_to_execute
            )
            bytecode_method = getattr(self, instruction)

            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)


what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),
                     ("LOAD_VALUE", 1),
                     ("ADD_TWO_VALUES", None),
                     ("LOAD_VALUE", 2),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5, 8]}


interpreter = Interpreter()
interpreter.execute(what_to_execute)
