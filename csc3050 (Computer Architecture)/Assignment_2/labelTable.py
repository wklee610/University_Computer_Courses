
#R-Type
Rtype = [ 'add'
        , 'addu'
        , 'and'
        , 'div'
        , 'divu'
        , 'jalr'
        , 'jr'
        , 'mfhi'
        , 'mflo'
        , 'mthi'
        , 'mtlo'
        , 'mult'
        , 'multu'
        , 'nor'
        , 'or'
        , 'sll'
        , 'sllv'
        , 'slt'
        , 'sltu'
        , 'sra'
        , 'srav'
        , 'srl'
        , 'srlv'
        , 'sub'
        , 'subu'
        , 'syscall'
        , 'xor']

#I-Type
Itype = [ 'addi'
        , 'addiu'
        , 'andi'
        , 'beq'
        , 'bgez'
        , 'bgtz'
        , 'blez'
        , 'bltz'
        , 'bne'
        , 'lb'
        , 'lbu'
        , 'lh'
        , 'lhu'
        , 'lui'
        , 'lw'
        , 'ori'
        , 'sb'
        , 'slti'
        , 'sltiu'
        , 'sh'
        , 'sw'
        , 'xori'
        , 'lwl' 
        , 'lwr' 
        , 'swl' 
        , 'swr']

#J-type
Jtype = [ 'j'
        , 'jal']




#Instruction of R-Type
ADD_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100000'}
ADDU_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100001'}
AND_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100100'}
DIV_INSTRUCTION = {'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '011010'}
DIVU_INSTRUCTION = {'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '011011'}
JALR_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'opcode': '000000'
                 , 'function': '001001'}
JR_INSTRUCTION = {'rs': ''
                 , 'opcode': '000000'
                 , 'function': '001000'}
MFHI_INSTRUCTION = {'rd': ''
                 , 'opcode': '000000'
                 , 'function': '010000'}
MFLO_INSTRUCTION = {'rd': ''
                 , 'opcode': '000000'
                 , 'function': '010010'}
MTHI_INSTRUCTION = {'rs': ''
                 , 'opcode': '000000'
                 , 'function': '010001'}
MTLO_INSTRUCTION = {'rs': ''
                 , 'opcode': '000000'
                 , 'function': '010011'}
MULT_INSTRUCTION = {'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '011000'}
MULTU_INSTRUCTION = {'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '011001'}
NOR_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100111'}
OR_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100101'}
SLL_INSTRUCTION = {'rd': ''
                 , 'rt': ''
                 , 'sa': ''
                 , 'opcode': '000000'
                 , 'function': '000000'}
SLLV_INSTRUCTION = {'rd': ''
                 , 'rt': ''
                 , 'rs': ''
                 , 'opcode': '000000'
                 , 'function': '000100'}
SLT_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '101010'}
SLTU_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '101011'}
SRA_INSTRUCTION = {'rd': ''
                 , 'rt': ''
                 , 'sa':''
                 , 'opcode': '000000'
                 , 'function': '000011'}
SRAV_INSTRUCTION = {'rd': ''
                 , 'rt': ''
                 , 'rs':''
                 , 'opcode': '000000'
                 , 'function': '000111'}
SRL_INSTRUCTION = {'rd': ''
                 , 'rt': ''
                 , 'sa':''
                 , 'opcode': '000000'
                 , 'function': '000010'}
SRLV_INSTRUCTION = {'rd': ''
                 , 'rt': ''
                 , 'rs': ''
                 , 'opcode': '000000'
                 , 'function': '000110'}
SUB_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100010'}
SUBU_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt':''
                 , 'opcode': '000000'
                 , 'function': '100011'}
SYSCALL_INSTRUCTION = {'opcode': '000000'
                 , 'function': '001100'}
XOR_INSTRUCTION = {'rd': ''
                 , 'rs': ''
                 , 'rt': ''
                 , 'opcode': '000000'
                 , 'function': '100110'}


#Instruction of I-Type
ADDI_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001000'}
ADDIU_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001001'}
ANDI_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001100'}
BEQ_INSTRUCTION = {'rs': ''
                 , 'rt': ''
                 , 'immediate': ''
                 , 'opcode': '000100'}
