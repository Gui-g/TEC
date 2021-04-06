from pathlib import Path
import sys

cmd_list = list()

class TuringAux:
    def __init__(self,tm_type, states, operations):
        self.type = tm_type
        self.states = states
        self.operations = operations
        self.initial_state = "0"

class CMD:
    def __init__(self, current_state, current_symbol, new_symbol, direction, new_state):
        self.current_state = current_state
        self.current_symbol = current_symbol
        self.new_symbol = new_symbol
        self.direction = direction
        self.new_state = new_state

    def string(self):
        return str(self)

#colocar símbolo especial # no começo da fita, para qualquer estado se ler # voltar
def S_to_I(turing_machine):

    turing_machine.type = "I"

    #mudar o número do estado com 1 para criar um novo estado 0 que prepara a fita
    for op in turing_machine.operations:
        op.current_state = op.current_state + "1"
        op.new_state = op.new_state + "1"

    new_state = list()
    for state in turing_machine.states:
        new_state.append(state + "1")

    turing_machine.states = new_state

    #para todo estado uma regra que caso leia # voltar para a fita
    for state in turing_machine.states:
        turing_machine.operations.append(CMD(state,"§","§","r",state))

    #comando para colocar # no começo da fita
    turing_machine.operations.insert(0,CMD(0,"*","*","l","step"))
    turing_machine.operations.insert(1,CMD("step","_","§","r",turing_machine.initial_state+"1")) #voltar para o estado inicial original

    return turing_machine

