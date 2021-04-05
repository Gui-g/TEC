from pathlib import Path
import sys

cmd_list = list()

class TuringAux:
    def __init__(self,tm_type, states, operations):
        self.type = tm_type
        self.states = states
        self.operations = operations

class CMD:
    def __init__(self, current_state, current_symbol, new_symbol, direction, new_state):
        self.current_state = current_state
        self.current_symbol = current_symbol
        self.new_symbol = new_symbol
        self.direction = direction
        self.new_state = new_state

#colocar símbolo especial # no começo da fita, para qualquer estado se ler # voltar
def S_to_I(turing_machine):

    turing_machine.type = "I"

    #aumenta o número do estado em 1 para criar um novo estado 0 que prepara a fita
    for op in turing_machine.operations:
        if op.new_state == "halt-accept":
            op.current_state = int(op.current_state) + 1
        else:
            op.current_state = int(op.current_state) + 1
            op.new_state = int(op.new_state) + 1

    new_state = list()
    for state in turing_machine.states:
        new_state.append(int(state) + 1)

    turing_machine.states = new_state

    #para todo estado uma regra que caso leia # voltar para a fita
    for state in turing_machine.states:
        turing_machine.operations.append(CMD(state,"#","#","r",state))

    #comando para colocar # no começo da fita
    turing_machine.operations.insert(0,CMD(0,"*","*","l",100))
    turing_machine.operations.insert(1,CMD(100,"_","#","r",1)) #voltar para o estado inicial original

    return turing_machine

#colocar símbolo especial # no começo da fita, mover fita uma casa para a direita quando chega em #
def I_to_S(turing_machine):

    turing_machine.type = "S"

    #aumenta o número do estado em 1 para criar um novo estado 0 que prepara a fita
    for op in turing_machine.operations:
        if op.new_state == "halt-accept":
            op.current_state = int(op.current_state) + 1
        else:
            op.current_state = int(op.current_state) + 1
            op.new_state = int(op.new_state) + 1

    new_state = list()
    for state in turing_machine.states:
        new_state.append(int(state) + 1)

    turing_machine.states = new_state

    #primeiro espaço:
    #dependendo do que lê (1 ou 0) vai para estados intermediários para manter a informação salva enquanto move fita
    turing_machine.operations.insert(0,CMD(0,"1","#","r",101)) #1
    turing_machine.operations.insert(1,CMD(0,"0","#","r",102)) #0
    turing_machine.operations.insert(2,CMD(101,"1","_","l",103)) #11
    turing_machine.operations.insert(3,CMD(101,"0","_","l",104)) #10
    turing_machine.operations.insert(4,CMD(102,"1","_","l",105)) #01
    turing_machine.operations.insert(5,CMD(102,"0","_","l",106)) #00
    turing_machine.operations.insert(6,CMD(103,"#","#","r",103)) #11
    turing_machine.operations.insert(7,CMD(103,"_","_","r",103)) #11
    turing_machine.operations.insert(8,CMD(103,"1","1","r",107)) #11
    turing_machine.operations.insert(9,CMD(103,"0","1","r",108)) #10
    turing_machine.operations.insert(10,CMD(104,"#","#","r",104)) #10
    turing_machine.operations.insert(11,CMD(104,"_","_","r",104)) #10
    turing_machine.operations.insert(12,CMD(104,"1","1","r",109)) #01
    turing_machine.operations.insert(13,CMD(104,"0","1","r",110)) #00
    turing_machine.operations.insert(14,CMD(105,"#","#","r",105)) #01
    turing_machine.operations.insert(15,CMD(105,"_","_","r",105)) #01
    turing_machine.operations.insert(16,CMD(105,"1","0","r",107)) #11
    turing_machine.operations.insert(17,CMD(105,"0","0","r",108)) #10
    turing_machine.operations.insert(18,CMD(106,"#","#","r",106)) #00
    turing_machine.operations.insert(19,CMD(106,"_","_","r",106)) #00
    turing_machine.operations.insert(20,CMD(106,"1","0","r",109)) #01
    turing_machine.operations.insert(21,CMD(106,"0","0","r",110)) #00
    turing_machine.operations.insert(22,CMD(107,"_","1","r",111)) #1
    turing_machine.operations.insert(23,CMD(107,"1","1","r",107)) #11
    turing_machine.operations.insert(24,CMD(107,"0","1","r",108)) #10
    turing_machine.operations.insert(25,CMD(108,"_","1","r",112)) #0
    turing_machine.operations.insert(26,CMD(108,"1","1","r",109)) #01
    turing_machine.operations.insert(27,CMD(108,"0","1","r",110)) #00
    turing_machine.operations.insert(28,CMD(109,"_","0","r",111)) #1
    turing_machine.operations.insert(29,CMD(109,"1","0","r",107)) #11
    turing_machine.operations.insert(30,CMD(109,"0","0","r",108)) #10
    turing_machine.operations.insert(31,CMD(110,"_","0","r",112)) #0
    turing_machine.operations.insert(32,CMD(110,"1","0","r",109)) #01
    turing_machine.operations.insert(33,CMD(110,"0","0","r",110)) #00
    turing_machine.operations.insert(34,CMD(111,"_","1","l",113)) #
    turing_machine.operations.insert(35,CMD(112,"_","0","l",113)) #
    turing_machine.operations.insert(36,CMD(113,"*","*","l",113)) #
    turing_machine.operations.insert(37,CMD(113,"_","_","r",1)) #voltar para o estado inicial original  

    #subrotina de espaço para cada estado
    #para qualquer estado, caso leia # então mover, colocar _ e empurrar fita para a direita
    for state in turing_machine.states:
        turing_machine.operations.append(CMD(state,"#","#","r",str(state)+"subr"))
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
        turing_machine.operations.append(CMD(str(state)+"subr3","#","#","r",state)) #
    
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