BGEZ_INSTRUCTION = {'rs': ''
                 , 'immediate': ''
                 , 'rt': '00001'
                 , 'opcode': '000001'}
BGTZ_INSTRUCTION = {'rs': ''
                 , 'immediate': ''
                 , 'rt': '00000'
                 , 'opcode': '000111'}
BLEZ_INSTRUCTION = {'rs': ''
                 , 'immediate': ''
                 , 'rt': '00000'
                 , 'opcode': '000110'}
BLTZ_INSTRUCTION = {'rs': ''
                 , 'immediate': ''
                 , 'rt': '00000'
                 , 'opcode': '000001'}
BNE_INSTRUCTION = {'rs': ''
                 , 'rt': ''
                 , 'immediate': ''
                 , 'opcode': '000101'}
LB_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100000'}
LBU_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100100'}
LH_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100001'}
LHU_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100101'}
LUI_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '001111'}
LW_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100011'}
ORI_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001101'}
SB_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '101000'}
SLTI_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001010'}
SLTIU_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001011'}
SH_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '101001'}
SW_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '101011'}
XORI_INSTRUCTION = {'rt': ''
                 , 'rs': ''
                 , 'immediate': ''
                 , 'opcode': '001110'}
LWL_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100010'}
LWR_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '100110'}
SWL_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '101010'}
SWR_INSTRUCTION = {'rt': ''
                 , 'immediate': ''
                 , 'opcode': '101110'}


J_INSTRUCTION = {'opcode': '000010'
                 , 'target': ''}
JAL_INSTRUCTION = {'opcode': '000011'
                 ,'target': ''}

#MIPS Register conventions
reg_num = ['$zero'
               , '$at'
               , '$v0'
               , '$v1'
               , '$a0'
               , '$a1'
               , '$a2'
               , '$a3'
               , '$t0'
               , '$t1'
               , '$t2'
               , '$t3'
               , '$t4'
               , '$t5'
               , '$t6'
               , '$t7'
               , '$s0'
               , '$s1'
               , '$s2'
               , '$s3'
               , '$s4'
               , '$s5'
               , '$s6'
               , '$s7'
               , '$t8'
               , '$t9'
               , '$k0'
               , '$k1'
               , '$gp'
               , '$sp'
               , '$fp'
               , '$ra']

R_cd = {'100000': 'add'
            , '100001': 'addu'
            , '100100': 'and'
            , '011010': 'div'
            , '011011': 'divu'
            , '001001': 'jalr'
            , '001000': 'jr'
            , '010000': 'mfhi'
            , '010010': 'mflo'
            , '010001': 'mthi'
            , '010011': 'mtlo'
            , '011000': 'mult'
            , '011001': 'multu'
            , '100111': 'nor'
            , '100101': 'or'
            , '000000': 'sll'
            , '000100': 'sllv'
            , '101010': 'slt'
            , '101011': 'sltu'
            , '000011': 'sra'
            , '000111': 'srav'
            , '000010': 'srl'
            , '000110': 'srlv'
            , '100010': 'sub'
            , '100011': 'subu'
            , '001100': 'syscall'
            , '100110': 'xor'}

I_cd = {'001000': 'addi'
            , '001001': 'addiu'
            , '001100': 'andi'
            , '000100': 'beq'
            , '000001': 'bltz'
            , '000111': 'bgtz'
            , '000110': 'blez'
            , '000101': 'bne'
            , '100000': 'lb'
            , '100100': 'lbu'
            , '100001': 'lh'
            , '100101': ' lhu'
            , '001111': 'lui'
            , '100011': 'lw'
            , '001101': 'ori'
            , '101000': 'sb'
            , '001010': 'slti'
            , '001011': 'sltiu'
            , '101001': 'sh'
            , '101011': 'sw'
            , '001110': 'xori'
            , '100010': 'lwl'
            , '100110': 'lwr'
            , '101010': 'swl'
            , '101110': 'swr'}

# #test
# if __name__ == '__main__':
#     a = eval("NOR_INSTRUCTION")
#     print(reg_num.index('$at'))
#     print(a)