#colocar símbolo especial # no começo da fita, mover fita uma casa para a direita quando chega em #
def I_to_S(turing_machine):

    turing_machine.type = "S"

    #mudar o número do estado com 1 para criar um novo estado 0 que prepara a fita
    for op in turing_machine.operations:
        op.current_state = op.current_state + "1"
        op.new_state = op.new_state + "1"

    new_state = list()
    for state in turing_machine.states:
        new_state.append(state + "1")

    turing_machine.states = new_state

    #primeiro espaço:
    #dependendo do que lê (1 ou 0) vai para estados intermediários para manter a informação salva enquanto move fita
    turing_machine.operations.insert(0,CMD(0,"1","§","r","step1")) #1
    turing_machine.operations.insert(1,CMD(0,"0","§","r","step2")) #0
    turing_machine.operations.insert(2,CMD("step1","1","_","l","step3")) #11
    turing_machine.operations.insert(3,CMD("step1","0","_","l","step4")) #10
    turing_machine.operations.insert(4,CMD("step2","1","_","l","step5")) #01
    turing_machine.operations.insert(5,CMD("step2","0","_","l","step6")) #00
    turing_machine.operations.insert(6,CMD("step3","§","§","r","step3")) #11
    turing_machine.operations.insert(7,CMD("step3","_","_","r","step3")) #11
    turing_machine.operations.insert(8,CMD("step3","1","1","r","step7")) #11
    turing_machine.operations.insert(9,CMD("step3","0","1","r","step8")) #10
    turing_machine.operations.insert(10,CMD("step4","§","§","r","step4")) #10
    turing_machine.operations.insert(11,CMD("step4","_","_","r","step4")) #10
    turing_machine.operations.insert(12,CMD("step4","1","1","r","step9")) #01
    turing_machine.operations.insert(13,CMD("step4","0","1","r","step10")) #00
    turing_machine.operations.insert(14,CMD("step5","§","§","r","step5")) #01
    turing_machine.operations.insert(15,CMD("step5","_","_","r","step5")) #01
    turing_machine.operations.insert(16,CMD("step5","1","0","r","step7")) #11
    turing_machine.operations.insert(17,CMD("step5","0","0","r","step8")) #10
    turing_machine.operations.insert(18,CMD("step6","§","§","r","step6")) #00
    turing_machine.operations.insert(19,CMD("step6","_","_","r","step6")) #00
    turing_machine.operations.insert(20,CMD("step6","1","0","r","step9")) #01
    turing_machine.operations.insert(21,CMD("step6","0","0","r","step10")) #00
    turing_machine.operations.insert(22,CMD("step7","_","1","r","step11")) #1
    turing_machine.operations.insert(23,CMD("step7","1","1","r","step7")) #11
    turing_machine.operations.insert(24,CMD("step7","0","1","r","step8")) #10
    turing_machine.operations.insert(25,CMD("step8","_","1","r","step12")) #0
    turing_machine.operations.insert(26,CMD("step8","1","1","r","step9")) #01
    turing_machine.operations.insert(27,CMD("step8","0","1","r","step10")) #00
    turing_machine.operations.insert(28,CMD("step9","_","0","r","step11")) #1
    turing_machine.operations.insert(29,CMD("step9","1","0","r","step7")) #11
    turing_machine.operations.insert(30,CMD("step9","0","0","r","step8")) #10
    turing_machine.operations.insert(31,CMD("step10","_","0","r","step12")) #0
    turing_machine.operations.insert(32,CMD("step10","1","0","r","step9")) #01
    turing_machine.operations.insert(33,CMD("step10","0","0","r","step10")) #00
    turing_machine.operations.insert(34,CMD("step11","_","1","l","step13")) #
    turing_machine.operations.insert(35,CMD("step12","_","0","l","step13")) #
    turing_machine.operations.insert(36,CMD("step13","*","*","l","step13")) #
    turing_machine.operations.insert(37,CMD("step13","_","_","r",turing_machine.initial_state+"1")) #voltar para o estado inicial original  

    #subrotina de espaço para cada estado
    #para qualquer estado, caso leia # então mover, colocar _ e empurrar fita para a direita
    for state in turing_machine.states:
        turing_machine.operations.append(CMD(state,"§","§","r",str(state)+"subr"))
        turing_machine.operations.append(CMD(str(state)+"subr","_","_","r",str(state)+"subr"))
        turing_machine.operations.append(CMD(str(state)+"subr","1","_","r",str(state)+"subr1")) #1
        turing_machine.operations.append(CMD(str(state)+"subr","0","_","r",str(state)+"subr2")) #0
        turing_machine.operations.append(CMD(str(state)+"subr1","1","1","r",str(state)+"subr1")) #1
        turing_machine.operations.append(CMD(str(state)+"subr1","0","1","r",str(state)+"subr2")) #0
        turing_machine.operations.append(CMD(str(state)+"subr1","_","1","r",str(state)+"subr3")) #
        turing_machine.operations.append(CMD(str(state)+"subr2","1","0","r",str(state)+"subr1")) #1
        turing_machine.operations.append(CMD(str(state)+"subr2","0","0","r",str(state)+"subr2")) #0
        turing_machine.operations.append(CMD(str(state)+"subr2","_","0","r",str(state)+"subr3")) #
        turing_machine.operations.append(CMD(str(state)+"subr3","*","*","l",str(state)+"subr3")) #
        turing_machine.operations.append(CMD(str(state)+"subr3","§","§","r",state)) #
    
    return turing_machine

if __name__ == "__main__":
    
    file_directory = Path("src/")
    for current_file in file_directory.iterdir():
        if current_file.is_file():
            with open(current_file, 'r') as data_file:
                lines = [line[:-1] for line in data_file]
                for line in lines:
                    if line[0] == ';':
                        mt_type = line[1]
                    else:
                        line_data = [x for x in line.split(" ")]
                        cmd_list.append(CMD(line_data[0],line_data[1],line_data[2],line_data[3],line_data[4]))

                states = set([x.current_state for x in cmd_list])
                turing_machine = TuringAux(mt_type, states, cmd_list)

                if(turing_machine.type == "I"):
                    new_tm = I_to_S(turing_machine)
                elif(turing_machine.type == "S"):
                    new_tm = S_to_I(turing_machine)
                else:
                    print("not recognized as doubly infinite or sipser")
                
                with open(current_file.name.split(".")[0] + "_new" + "." + current_file.name.split(".")[1], 'w') as new_data:
                    sys.stdout = new_data
                    print(";" + str(new_tm.type))
                    for op in new_tm.operations:
                        print(str(op.current_state) + " " + str(op.current_symbol) + " " + str(op.new_symbol) + " " + str(op.direction) + " " + str(op.new_state))

                cmd_list.clear()