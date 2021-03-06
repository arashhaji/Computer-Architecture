"""CPU functionality."""
import sys  
HLT = 0b00000001
LDI = 0b10000010 
PRN = 0b01000111
MUL = 0b10100010 
PUSH = 0b01000101
POP = 0b01000110
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter, index of the current instruction 
        self.reg = [0] * 8 # 8 registers / like variables 
        self.ram = [0] * 256 #ram
        self.sp = 7
        self.reg[self.sp] = 0xF4 # Stack pointer starts at F4 or 244 in Ram 
        self.branchtable ={}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
    def ram_read(self, address ): # accept the address to read and return the value stored 
        return self.ram[address]
    def ram_write(self, value, address): # accept a value to write, and the address to write it to 
        self.ram[address] = value
    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]
        address = 0
        with open(filename) as filehandle:
            for line in filehandle:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                # self.ram[address] = v
                self.ram_write(v, address)
                address += 1
        # address = 0
        # # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    def handle_ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc +=3
    def handle_prn(self):
        print(self.reg[self.ram_read(self.pc +1)])
        self.pc += 2
    def handle_mul(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_1, reg_2)
        self.pc += 3
    # def handle_push(self):
    #     self.reg[self.sp] -=1 
    #     reg_1 = self.ram_read(self.pc + 1) 
    #     value = self.reg[reg_1]
    #     stack_address = self.reg[self.sp]
    #     self.ram_write(value, reg_1)
    #     self.pc +=2
    def handle_push(self):
        self.reg[self.sp] -=1 
        reg_1 = self.ram[self.pc + 1] 
        value = self.reg[reg_1]
        stack_address = self.reg[self.sp]
        self.ram[stack_address] = value
        self.pc +=2
    def handle_pop(self):
        if self.reg[self.sp] == 0xF4:
            return "Empty Stack"
        reg_1 = self.ram_read(self.pc + 1)
        self.reg[reg_1] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] +=1
        self.pc += 2
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
    def handle_hlt(self):
        self.pc += 1
        self.running = False
        return self.running
    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.ram[self.pc]
            if ir in self.branchtable:
                self.branchtable[ir]()
            else:
                print(f'Unknown instruction: {ir}, at address PC: {self.pc}')
                sys.exit(1)
        # HLT = 0b00000001
        # LDI = 0b10000010
        # PRN = 0b01000111
        # running = True 
        # while running:
        #     IR = self.ram_read(self.pc)
        #     register_1 = self.ram_read(self.pc + 1)
        #     register_2 = self.ram_read(self.pc + 2)
        # if IR == HLT:
        #     running = False
        #     self.pc +=1
        # elif IR == LDI:
        #     self.registers[register_1] = register_2
        #     self.pc +=3
        # elif IR == PRN:
        #     print(self.registers[register_1])
        #     self.pc +=2
        # else:
        #     print(f"bad input: {bin(IR)}")
        #     running = False 
        # ir = LDI
        # self.branchtable[ir]()
        # ir = LDI
        # self.branchtable[ir]()
        # ir = MUL
        # self.branchtable[ir]()
        # ir = PRN
        # self.branchtable[ir]()