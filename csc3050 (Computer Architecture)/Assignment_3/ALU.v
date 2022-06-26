module alu(instruction, regA, regB, result, flags);             


input[31:0] instruction, regA, regB;                                                     

output signed[31:0] result;                     
output signed[2:0] flags;


reg[5:0] opcode, func;
reg signed[32:0] overflow;                 
reg signed[2:0] flag;
reg[15:0] immediate;

reg[31:0] reg_A, reg_B, reg_C;                        
reg[31:0] temp_A, temp_B;                                     

reg of = 0; //overflow
reg nf = 0; //negative
reg zf = 0; //zero

// Func (R Types, opcode = 000000)
parameter 
    add = 6'b100000
    ,addu = 6'b100001
    ,sub = 6'b100010
    ,subu = 6'b100011

    ,and_ = 6'b100100
    ,nor_ = 6'b100111
    ,or_ = 6'b100101
    ,xor_ = 6'b100110

    ,slt = 6'b101010
    ,sltu = 6'b101011

    ,sll = 6'b000000
    ,sllv = 6'b000100
    ,sra = 6'b000011
    ,srav = 6'b000111
    ,srl = 6'b000010
    ,srlv = 6'b000110;

//Opcodes
parameter 
    beq = 6'b000100
    ,bne = 6'b000101

    ,addi =6'b001000
    ,addiu = 6'b001001

    ,andi = 6'b001100
    ,ori = 6'b001101
    ,xori = 6'b001110
    ,slti = 6'b001010
    ,sltiu = 6'b001011

    ,lw = 6'b100011
    ,sw = 6'b101011;


always @(instruction,reg_A)
begin

opcode = instruction[31:26];
func = instruction[5:0];

//registers
case(instruction[25:21])
    5'b00000:
    begin
        reg_A = regA;
    end

    5'b00001:
    begin
        reg_A = regB;
    end
    endcase

case(instruction[20:16])
    5'b00000:
    begin
        reg_B = regA;
    end

    5'b00001:
    begin
        reg_B = regB;
    end
    endcase

//R type
case(opcode)
6'b000000:
begin
    flag = 3'b000;

    case(func)
    add:
    begin
        reg_C = reg_A + reg_B;
        overflow = reg_A + reg_B;
    end

    addu:
    begin
        reg_C = reg_A + reg_B;
    end
    

    sub:
    begin
        reg_C = reg_A - reg_B;
        overflow = reg_A + reg_B;
    end

    subu:
    begin
        reg_C = reg_A - reg_B;
    end

    and_:
    begin
        reg_C = reg_A & reg_B;
    end

    nor_:
    begin
        reg_C = ~(reg_A | reg_B);
    end

    or_:
    begin
        reg_C = (reg_A | reg_B);
    end

    xor_:
    begin
        reg_C = (reg_A ^ reg_B);
    end
    
    slt:
    begin
        temp_A = reg_A;
        temp_B = reg_B;
        reg_C = 32'b0;

        if (temp_A < temp_B)
        begin
            reg_C = 32'b1;
            nf = 1'b1;
        end
    end

    sltu:
    begin
        reg_C = 32'b0;

        if (reg_A < reg_B)
        begin
            reg_C = 32'b1;
            nf = 1'b1;
        end
    end

    sll:
    begin
        reg_C = reg_B << instruction[10:6];
    end

    sllv:
    begin
        reg_C = reg_B << reg_A;
    end

    srl:
    begin
        reg_C = reg_B >> instruction[10:6];
    end

    srlv:
    begin
        reg_C = reg_B >> reg_A;
    end

    sra:
    begin
        reg_C = reg_B >>> instruction[10:6];
    end

    srav:
    begin
        reg_C = reg_B >>> reg_A;
    end
    endcase    
end
endcase

//I type
case(opcode)

    addi:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        reg_C = reg_A + immediate;
        overflow = reg_A + immediate;
    end

    addiu:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        reg_C = reg_A + immediate;
    end

    andi:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        reg_C = reg_A & immediate;
    end

    ori:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];
        
        reg_C = reg_A | immediate;
    end 

    xori:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];
        
        reg_C = reg_A ^ immediate;
    end

    slti:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        temp_A = reg_A;
        temp_B = immediate;
        reg_C = 32'b0;

        if (temp_A < temp_B)
        begin
            reg_C = 32'b1;
            nf = 1'b1;
        end
    end

    sltu:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        reg_C = 32'b0;

        if (reg_A < immediate)
        begin
            reg_C = 32'b1;
            nf = 1'b1;
        end    
    end

    beq:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        reg_C = 32'b0;

        if(reg_A == reg_B)
        begin
            zf = 1'b1;
            reg_C = instruction[15:0];
        end
    end

    bne:
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        reg_C = 32'b0;

        if(reg_A != reg_B)
        begin
            zf = 1'b1;
            reg_C = instruction[15:0];
        end
    end


    lw:
    begin
        reg_C = instruction[15:0];
    end

    sw:
    begin
        reg_C = instruction[15:0];
    end
endcase

end

assign result = reg_C[31:0];
assign flags[0] = zf;
assign flags[1] = nf;
assign flags[2] = of;

endmodule

//iverilog -o out ALU.v