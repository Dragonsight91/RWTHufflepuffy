
class Equation(object):
    def __init__(self, equation):
        self.equation = self.filterWhitespace(equation)
        self.equationFunc = self.makeSolver(self.equation)

        # get variables
        varList = sorted(
            list(''.join(filter(str.isalpha, ''.join(set(self.equation))))))
        self.Vars = {}
        for i in varList:
            self.Vars[i] = False

    def filterWhitespace(self, equation):
        string = ""
        for char in equation:
            if(char != " " and char != "\t"):
                string += char
        print(string)
        return string

    def makeSolver(self, equation):
        bracketsOpen = 0
        opIndex = None

        for index, char in enumerate(equation):
            if(char == "("):
                bracketsOpen += 1
            elif(char == ")"):
                bracketsOpen -= 1

            if((char == "⇔" or char == "↔" or char == "⇒" or char == "→" or char == "⊕") and bracketsOpen == 0):
                opIndex = index
                break

        if(opIndex != None):
            part1 = self.partition(equation, 0, opIndex)
            part2 = self.partition(equation, opIndex+1, len(equation))

            A = self.makeSolver(part1)
            B = self.makeSolver(part2)

            solveEq = f'self.solver(\"{equation[opIndex]}\", {A}, {B})'
            # print(solveEq)
            return solveEq
        else:
            for index, char in enumerate(equation):
                if(char == "("):
                    bracketsOpen += 1
                elif(char == ")"):
                    bracketsOpen -= 1

                
                if((any(x in char for x in ["∧", "*"]) or any(x in char for x in ["∨", "+"])) and bracketsOpen == 0):
                    opIndex = index
                    break
            if(opIndex != None):
                part1 = self.partition(equation, 0, opIndex)
                part2 = self.partition(equation, opIndex+1, len(equation))

                A = self.makeSolver(part1)
                B = self.makeSolver(part2)

                solveEq = f'self.solver(\"{equation[opIndex]}\", {A}, {B})'
                # print(solveEq)
                return solveEq
            else:
                if(equation[0] == "¬"):
                    A = self.makeSolver(equation[1:len(equation)])
                    solveEq = f'self.negate({A})'
                    # print(solveEq)
                    return solveEq
                elif(equation[0] == "(" and equation[-1] == ")"):
                    A = self.makeSolver(equation[1:-1])
                    # print(A)
                    return A
                else:
                    try:
                        return int(equation)
                    except:
                        return f"self.Vars[\"{equation}\"]"

    def partition(self, equation, start, end):
        return equation[start:end]

    async def solve(self):
        solution = ""
        ldic = locals()
        exec("solution = " + self.equationFunc, globals(), ldic)
        solution = str(ldic["solution"])

        return solution

    def solver(self, operator, A, B):
        if((operator == "⇔" or operator == "↔") and A == B):
            solution = True
        elif(operator == "⇒" or operator == "→"):
            if(A == True and B == False):
                solution = False
            else:
                solution = True
        elif(operator == "⊕"):
            solution = A ^ B
        else:
            solution = False

        if any(x in operator for x in ["∧", "*"]):

            solution = (A and B)
        elif(any(x in operator for x in ["∨", "+"])):
            solution = (A or B)
        # print(f'{A}\t{operator}\t{B}\tSolution:{solution}')
        return solution

    def negate(self, A):
        return not A


    async def asciiTableSolve(self):
        header = ""
        for key in self.Vars.keys():
            header += f"  {key}  |"
        header += f'  Equation  '
        header += "\n"+"-"*43
        
        out = {
            "header":header,
            "table": ""
        }

        keys = self.Vars.keys()
        for i in range(0, (2**len(keys))):
            bin = format(i, 'b')
            counter = str(int(bin)).zfill(len(keys))

            row = ""
            for index, key in enumerate(keys):
                self.Vars[key] = bool(int(counter[index]))
                row += f'  {int(self.Vars[key])}  |'
            
            out["table"] += f"{row}  {int(eval(self.solve()))} \n"

        return out