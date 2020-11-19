ram_dp_wrapper_head = ""\
'`ifndef RAM_DP\n'\
'`define RAM_DP\n'\
'module ram_dp  #(\n'\
'    parameter   DATA        = 32,\n'\
'    parameter   ADDR        = 9,\n'\
'    parameter   DEPTH       = (2**ADDR),\n'\
'    parameter   PIPELINE_WR = 0,\n'\
'    parameter   PIPELINE_WR_DATA = PIPELINE_WR,\n'\
'    parameter   PIPELINE_RD = 1,\n'\
'    parameter   WARNINGS    = 1\n'\
') (\n'\
'    // write port\n'\
'    input   wire                write_clk,\n'\
'    input   wire                write_en,\n'\
'    input   wire    [ADDR-1:0]  write_addr,\n'\
'    input   wire    [DATA-1:0]  write_data,\n'\
'\n'\
'    //clock gate bypass\n'\
'    input   wire                cg_bypass,\n'\
'\n'\
'    // read port\n'\
'    input   wire                read_clk,\n'\
'    input   wire                read_en,\n'\
'    input   wire    [ADDR-1:0]  read_addr,\n'\
'    output  reg     [DATA-1:0]  read_data\n'\
');\n'\
'\n'\
'`ifdef SIM_RAM\n'\
'\n'\
'    reg write_en_ff;\n'\
'    reg [ADDR-1:0] write_addr_ff;\n'\
'    reg [DATA-1:0] write_data_ff;\n'\
'\n'\
'    always @(posedge  write_clk) begin\n'\
'        write_en_ff   <= write_en;\n'\
'        write_addr_ff <= write_addr;\n'\
'        write_data_ff <= write_data;\n'\
'    end\n'\
'\n'\
'    reg write_en_vld;\n'\
'    reg [ADDR-1:0] write_addr_vld;\n'\
'    reg [DATA-1:0] write_data_vld;\n'\
'    always @(*) begin\n'\
'        if(PIPELINE_WR == 1) begin\n'\
'            write_en_vld = write_en_ff;\n'\
'            write_addr_vld = write_addr_ff;\n'\
'            write_data_vld = write_data_ff;\n'\
'        end\n'\
'        else begin\n'\
'            write_en_vld = write_en;\n'\
'            write_addr_vld = write_addr;\n'\
'            write_data_vld = write_data;\n'\
'        end\n'\
'    end\n'\
'\n'\
'\n'\
'    reg [DATA-1:0] mem[0:DEPTH-1];\n'\
'    generate\n'\
'        genvar i;\n'\
'        for (i = 0; i < DEPTH; i=i+1) begin:mem_ins\n'\
'            always @(posedge  write_clk) begin\n'\
'                if(write_en_vld & (write_addr_vld == i))\n'\
'                    mem[i] <= write_data_vld;\n'\
'            end\n'\
'        end\n'\
'    endgenerate\n'\
'\n'\
'    reg [DATA-1:0] rdata_ff1;\n'\
'    reg [DATA-1:0] rdata_ff2;\n'\
'    always @(posedge read_clk) begin\n'\
'        if(read_en)\n'\
'            rdata_ff1 <= mem[read_addr];\n'\
'    end\n'\
'\n'\
'    always @(posedge read_clk) begin\n'\
'        rdata_ff2 <= rdata_ff1;\n'\
'    end\n'\
'\n'\
'    always @(*) begin\n'\
'        if(PIPELINE_RD == 2)\n'\
'            read_data = rdata_ff2;\n'\
'        else\n'\
'            read_data = rdata_ff1;\n'\
'    end\n'\
'\n'\
'    // synopsys translate_off\n'\
'    always @(posedge write_clk) begin\n'\
'        if(write_en & read_en & (write_addr == read_addr))\n'\
'            $display("TIME:%d ADDR:%0h collision under write clk FILE:%m",$time,write_addr);\n'\
'    end\n'\
'\n'\
'    always @(posedge read_clk) begin\n'\
'        if(write_en & read_en & (write_addr == read_addr))\n'\
'            $display("TIME:%d ADDR:%0h collision under read clk FILE:%m",$time,write_addr);\n'\
'    end\n'\
'    // synopsys translate_on\n'\
'\n'\
'`else//ASIC_MEM\n'\
'\n'\
'    wire [DATA-1:0] read_data_wire;\n'\
'    always @(*) begin\n'\
'        read_data = read_data_wire;\n'\
'    end\n'

