import xlrd
import sys
import os
import re
from memory_class import *
from ram_wrapper import *


def proc(list):
    mem_file = list[0]
    print(mem_file)
    if not os.path.exists(mem_file):
        sys.exit("ERROR! file: %s do not exist!" % mem_file)

    build_mem_list(mem_file)


def build_mem_list(mem_file):
    sp_mem_list = []
    tp_mem_list = []
    dp_mem_list = []
    workbook = xlrd.open_workbook(mem_file)
    sheet_list = workbook.sheets()
    sheet = sheet_list[0]
    row_num = sheet.nrows
    col_num = sheet.ncols
    print(row_num)
    print(col_num)

    for x in range(1, row_num):  # without title
        mem_name = sheet.cell(x, 0).value
        mem_stype = sheet.cell(x, 1).value
        mem_dwidth = sheet.cell(x, 2).value
        mem_awidth = sheet.cell(x, 3).value
        mem_depth = sheet.cell(x, 4).value
        mem_ptype = sheet.cell(x, 5).value
        mem_pwr = sheet.cell(x, 6).value
        mem_prd = sheet.cell(x, 7).value
        mem = c_lib_memory(mem_name, mem_stype, mem_dwidth, mem_awidth, mem_depth, mem_ptype, mem_pwr, mem_prd)
        print(mem.get_info())
        if re.match("sp", mem.get_stype(), flags=re.IGNORECASE):
            sp_mem_list.append(mem)
        if re.match("tp", mem.get_stype(), flags=re.IGNORECASE):
            tp_mem_list.append(mem)
        if re.match("dp", mem.get_stype(), flags=re.IGNORECASE):
            dp_mem_list.append(mem)
    content = write_wrapper_file(ram_dp_wrapper_head, dp_mem_list, "dp")
    write_file("ram_dp.v",content)
    content = write_wrapper_file(ram_sp_wrapper_head, sp_mem_list, "sp")
    write_file("ram_sp.v",content)


def write_wrapper_file(wrapper_head, mem_list, mem_type):
    ostring = wrapper_head + "\n"
    ostring = ostring + "generate\n"
    for index, mem in enumerate(mem_list):
        ins_name = mem_type+("_data%d_addr%d_depth%d_pwr%d_prd%d"
                    % (mem.get_dwidth(), mem.get_awidth(), mem.get_depth(), mem.get_pwr(), mem.get_prd()))
        if (index > 0):
            ostring = ostring + "else "
        ostring = ostring + (
                    "if((DATA==%d) & (ADDR==%d) & (DEPTH==%d) & (PIPELINE_WR == %d) & (PIPELINE_RD==%d)) begin:"
                    % (mem.get_dwidth(), mem.get_awidth(), mem.get_depth(), mem.get_pwr(), mem.get_prd()))+ins_name+"\n"
        if (re.match("uhd", mem.get_ptype())):
            ostring = ostring + "\torbbec_ram_uhd_" + mem_type + " #(\n"
        else:
            ostring = ostring + "\torbbec_ram_" + mem_type + " #(\n"
        if(mem_type == "dp"):
            ostring = ostring + ram_para_dp
        else:
            ostring = ostring + ram_para_sp
        if (re.match("uhd", mem.get_ptype())):
            ostring = ostring + "\t) u_orbbec_ram_uhd_"
        else:
            ostring = ostring + "\t) u_orbbec_ram_"
        ostring = ostring + ins_name + " (\n"
        if(mem_type == "dp"):
            ostring = ostring + ram_port_dp
        else:
            ostring = ostring + ram_port_sp
        ostring = ostring + "\t);\n"
        ostring = ostring + "end\n"
    ostring = ostring + "`endif//ASIC_MEM\n"
    ostring = ostring + "`endmodule\n"
    if(mem_type == "DP"):
        ostring = ostring + "`endif//RAM_DP__CTL\n"
    else:
        ostring = ostring + "`endif//RAM_DP__CTL\n"
    print(ostring)
    return ostring

def write_file(file_name,content):
    file = open(file_name,mode='w')
    file.write(content)
    file.close()


def main():
    if (len(sys.argv) <= 1):
        sys.exit("ERROR! No input File!")
    else:
        proc(sys.argv[1:])


if __name__ == '__main__':
    main()
