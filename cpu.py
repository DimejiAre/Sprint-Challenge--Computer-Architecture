"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000
        self.bt = {
            self.LDI: self.handle_ldi,
            self.PRN: self.handle_prn,
            self.MUL: self.handle_mul,
            self.HLT: self.handle_hlt,
            self.PUSH: self.handle_push,
            self.POP: self.handle_pop,
            self.CALL: self.handle_call,
            self.RET: self.handle_ret,
            self.ADD: self.handle_add
        }
    
    def handle_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        inc_size = (self.LDI >> 6) + 1
        return inc_size

    def handle_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        inc_size = (self.PRN >> 6) + 1
        return inc_size

    def handle_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
        inc_size = (self.MUL >> 6) + 1
        return inc_size

    def handle_push(self, operand_a, operand_b):
        sp = 7
        register = operand_a
        val = self.reg[register]
        self.reg[sp] -= 1
        print("reg[sp]", self.reg[sp])
        self.ram_write(self.reg[sp], val)
        inc_size = (self.PUSH >> 6) + 1
        return inc_size
    
    def handle_pop(self, operand_a, operand_b):
        sp = 7
        register = operand_a
        val = self.ram_read(self.reg[sp])

        self.reg[register] = val
        self.reg[sp] += 1
        inc_size = (self.POP >> 6) + 1
        return inc_size

    def handle_call(self, operand_a, operand_b):
        sp = 7
        val = self.pc + (self.CALL >> 6) + 1
        self.reg[sp] -= 1
        self.ram_write(self.reg[sp], val)

        register = operand_a
        self.pc = self.reg[register]
        inc_size = 0
        return inc_size
    
    def handle_ret(self,operand_a, operand_b):
        sp = 7
        val = self.ram_read(self.reg[sp])
        self.pc = val
        self.reg[sp] += 1
        inc_size = 0
        return inc_size

    def handle_add(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)
        inc_size = (self.MUL >> 6) + 1
        return inc_size

    def handle_hlt(self, operand_a, operand_b):
        sys.exit(1)


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = []

        if len(sys.argv) != 2:
            print("usage: 03-fileio02.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split('#')[0].strip()

                    if num == '':
                        continue

                    value = int(num, 2)
                    program.append(value)

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        running = True

        while running:

            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR in self.bt:
                inc_size = self.bt[IR](operand_a, operand_b)
                self.pc += inc_size
            else:
                raise Exception(f"Invalid instruction {hex(IR)} at address {hex(self.pc)}")


        """Run the CPU."""
        # running = True
        # inc_size = 0
        # self.pc = 0
        # sp = 7

        # while running:
        #     IR = self.ram[self.pc]

        #     if IR == self.LDI:
        #         operand_a = self.ram_read(self.pc + 1)
        #         operand_b = self.ram_read(self.pc + 2)
        #         self.reg[operand_a] = operand_b
        #         inc_size = (self.LDI >> 6) + 1
            
        #     elif IR == self.PRN:
        #         operand_a = self.ram_read(self.pc + 1)
        #         print(self.reg[operand_a])
        #         inc_size = (self.PRN >> 6) + 1

        #     elif IR == self.MUL:
        #         operand_a = self.ram_read(self.pc + 1)
        #         operand_b = self.ram_read(self.pc + 2)
        #         self.alu('MUL', operand_a, operand_b)
        #         inc_size = (self.MUL >> 6) + 1

        #     elif IR == self.PUSH:
        #         register = self.ram_read(self.pc + 1)
        #         val = self.reg[register]

        #         self.reg[sp] -= 1
        #         self.ram_write(self.reg[sp], val)
        #         inc_size = (self.PUSH >> 6) + 1

        #     elif IR == self.POP:
        #         register = self.ram_read(self.pc + 1)
        #         val = self.ram_read(self.reg[sp])

        #         self.reg[register] = val
        #         self.reg[sp] += 1
        #         inc_size = (self.POP >> 6) + 1

        #     elif IR == self.CALL:
        #         # val = self.pc + (self.CALL >> 6) + 1
        #         val = self.pc + 2
        #         self.reg[sp] -= 1
        #         self.ram_write(self.reg[sp], val)

        #         register = self.ram_read(self.pc + 1)
        #         self.pc = self.reg[register]
        #         inc_size = 0
            
        #     elif IR == self.RET:
        #         val = self.ram_read(self.reg[sp])
        #         self.pc = val
        #         self.reg[sp] += 1
        #         inc_size = 0

        #     elif IR == self.ADD:
        #         operand_a = self.ram_read(self.pc + 1)
        #         operand_b = self.ram_read(self.pc + 2)
        #         self.alu('ADD', operand_a, operand_b)
        #         inc_size = (self.MUL >> 6) + 1

            
        #     elif IR == self.HLT:
        #         running = False

        #     else:
        #         print("Invalid Instruction")
        #         running = False

        #     self.pc += inc_size
