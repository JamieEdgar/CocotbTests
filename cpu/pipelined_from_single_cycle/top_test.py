import cocotb
from cocotb.triggers import Timer
import numpy as np

DEBUG = 1

async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    if DEBUG==3:
        print(  "rstn", hex(dut.pc1.rstn.value),
                "pc_source", hex(dut.pc1.pc_source.value),
                "stall", hex(dut.pc1.stall.value)
            )
    if DEBUG==2:
        if dut.data_we == 1:
            print(  "rstn", hex(dut.pc1.rstn.value),
                    "pc_source", hex(dut.pc1.pc_source.value),
                    "stall", hex(dut.pc1.stall.value),
                    "data_we", dut.data_we.value,
                    "pc", int(dut.pc.value),
                    "instruction", hex(dut.instruction.value),
                    "instruction[31:26]", hex(int(int(dut.instruction.value)/2**26)),
                    "alu_out", int(dut.alu_out.value),
                )
    if DEBUG == 2:
        if dut.dm.memory[19] != 0:
            print("Memory 19 set!")
        if dut.data_we.value == 1:
            print("Data Write enabled", dut.data_we.value,
                  "alu_out", int(dut.alu_out.value),)

async def setup(dut):
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    await toggle_clk(dut)
    dut.rstn.value = 1

async def write_beq_tests(dut):
    dut.rstn = 0
    # jump 3 to 12 to 7 to 13
    for i in range(40):
        dut.pm_write_address.value = 4*i
        dut.pm_data_in.value = i+1
        dut.pm_write_en.value = 1
        if (i == 3):
            dut.pm_data_in.value = 0x10000008   # Skip 8 instructions
        if (i == 7):
            dut.pm_data_in.value = 0x1000000B   # Skip 11 instructions
        if (i == 12):
            dut.pm_data_in.value = 0x1000FFFA   # Go back 6 instructions
        if (i == 19):
            dut.pm_data_in.value = 0x1000FFEC   # Go back 20 instructions
        await toggle_clk(dut)
    dut.pm_write_en.value = 0
    dut.rstn = 1

def JumpInst(offset):
    result = 2 << 26 | offset
    print("jump", hex(result))
    return result

async def write_jump_tests(dut):
    # jumps 2 to 16 to 10 to 24 to 0
    dut.rstn.value = 0
    print("write_jump_tests")
    for i in range(40):
        dut.pm_write_address.value = 4*i
        dut.pm_data_in.value = i+1
        dut.pm_write_en.value = 1
        if (i == 2):
            dut.pm_data_in.value = JumpInst(16)
        if (i == 10):
            dut.pm_data_in.value = JumpInst(24)
        if (i == 16):
            dut.pm_data_in.value = JumpInst(10)
        if (i == 24):
            dut.pm_data_in.value = JumpInst(0)
        await toggle_clk(dut)
    dut.pm_write_en.value = 0
    dut.rstn.value = 1

def AddInst(rega, regb, regc):
    result =  0x0 << 26 | rega << 21 | regb << 16 | regc << 11 | 0x20
    print("add", hex(result))
    return result

def SubInst(rega, regb, regc):
    result =  0x0 << 26 | rega << 21 | regb << 16 | regc << 11 | 0x22
    print("sub", hex(result))
    return result

def AndInst(rega, regb, regc):
    result =  0x0 << 26 | rega << 21 | regb << 16 | regc << 11 | 0x24
    print("and", hex(result))
    return result

def OrInst(rega, regb, regc):
    result =  0x0 << 26 | rega << 21 | regb << 16 | regc << 11 | 0x25
    print("or", hex(result))
    return result

def AddiInst(rega, regb, immediate):
    result =  0x08 << 26 | rega << 21 | regb << 16 | immediate
    print("addi", hex(result), end = " ")
    return result

def BeqInst(rega, regb, offset):
    if offset < 0:
        immediate = 0x10000 + offset
    else:
        immediate = offset
    immediate = immediate & 0xFFFF
    result = 0x04 << 26 | rega << 21 | regb << 16 | immediate
    print("beq", hex(result), end = " ")
    return result

