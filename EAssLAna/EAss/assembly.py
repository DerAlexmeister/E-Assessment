INST = ['MOV', 'ADD', 'SUB', 'INC', 'DEC']

def isStateValue(state, key):
    try:
        return key in state.keys()
    except Exception as error:
        print(error)
        return False

def checkRegisters(command, state):
    try:
        exists = []
        for index, i in enumerate(command):
            if i.startswith("$"):
                if index == 0:
                    if i not in state.keys():
                        state[i] = 0
                    exists.append(True)
                else:
                    exists.append(isStateValue(state, i))
        return exists
    except Exception as error:
        print(error)
        return [False]

def getStateValue(state, register):
    if register in state.keys():
        return int(state[register])
    else:
        return int(register)

def addfunc(command, state):
    try:
        registersstatus = checkRegisters(command, state)
        if False in registersstatus:
            return None
        else:
            state[command[0]] = getStateValue(state, command[1]) + getStateValue(state, command[2])
        return state
    except Exception as error:
        print(error)
        return error

def subfunc(command, state):
    try:
        registersstatus = checkRegisters(command, state)
        if False in registersstatus:
            return None
        else:
            state[command[0]] = getStateValue(state, command[1]) - getStateValue(state, command[2])
        return state
    except Exception as error:
        print(error)
        return error

def movfunc(command, state):
    try:
        registersstatus = checkRegisters(command, state)
        if False in registersstatus:
            return None
        else:
            state[command[0]] = getStateValue(state, command[1])
        return state
    except Exception as error:
        print(error)
        return error

def incfunc(command, state):
    try:
        registersstatus = checkRegisters(command, state)
        if False in registersstatus:
            return None
        else:
            state[command[0]] = getStateValue(state, command[0]) + 1
        return state
    except Exception as error:
        print(error)
        return error

def decfunc(command, state):
    try:
        registersstatus = checkRegisters(command, state)
        if False in registersstatus:
            return None
        else:
            state[command[0]] = getStateValue(state, command[0]) - 1
        return state
    except Exception as error:
        print(error)
        return error

def parser(programm):
    try:
        programm = programm.replace("\r", "")
        instructionssets = []
        programm_split = []
        for statement in [i if i != '' and len(i) > 3 else None for i in str(programm).split('\n')]:
            if statement is not None: programm_split.append(statement)
        for index, command in enumerate(programm_split):
            command_split = command.split(' ')
            instruction, operators = command_split[0], command_split[1].split(',')
            if instruction not in INST:
                return MiniAssembler(error="Unknown command")
            if (oplen := len(operators)) is None and (oplen < 1 or oplen > 3):
                if oplen is None:
                    return MiniAssembler(error="Synatxerror in line {}!".format(index))
                elif oplen < 2:
                    return MiniAssembler(error="There is a operator missing!")
                elif oplen > 3:
                    return MiniAssembler(error="There are more then 3 operators!")
                else:
                    return MiniAssembler(error="Unknown error in the operators!")
            else:
                instructionssets.append([instruction, *operators]) 
        return MiniAssembler(instructions=instructionssets)
    except Exception as error:
        print(error)
        return MiniAssembler(error=str(error))

class MiniAssembler():

    def __init__(self, instructions=[], error=None, state={}):
        self.instructions = instructions
        self.error = error
        self.state = state
        self.missing_instructions = []
        self.states = []

    def getCode(self):
        return self.instructions

    def getMissingInstructions(self):
        return self.missing_instructions

    def eval(self):
        try:
            l_states = []
            state = {}
            for command in self.instructions:
                state = OPINST[command[0]](command[1:], state)
                if state == None and not isinstance(state, dict):
                    self.error = state
                    return self.error
                l_states.append({str(command[0]) + " " + ','.join(command[1:]): dict(state.items())})
            self.state, self.states = state, l_states 
            return state
        except Exception as error:
            self.error = error
            return self.error

    def getInstructions(self):
        return self.instructions

    def getStates(self):
        return self.states

    def getLastStates(self):
        try:
            lastworkingstate = 0
            for i, e in enumerate(self.states):
                if None not in e.keys():
                    lastworkingstate = i
                else:
                    break
            laststate = self.states[lastworkingstate]
            for _, v in laststate.items(): 
                if isinstance(v, dict):
                    return v
        except Exception as error:
            print(error)
        return {}

    def hasError(self):
        return self.error is not None

    def getError(self):
        return self.error

    def print(self):
        try:
            for k, v in self.state.items():
                if k is not None and v is not None:
                    print("Register {}: {}".format(k, v))
        except Exception as error:
            pass

    def __str__(self):
        return str(self.instructions)

    def equalsState(self, foreignstate):
        try:
            if isinstance(foreignstate, dict):
                return self.state == foreignstate
            return False
        except Exception as error:
            print(error)
            return False

    def checkForStatement(self, n_statements):
        try:
            instruction_statements = [i[0] for i in self.instructions]
            for instruction in n_statements:
                if instruction not in instruction_statements:
                    self.missing_instructions.append(instruction)
        except Exception as error:
            print(error)
        return self.missing_instructions

    def hasMissingInstructions(self):
        return len(self.missing_instructions) > 0

    def compareSolutions(self):
        try:
            pass
        except Exception as error:
            print(error) 

OPINST = {
    "ADD": addfunc,
    "SUB": subfunc,
    "MOV": movfunc,
    "INC": incfunc,
    "DEC": decfunc
}


programm = """
MOV $0,1
MOV $1,2
MOV $2,534
MOV $3,4
ADD $0,$0,1
SUB $0,$1,$0
MOV $0,-1
INC $2
DEC $3
"""

#parsed = parser(programm)
#print(parsed)
#state = parsed.eval()
#parsed.print()