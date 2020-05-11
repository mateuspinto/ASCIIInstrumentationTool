import sys
import json
import re

class ASCIIInstrumentationTool:

    def __init__(self, instr_filename):

        with open(instr_filename, "r") as file_json:

            data = json.load(file_json)

            self.main_mark = data["main_mark"]
            self.return_mark = data["return_mark"]
            self.to_add_start_file= data["to_add_start_file"]
            self.to_add_before_main = data["to_add_before_main"]
            self.to_add_before_return = data["to_add_before_return"]
            self.to_instrument = data["to_instrument"]

    def run(self, input_filename, output_filename):

        with open(input_filename, "r") as input_asm:
            with open(output_filename, "w") as output_asm:

                for line_w in self.to_add_start_file:
                    output_asm.write(line_w + "\n")

                main = 0

                for line_r_raw in input_asm:

                    line_r = line_r_raw.strip()
                    parameters = re.findall(r"[\w']+", line_r)
                    inst_prefix = parameters[0]

                    if inst_prefix == self.main_mark:
                        for line_w in self.to_add_before_main:
                            output_asm.write(line_w + "\n")
                            output_asm.write(line_r_raw)
                            main=1

                    elif inst_prefix == self.return_mark:
                        for line_w in self.to_add_before_return:
                            output_asm.write(line_w + "\n")
                            output_asm.write(line_r_raw)

                    elif inst_prefix in self.to_instrument:
                        to_instrument = self.to_instrument[inst_prefix]
                        if to_instrument["inst_functions"] and main==0 or to_instrument["inst_main"] and main==1:

                            for line_w_raw in to_instrument["before"]:
                                line_w = line_w_raw
                                for i in range(len(parameters)):
                                    line_w = line_w.replace("_P" + str(i), parameters[i])
                                output_asm.write(line_w + "\n")

                            output_asm.write(line_r_raw)

                            for line_w_raw in to_instrument["after"]:
                                line_w = line_w_raw
                                for i in range(len(parameters)):
                                    line_w = line_w.replace("_P" + str(i), parameters[i])
                                output_asm.write(line_w + "\n")

                    else:
                        output_asm.write(line_r_raw)

if __name__ == "__main__":
    tool = ASCIIInstrumentationTool("example.json")
    tool.run("hello_world.s", "hello_world_INST.s")