module alu(instruction, regA, regB, result, flags);

input signed[31:0] instruction, regA, regB;

output signed[31:0] result;
output signed[2:0] flags;

reg[5:0] opcode, func;
reg signed[32:0] overflow;
reg signed[2:0] flag;
reg [15:0] immediate;

reg signed[31:0] reg_A, reg_B, reg_C;
reg [31:0] temp_A, temp_B;
reg signed[31:0] reg1, reg2;

reg of = 0; //overflow
reg nf = 0; //negative
reg zf = 0; //zero

//----------------------------------------

always @(regA,regB)
begin
    opcode = instruction[31:26];
    func = instruction[5:0];
    reg1 = regA;
    reg2 = regB;
    immediate = instruction[15:0];

    if(opcode==6'b000000) // R type
    begin
        flag = 3'b000;

        if(func==6'b100000 || func==6'b100001) // add, addu
            reg_C = reg1 + reg2;

        else if(func==6'b100010 || func==6'b100011) // sub, subu
            reg_C = reg1 - reg2;

        else if(func==6'b100100) // and
            reg_C = reg1 & reg2;

        else if(func==6'b100111) // nor
            reg_C = ~(reg1 || reg2);

        else if(func==6'b100101) // or
            reg_C = reg1 || reg2;

        else if(func==6'b100110) // xor
            reg_C = reg1 ^ reg2;

        else if(func==6'b101010) // slt
        begin
            reg_A = reg1;
            reg_B = reg2;
            reg_C = 32'b0;

            if(reg_A < reg_B)
                begin
                nf = 1'b1;
                reg_C = 32'b1;
                end
        end

        else if(func==6'b101011) // sltu
        begin
            temp_A = reg1;
            temp_B = reg2;
            reg_C = 32'b0;

            if(temp_A < temp_B)
                begin
                nf = 1'b1;
                reg_C = 32'b1;
                end
        end

        else if(func==6'b000000) // sll
            reg_C = reg2 << instruction[10:6];

        else if(func==6'b000100) // sllv
            reg_C = reg2 << reg1;

        else if(func==6'b000010) // srl
            reg_C = reg2 >> instruction[10:6];

        else if(func==6'b000110) // srlv
            reg_C = reg2 >> reg1;

        else if(func==6'b000011) // sra
            reg_C = reg2 >>> instruction[10:6];

        else if(func==6'b000111) // srav
            reg_C = reg2 >>> reg1;
    end

    else if(opcode!=6'b000000) // I type
    begin
        flag = 3'b000;
        immediate = instruction[15:0];

        if(opcode==6'b001000 || opcode==6'b001001) //addi, addiu
            reg_C = reg1 + immediate;

        else if (opcode==6'b001100) // andi
            reg_C = reg1 && immediate;

        else if(opcode==6'b001101) // ori
            reg_C = reg1 | immediate;

        else if(opcode==6'b001110) // xori
            reg_C = reg1 ^ immediate;

        else if(opcode==6'b000100) // beq
        begin
            flag = 3'b000;
            immediate = instruction[15:0];

            reg_A = reg1;
            reg_B = reg2;
            reg_C = 32'b0;

            if(reg_A==reg_B)
            begin
                zf = 1'b1;
                reg_C= 32'b0 + instruction[15:0] + instruction[15:0] + instruction[15:0] + instruction[15:0];
            end
        end

        else if(opcode==6'b000101) //bne
        begin
            flag = 3'b000;
            immediate = instruction[15:0];

            reg_A = reg1;
            reg_B = reg2;
            reg_C = 32'b0;

            if(reg_A!=reg_B)
            begin
                zf = 1'b1;
                reg_C= 32'b0 + immediate + immediate + immediate + immediate;
            end
        end

        else if(opcode==6'b100011 || opcode==6'b101011) // lw 
            reg_C = 32'b0 + instruction[15:0];

        else if(opcode==6'b001010) // slti
        begin
            flag = 3'b000;
            immediate = instruction[15:0];

            reg_A = reg1;
            reg_B = 32'b0 + immediate;
            reg_C = 32'b0;

            if(reg_A < reg_B)
            begin
                nf = 1'b1;
                reg_C = 32'b1;
            end
        end 

        else if(opcode==6'b001011) // sltiu
        begin
            flag = 3'b000;
            immediate = instruction[15:0];

            reg_A = reg1;
            reg_B = 32'b0 + immediate;
            reg_C = 32'b0;
                
            if(temp_A < immediate)
            begin
                nf = 1'b1;
                reg_C = 0000_0000_0000_0000_0000_0000_0000_0001;
            end
        end
    end
end

assign result = 32'b0 + reg_C;
assign flags[0] = zf;
assign flags[1] = nf;
assign flags[2] = of;

endmodule