async def write_reg_tests(dut):
    dut.rstn.value = 0
    await toggle_clk(dut)
    for i in range(64):
        dut.pm_write_address.value = 4*i
        dut.pm_write_en.value = 1
        dut.pm_data_in.value = 0
        if (i % 32 != 0):
            dut.pm_data_in.value = AddiInst(i % 32, i % 32, i+1)
        if (DEBUG == 2): print("update", dut.update.value)
        await toggle_clk(dut)
    dut.pm_write_en.value = 0
    dut.rstn.value = 1

def SwInst(rega, regb, immed):
    result = 0x2b << 26 | rega << 21 | regb << 16 | immed
    print("SwInst", hex(result), "rega", rega, "regb", regb, "immed", immed)
    return result

async def write_sw_tests(dut):
    dut.rstn.value = 0
    dut.pm_write_address.value = 4
    await toggle_clk(dut)
    for i in range(1, 32):
        dut.pm_write_en.value = 1
        for j in range(2):
            if (j == 0):
                dut.pm_data_in.value = AddiInst(i, i, i)
            else:
                dut.pm_data_in.value = SwInst(i, i, i)
            await toggle_clk(dut)
            dut.pm_write_address.value = dut.pm_write_address.value + 4
        if (DEBUG == 2): print("update", dut.update.value)

    dut.pm_write_en.value = 0
    dut.rstn.value = 1

def LwInst(rega, regb, immed):
    result = 0x23 << 26 | rega << 21 | regb << 16 | immed
    print("LwInst", hex(result), "rega", rega, "regb", regb, "immed", immed)
    return result

async def write_lw_tests(dut):
    dut.rstn.value = 0
    dut.pm_write_address.value = 4
    await toggle_clk(dut)
    for i in range(1, 32):
        dut.pm_write_en.value = 1
        dut.pm_data_in.value = LwInst(0, i, i)
        await toggle_clk(dut)
        dut.pm_write_address.value = dut.pm_write_address.value + 4
        if (DEBUG == 2): print("update", dut.update.value)
    dut.pm_write_en.value = 0
    dut.rstn.value = 1

async def write_add_tests(dut):
    for i in range(40):
        dut.pm_write_address.value = 4*i
        dut.pm_data_in.value = i+1
        dut.pm_write_en.value = 1
        if (i == 4):
            dut.pm_data_in.value = AddInst(1, 2, 3)
        if (i == 8):
            dut.pm_data_in.value = AddInst(3, 4, 5)
        await toggle_clk(dut)
    dut.pm_write_en.value = 0

async def write_add_sub_and_or_tests(dut):
    dut.rstn.value = 0
    for i in range(32,132):
        dut.pm_write_address.value = 4*i
        dut.pm_data_in.value = i+1
        dut.pm_write_en.value = 1
        rega = 1 + i % 31
        regb = 1 + ((i+1) % 31)
        regc = 1 + ((i+2) % 31)
        if (i % 4 == 0):
            dut.pm_data_in.value = AddInst(rega, regb, regc)
        if (i % 4 == 1):
            dut.pm_data_in.value = SubInst(rega, regb, regc)
        if (i % 4 == 2):
            dut.pm_data_in.value = AndInst(rega, regb, regc)
        if (i % 4 == 3):
            dut.pm_data_in.value = OrInst(rega, regb, regc)
        await toggle_clk(dut)
    dut.pm_write_en.value = 0
    dut.rstn.value = 1

def get_reg_values(dut):
    result = []
    for i in range(32):
        value = int(dut.reg1.registers[i])
        if (value & 0x80000000):
            value = value - 0x100000000
        result.append(value)
    return result

def get_reg_set(dut):
    inst = dut.instruction.value
    reg_a = int((inst >> 21) & 0x1F)
    reg_b = int((inst >> 16) & 0x1F)
    reg_c = int((inst >> 11) & 0x1F)
    return reg_a, reg_b, reg_c