ram_para_dp = \
'\t\t.DATA             ( DATA ),  \n' \
'\t\t.ADDR             ( ADDR ) , \n' \
'\t\t.DEPTH            ( DEPTH ) , \n' \
'\t\t.PIPELINE_WR      ( PIPELINE_WR ) , \n' \
'\t\t.PIPELINE_WR_DATA ( PIPELINE_WR_DATA ) , \n' \
'\t\t.PIPELINE_RD      ( PIPELINE_RD+1 ) , \n' \
'\t\t.WARNINGS         ( 1 ) \n'

ram_port_dp = \
'\t\t.write_clk     ( write_clk     ),  \n' \
'\t\t.write_en      ( write_en      ) , \n' \
'\t\t.write_addr    ( write_addr    ) , \n' \
'\t\t.write_data    ( write_data    ) , \n' \
'\t\t.cg_bypass     ( cg_bypass     ) , \n' \
'\t\t.read_clk      ( read_clk      ) , \n' \
'\t\t.read_en       ( read_en       ) , \n' \
'\t\t.read_addr     ( read_addr     ) , \n' \
'\t\t.read_data     ( read_data     )   \n' \


ram_sp_wrapper_head = ""\
'`ifndef RAM_SP\n'\
'`define RAM_SP\n'\
'module ram_dp  #(\n'\
'    parameter   DATA        = 32,\n'\
'    parameter   ADDR        = 9,\n'\
'    parameter   DEPTH       = (2**ADDR),\n'\
'    parameter   PIPELINE    = 0,\n'\
'    parameter   WARNINGS    = 1\n'\
') (\n'\
'    input   wire                clk,\n'\
'    input   wire                cg_bypass,\n'\
'    input   wire                slp,\n'\
'    input   wire                sd,\n'\
'    input   wire    [ADDR-1:0]  addr,\n'\
'    input   wire                chip_en,\n'\
'    input   wire                write_en,\n'\
'    input   wire    [DATA-1:0]  write_data,\n'\
'    output  reg     [DATA-1:0]  read_data\n'\
');\n'\
'\n'\
'`ifdef SIM_RAM\n'\
'    wire wr_en = write_en    & chip_en;\n'\
'    wire rd_en = (~write_en) & chip_en;\n'\
'\n'\
'    reg write_en_vld;\n'\
'    reg [ADDR-1:0] write_addr_vld;\n'\
'    reg [DATA-1:0] write_data_vld;\n'\
'    always @(*) begin\n'\
'        write_en_vld = write_en;\n'\
'        write_addr_vld = addr;\n'\
'        write_data_vld = write_data;    \n'\
'    end\n'\
'\n'\
'\n'\
'    reg [DATA-1:0] mem[0:DEPTH-1];\n'\
'    generate\n'\
'        genvar i;\n'\
'        for (i = 0; i < DEPTH; i=i+1) begin:mem_ins\n'\
'            always @(posedge  clk) begin\n'\
'                if(write_en_vld & (write_addr_vld == i))\n'\
'                    mem[i] <= write_data_vld;\n'\
'            end\n'\
'        end\n'\
'    endgenerate\n'\
'\n'\
'    reg [DATA-1:0] rdata_ff1;\n'\
'    reg [DATA-1:0] rdata_ff2;\n'\
'    always @(posedge clk) begin\n'\
'        if(rd_en) \n'\
'            rdata_ff1 <= mem[addr];\n'\
'    end \n'\
'\n'\
'    always @(posedge clk) begin\n'\
'        rdata_ff2 <= rdata_ff1;\n'\
'    end \n'\
'\n'\
'    always @(*) begin\n'\
'        if(PIPELINE == 1)\n'\
'            read_data = rdata_ff2;\n'\
'        else\n'\
'            read_data = rdata_ff1;\n'\
'    end\n'\
'\n'\
'`else \n'\
'\n'\
'    wire [DATA-1:0] read_data_wire;\n'\
'    always @(*) begin\n'\
'        read_data = read_data_wire;\n'\
'    end\n'

ram_para_sp = \
'\t\t.DATA    (DATA),\n' \
'\t\t.ADDR    (ADDR),\n' \
'\t\t.DEPTH   (DEPTH),\n' \
'\t\t.PIPELINE(PIPELINE),\n' \
'\t\t.WARNINGS(WARNINGS)\n'

ram_port_sp = \
'\t\t.clk       (clk),\n' \
'\t\t.cg_bypass (cg_bypass),\n' \
'\t\t.slp       (slp),\n' \
'\t\t.sd        (sd),\n' \
'\t\t.addr      (addr),\n' \
'\t\t.chip_en   (chip_en),\n' \
'\t\t.write_en  (write_en),\n' \
'\t\t.write_data(write_data),\n' \
'\t\t.read_data (read_data)\n'
