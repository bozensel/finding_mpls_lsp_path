from pprint import pprint
from ttp import ttp
import json
import time
import urllib.request as urllib2
import json
import codecs
import re
import os
import difflib
from termcolor import colored
import sys

def mpls_lsp_path_parser(data_to_parse):
    ttp_template = template_mpls_lsp_path

    parser = ttp(data=data_to_parse, template=ttp_template)
    parser.parse()

    # print result in JSON format
    results = parser.result(format='json')[0]
    #print(results)

    #converting str to json. 
    result = json.loads(results)

    return(result)

parsed_mpls_lsp_path_parser = mpls_lsp_path_parser(data_to_parse)

# Collecting 1st data 

# print(parsed_mpls_lsp_path_parser[0]['LSP_PATH'])
for lsp in parsed_mpls_lsp_path_parser[0]['LSP_PATH']:
    if len(parsed_mpls_lsp_path_parser[0]['LSP_PATH']) == 1: continue
    #print(lsp["LSP_PATH_DETAIL"])
    actual_hops_list = []
    if "Actual_Hops" in lsp["LSP_PATH_DETAIL"]:
        for actual_hops in lsp["LSP_PATH_DETAIL"]["Actual_Hops"]:
            actual_hops_list.append(actual_hops['IP_Hops'])
        with open("clishow_parser_outputs\mpls_lsp_path_detail.txt", "a") as f:
            f.write(f"The LSP Name : {lsp['LSP_PATH_DETAIL']['LSP_Name']} **** The Path Used : {lsp['LSP_PATH_DETAIL']['Path_Used']} **** Out Interface : {lsp['LSP_PATH_DETAIL']['Out_Interface']} **** Path LSP ID : {lsp['LSP_PATH_DETAIL']['PATH_Lsp_ID']} **** IP Hops {actual_hops_list}\n")

# 1st data has been collected

# Collecting 2nd data. 

with open('7750SR-bor57_20201209_1328.bin.txt.show') as f:
    data_to_parse = f.read()

parsed_mpls_lsp_path_parser = mpls_lsp_path_parser(data_to_parse)

for lsp in parsed_mpls_lsp_path_parser[0]['LSP_PATH']:
    if len(parsed_mpls_lsp_path_parser[0]['LSP_PATH']) == 1: continue
    #print(lsp["LSP_PATH_DETAIL"])
    actual_hops_list = []
    if "Actual_Hops" in lsp["LSP_PATH_DETAIL"]:
        for actual_hops in lsp["LSP_PATH_DETAIL"]["Actual_Hops"]:
            actual_hops_list.append(actual_hops['IP_Hops'])
        with open("clishow_parser_outputs\mpls_lsp_path_detail2.txt", "a") as f:
            f.write(f"The LSP Name : {lsp['LSP_PATH_DETAIL']['LSP_Name']} **** The Path Used : {lsp['LSP_PATH_DETAIL']['Path_Used']} **** Out Interface : {lsp['LSP_PATH_DETAIL']['Out_Interface']} **** Path LSP ID : {lsp['LSP_PATH_DETAIL']['PATH_Lsp_ID']} **** IP Hops {actual_hops_list}\n")

# 2nd data has been collected. 

compared_list = []
def comparing_lsps():
    with open('clishow_parser_outputs\mpls_lsp_path_detail.txt') as file_1:
        file_1_text = file_1.readlines()
    
    with open('clishow_parser_outputs\mpls_lsp_path_detail2.txt') as file_2:
        file_2_text = file_2.readlines()

    for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile='file1.txt', 
            tofile='file2.txt', lineterm=''):
        if ("-" == line[0]) or ("+" == line[0]):
            line2 = line.split("****")
            if len(line2) == 1: continue
            compared_list.append([line2[0]])
            with open("clishow_parser_outputs\compared_lsps.txt", "a") as f:
                f.write(f"{line2[0]} --> {line2[1]} --> {line2[2]} --> {line2[3]} --> {line2[4]}")
    print(colored("\n############################ WARNING! ############################\n", "red"))
    print(colored(f"Following lsps have different IP Hops between two tech-support files. You can see details in 'compared_lsps.txt' file.\n", "yellow"))
    for compared_lsp in compared_list:
        print(compared_lsp[0])

comparing_lsps()