def print_add_values(dut):
    reg_values = get_reg_values(dut)
    reg_a, reg_b, reg_c = get_reg_set(instruction)
    print("reg_a", reg_a, reg_values[reg_a],
          "reg_b", reg_b, reg_values[reg_b],
          "reg_c", reg_c, reg_values[reg_c],
          "sum", reg_values[reg_a] + reg_values[reg_b]
          )

async def check_add(dut):
    reg_values = get_reg_values(dut)
    reg_a, reg_b, reg_c = get_reg_set(dut)
    sum_val = reg_values[reg_a] + reg_values[reg_b]
    print("update", dut.update.value,
          "reg_a", reg_a, reg_values[reg_a], hex(reg_values[reg_a]),
          "reg_b", reg_b, reg_values[reg_b], hex(reg_values[reg_b]),
          "sum", sum_val, end=" "
          )
    await toggle_clk(dut)
    reg_values = get_reg_values(dut)
    print("reg_c", reg_c, reg_values[reg_c])
    assert sum_val == reg_values[reg_c]

async def check_sub(dut):
    reg_values = get_reg_values(dut)
    reg_a, reg_b, reg_c = get_reg_set(dut)
    dif_val = reg_values[reg_a] - reg_values[reg_b]
    print("update", dut.update.value,
          "reg_a", reg_a, reg_values[reg_a], hex(reg_values[reg_a]),
          "reg_b", reg_b, reg_values[reg_b], hex(reg_values[reg_b]),
          "dif", dif_val, end=" "
          )
    await toggle_clk(dut)
    reg_values = get_reg_values(dut)
    print("reg_c", reg_c, reg_values[reg_c])
    assert dif_val == reg_values[reg_c]

async def check_and(dut):
    reg_values = get_reg_values(dut)
    reg_a, reg_b, reg_c = get_reg_set(dut)
    and_val = reg_values[reg_a] & reg_values[reg_b]
    print("update", dut.update.value,
          "reg_a", reg_a, reg_values[reg_a], hex(reg_values[reg_a]),
          "reg_b", reg_b, reg_values[reg_b], hex(reg_values[reg_b]),
          "and", and_val, end=" "
          )
    await toggle_clk(dut)
    reg_values = get_reg_values(dut)
    print("reg_c", reg_c, reg_values[reg_c])
    assert and_val == reg_values[reg_c]

async def check_or(dut):
    reg_values = get_reg_values(dut)
    reg_a, reg_b, reg_c = get_reg_set(dut)
    or_val = reg_values[reg_a] | reg_values[reg_b]
    print("update", dut.update.value,
          "reg_a", reg_a, reg_values[reg_a], hex(reg_values[reg_a]),
          "reg_b", reg_b, reg_values[reg_b], hex(reg_values[reg_b]),
          "or", or_val, end=" "
          )
    await toggle_clk(dut)
    reg_values = get_reg_values(dut)
    print("reg_c", reg_c, reg_values[reg_c])
    assert or_val == reg_values[reg_c]

def print_addi_values(dut):
    reg_values = get_reg_values(dut)
    print(reg_values)
    inst = dut.instruction.value
    reg_a = int((inst >> 21) & 0x1F)
    reg_b = int((inst >> 16) & 0x1F)
    immed = int(inst & 0xFFFF)
    print("reg_a", reg_a, reg_values[reg_a],
          "immed", immed,
          "reg_b", reg_b, reg_values[reg_b],
          "update", dut.update.value,
          "rd", dut.rd.value,
          "alu_out", int(dut.alu_out.value)
         )

def print_sw_values(dut):
    reg_values = get_reg_values(dut)
    print(reg_values)
    inst = dut.instruction.value
    reg_a = int((inst >> 21) & 0x1F)
    reg_b = int((inst >> 16) & 0x1F)
    immed = int(inst & 0xFFFF)
    print("reg_a", reg_a, reg_values[reg_a],
          "immed", immed,
          "reg_b", reg_b, reg_values[reg_b],
          "update", dut.update.value,
          "rd", dut.rd.value,
          "alu_a", int(dut.alu_a.value),
          "alu_b", int(dut.alu_b.value),
          "alu_out", int(dut.alu_out.value),
          "data_we", dut.data_we.value,
          "dm_data_in", int(dut.dm_data_in.value)
         )
def print_lw_values(dut):
    reg_values = get_reg_values(dut)
    print(reg_values)
    inst = dut.instruction.value
    reg_a = int((inst >> 21) & 0x1F)
    reg_b = int((inst >> 16) & 0x1F)
    immed = int(inst & 0xFFFF)
    print("reg_a", reg_a, reg_values[reg_a],
          "immed", immed,
          "reg_b", reg_b, reg_values[reg_b],
          "update", dut.update.value,
          "rd", dut.rd.value,
          "alu_a", int(dut.alu_a.value),
          "alu_b", int(dut.alu_b.value),
          "dm_data_out", int(dut.dm_data_out.value),
          "din", int(dut.din.value),
          "dm_data_in", int(dut.dm_data_in.value)
         )

def get_dm_values(dut, start, end):
    result = []
    for i in range(start, end):
        result.append(int(dut.dm.memory[i]))
    return result

def check_sw_values(dut):
    dm_values = get_dm_values(dut, 0, 255)
    print("dm_values", dm_values)
    for i in range(32):
        assert dm_values[2*i] == i


def get_instruction(binary):
    inst = (binary >> 26)
    function = binary % 2**6
    if inst == 0x00:
        if function == 0x20:
            return "ADD"
        if function == 0x24:
            return "AND"
        if function == 0x25:
            return "OR"
        if function == 0x22:
            return "SUB"
    if inst == 0x08:
        return "ADDI"
    if inst == 0x04:
        return "BEQ"
    if inst == 0x23:
        return "LW"
    if inst == 0x02:
        return "JUMP"
    if inst == 0x2B:
        return "SW"
    return "unknown"

def print_instruction(dut):
    binary = dut.instruction.value
    print(hex(binary))
    reg_a, reg_b, reg_c = get_reg_set(dut)
    immed = binary & 0xFFFF
    inst = (binary >> 26)
    function = binary % 2**6
    if inst == 0x00:
        if function == 0x20:
            print("ADD", reg_a, reg_b, reg_c)
        if function == 0x24:
            print("AND")
        if function == 0x25:
            print("OR")
        if function == 0x22:
            print("SUB")
    if inst == 0x08:
        print("ADDI", reg_a, reg_b, immed)
    if inst == 0x04:
        print("BEQ", reg_a, reg_b, "zero", dut.zero.value, "ds_pre",
              int(dut.ds_pre.value), "dt_pre", int(dut.dt_pre.value))
    if inst == 0x23:
        print("LW", reg_a, reg_b, immed)
    if inst == 0x02:
        print("JUMP")
    if inst == 0x2B:
        print("SW", reg_a, reg_b, immed)
    #print("unknown")

async def check_beq_test(dut):
    print("check_beq_test")
    jump_address = None
    for i in range(50):
        await toggle_clk(dut)
        print_pipeline_details(dut)
        if (jump_address != None):
            print("pc before assert", int(dut.pc.value))
            assert dut.pc.value == jump_address
            print("Jumped to", jump_address)
            jump_address = None
        if get_instruction(dut.instruction.value) == "BEQ":
            offset = (int(dut.instruction.value) % 2**16) * 4
            if (offset & 0x20000):
                offset = offset - 0x40000
            print("BEQ", int(offset), "pc", int(dut.pc.value))
            jump_address = dut.pc.value + offset # Note that PC has already been incremented

async def check_add_sub_and_or_tests(dut):
    print("check_add_sub_and_or_tests")
    for i in range(100):
        toggled = False
        if get_instruction(dut.instruction.value) == "ADD":
            print("ADD", end=" ")
            await check_add(dut)
            toggled = True
        if get_instruction(dut.instruction.value) == "SUB":
            print("SUB", end=" ")
            await check_sub(dut)
            toggled = True
        if get_instruction(dut.instruction.value) == "AND":
            print("AND", end=" ")
            await check_and(dut)
            toggled = True
        if get_instruction(dut.instruction.value) == "OR":
            print("OR", end=" ")
            await check_or(dut)
            toggled = True
        if toggled == False:
            await toggle_clk(dut)

async def check_jump_test(dut):
    print("check_jump_test")
    jump_address = None
    for i in range(50):
        await toggle_clk(dut)
        print_pipeline_details(dut)
        if (jump_address != None):
            print("pc before assert", int(dut.pc.value))
            assert dut.pc.value == jump_address
            print("Jumped to", jump_address)
            jump_address = None
        if get_instruction(dut.instruction.value) == "JUMP":
            jump_address = (int(dut.instruction.value) % 2**26) * 4
            print("JUMP", jump_address, "pc", int(dut.pc.value))

async def check_reg_values(dut):
    await setup(dut)
    reg_values = get_reg_values(dut)
    print("reg_values", get_reg_values(dut))
    for i in range(32):
        assert reg_values[i] == 0
    for i in range(32+4):
        print_pipeline_details(dut)
        await toggle_clk(dut)
    reg_values = get_reg_values(dut)
    print("reg_values", get_reg_values(dut))
    for i in range(32):
        if i == 0:
            assert reg_values[i] == 0
        else:
            assert reg_values[i] == i + 1
    print("reg values correct")

async def check_instructions(dut):
    for i in range(10):
        await toggle_clk(dut)
        if DEBUG == 1:
            print("pc", hex(dut.pc.value),
                "instruction", i, hex(dut.instruction.value),
                "jump", dut.jump.value,
                "zero", dut.zero.value, end=" ")
        if DEBUG == 1:
            inst = get_instruction(dut.instruction.value)
            print("inst", inst)
            if (inst == "ADD"):
                print("Add", end = " ")
                print_add_values(dut)
            if (inst == "ADDI"):
                print("ADDI", end = " ")
                print_addi_values(dut)
            if (inst == "SW"):
                print("SW", end = " ")
                print_sw_values(dut)
            if (inst == "LW"):
                print("LW", end=" ")
                print_lw_values(dut)
        print("")

async def test_beq_inst(dut):
    await write_beq_tests(dut)
    await setup(dut)
    await check_beq_test(dut)

async def test_jump_inst(dut):
    await write_jump_tests(dut)
    await setup(dut)
    await check_jump_test(dut)

async def test_addi_inst(dut):
    #await write_add_tests(dut)
    await write_reg_tests(dut)
    print("reg_values", get_reg_values(dut))
    await setup(dut)
    print("reg_values", get_reg_values(dut))
    await check_reg_values(dut)
    await check_instructions(dut)

async def test_sw_inst(dut):
    await setup(dut)
    await write_sw_tests(dut)
    for i in range(160):
        print_pipeline_details(dut)
        await toggle_clk(dut)
    check_sw_values(dut)

async def test_add_sub_and_or_inst(dut):
    await setup(dut)
    await write_add_sub_and_or_tests(dut)
    await check_add_sub_and_or_tests(dut)

async def load_data(dut, mem_range, values):
    print("load data")
    dut.rstn.value = 0
    for i in range(len(mem_range)):
        dut.dm_write_en.value = 1
        dut.dm_write_address_load.value = mem_range[i]
        dut.dm_data_in_load.value = values[i]
        await toggle_clk(dut)
    dut.dm_write_en.value = 0
    dut.rstn.value = 1


async def test_lw_inst(dut):
    clear_registers(dut)
    await setup(dut)
    mem_range = []
    values = []
    for i in range(1, 32):
        mem_range.append(i)
        values.append(i*10)
    await load_data(dut, mem_range, values)
    dm_values = get_dm_values(dut, 1, 31)
    print("dm_values", dm_values)
    print("reg_values", get_reg_values(dut))
    await write_lw_tests(dut)
    for i in range(32+4):
        print_pipeline_details(dut)
        await toggle_clk(dut)
    reg_values = get_reg_values(dut)
    print("reg_values", reg_values)
    for i in range(32):
        assert reg_values[i] == 10*i

instruction_count = 0

async def add_instruction(dut, inst, r1, r2, r3, immed):
    global instruction_count
    added = False
    if inst == "ADD":
        dut.pm_data_in.value = AddInst(r1, r2, r3)
        added = True
    if inst == "ADDI":
        dut.pm_data_in.value = AddiInst(r1, r2, immed)
        added = True
    if inst == "BEQ":
        dut.pm_data_in.value = BeqInst(r1, r2, immed)
        added = True
    if added == True:
        dut.pm_write_address.value = 4*instruction_count
        dut.pm_write_en.value = 1
        await toggle_clk(dut)
        instruction_count += 1
        dut.pm_write_en.value = 0

def print_pipeline_details(dut):
    print("")
    print_instruction(dut)
    for j in range(5):
        print("reg_busy", dut.register_busy.value[j], end=" ")
    print("")
    print("reg_values", get_reg_values(dut))
    print("stall", dut.stall.value,
              "pc", int(dut.pc.value),
              "immediate", dut.immediate.value)
    print("select", hex(dut.select.value),
              "alu_a", int(dut.alu_a.value),
              "alu_b", int(dut.alu_b.value))
    print(  "rs", int(dut.rs.value),
            "rt", int(dut.rt.value),
            "ds", int(dut.ds.value),
            "dt", int(dut.dt.value),
            "rd", int(dut.rd.value),
            "rd_d2", int(dut.rd_d2.value),
            "rd_d1", int(dut.rd_d1.value),
            "rd_d", int(dut.rd_d.value),)
    print("update", dut.update.value,
          "update_pre", dut.update_pre.value,
          "dut_update_pre2", dut.update_pre2.value,
          "dut_update_pre3", dut.update_pre3.value)
    print("din", int(dut.din.value),
              "alu_out_pre", int(dut.alu_out_pre.value),
              "alu_out", int(dut.alu_out.value),)
    print("data_we", dut.data_we.value,
          "dm_write_address", int(dut.dm_write_address.value),
          "dm_data_in", int(dut.dm_data_in.value),
          "dt", int(dut.dt.value),
          "dt_pre", int(dut.dt_pre.value),
          "rt", int(dut.reg1.rt.value)
          )
    print(  "dm_read_address", hex(dut.dm.read_address.value),
            "dm_data_out", int(dut.dm_data_out.value)
            )


# This test should cause stalls in a pipelined processor
# In the single cycle processor, it should always pass
async def pipeline_test(dut):
    global instruction_count
    await clear_registers(dut)
    instruction_count = 0
    dut.rstn.value = 0
    await add_instruction(dut, "ADDI", 0, 1, 0, 1)
    for i in range(2, 17):
        await add_instruction(dut, "ADD", i-1, 1, i, 0)
    await add_instruction(dut, "BEQ", 0, 0, 0, -1)
    dut.rstn.value = 1
    print("reg_values", get_reg_values(dut))
    for i in range(60):
        print_pipeline_details(dut)
        await toggle_clk(dut)
    register_values = get_reg_values(dut)
    print("reg_values", register_values)
    for i in range(16):
        assert register_values[i] == i
    print("pipeline test passed")

async def clear_registers(dut):
    global instruction_count
    instruction_count = 0
    dut.rstn.value = 0
    for i in range(1, 32):
        await add_instruction(dut, "ADD", 0, i, 0, 0)
    dut.rstn.value = 1
    for i in range(32):
        await toggle_clk(dut)

async def all_tests(dut):
    await test_addi_inst(dut)       # addi
    await test_sw_inst(dut)         # sw
    await test_lw_inst(dut)         # lw
    await test_jump_inst(dut)       # jump
    await test_beq_inst(dut)        # beq

    await test_add_sub_and_or_inst(dut) # registers should have values first

    await pipeline_test(dut)

@cocotb.test()
async def my_first_test(dut):

    await all_tests(dut)

    for i in range(30):
        await toggle_clk(dut)

