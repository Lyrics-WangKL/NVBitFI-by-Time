import sys, re, string, os, operator, math, datetime, random

# resovle path issues first
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import params as p
import numpy as np
# parse the file with inst count info per thread and create a tid->inst_count map
def read_inst_counts(d, app):
	countList = []
	fName = d + "/" + p.nvbit_profile_log 
	if not os.path.exists(fName):
		print ("%s file not found!" %fName )
		return countList
	print("logfile: ", fName)
	f = open(fName, "r")
	for line in f:
		# NVBit-igprofile; index: 0; kernel_name: _Z10simple_addi; ctas: 10; instrs: 409600; FADD: 0, FADD32I: 0, FCHK: 0, FCMP: 0, FFMA: 0, FFMA32I: 0, FMNMX: 0, FMUL: 0, FMUL32I: 0, FSET: 0, FSETP: 0, FSWZADD: 0, IPA: 0, MUFU: 0, RRO: 0, DADD: 0, DFMA: 0, DMNMX: 0, DMUL: 0, DSET: 0, DSETP: 0, HADD2: 0, HADD2_32I: 0, HFMA2: 0, HFMA2_32I: 0, HMUL2: 0, HMUL2_32I: 0, HSET2: 0, HSETP2: 0, IDP: 0, BFE: 0, BFI: 0, FLO: 10240, IADD: 0, IADD3: 0, IADD32I: 30720, ICMP: 0, IMAD: 0, IMAD32I: 0, IMADSP: 0, IMNMX: 0, IMUL: 0, IMUL32I: 0, ISCADD: 0, ISCADD32I: 0, ISET: 0, ISETP: 30720, LEA: 0, LOP: 0, LOP3: 0, LOP32I: 0, POPC: 10240, SHF: 0, SHL: 0, SHR: 0, XMAD: 30720, VABSDIFF: 40960, VADD: 0, VMAD: 0, VMNMX: 0, VSET: 0, VSETP: 0, VSHL: 0, VSHR: 0, VABSDIFF4: 0, F2F: 0, F2I: 0, I2F: 0, I2I: 0, MOV: 122880, MOV32I: 40960, PRMT: 0, SEL: 0, SHFL: 0, CSET: 0, CSETP: 0, PSET: 0, PSETP: 0, P2R: 0, R2P: 0, TEX: 0, TLD: 0, TLD4: 0, TMML: 0, TXA: 0, TXD: 0, TXQ: 0, TEXS: 0, TLD4S: 0, TLDS: 0, STP: 0, LD: 0, LDC: 0, LDG: 0, LDL: 0, LDS: 0, ST: 0, STG: 0, STL: 0, STS: 0, ATOM: 0, ATOMS: 0, RED: 320, CCTL: 0, CCTLL: 0, MEMBAR: 0, CCTLT: 0, SUATOM: 0, SULD: 0, SURED: 0, SUST: 0, BRA: 61120, BRX: 0, JMP: 0, JMX: 0, SSY: 0, SYNC: 0, CAL: 0, JCAL: 0, PRET: 0, RET: 0, BRK: 0, PBK: 0, CONT: 0, PCNT: 0, EXIT: 10240, PEXIT: 0, LONGJMP: 0, PLONGJMP: 0, KIL: 0, BPT: 0, IDE: 0, RAM: 0, RTT: 0, SAM: 0, NOP: 0, CS2R: 0, S2R: 10240, LEPC: 0, B2R: 0, BAR: 0, R2B: 0, VOTE: 10240, DEPBAR: 0, GETCRSPTR: 0, GETLMEMBASE: 0, SETCRSPTR: 0, SETLMEMBASE: 0, fp64: 0, fp32: 0, ld: 0, pr: 30720, nodest: 71680, others: 307200, gppr: 337920,
		line = line.rstrip()
		kcount = line.split(';')[1].split(':')[1].strip()
		kname = line.split(';')[2].split('kernel_name:')[1].strip()
		icount = line.split(';')[4].split(':')[1].strip()
		cl = line.split(';')[5].split(',')
		countList.append([kname, int(kcount), int(icount)])
		for e in cl: 
			if e != "":
				countList[-1].append(e.split(':')[1])
	f.close()
	# print(countList)
	return countList 

# return total number of instructions in the countList 
def get_total_insts(countList, with_will_not_execute):
	total = 0
	for l in countList:
		# kname:kcount:instrns 
		total += int(l[2])
	# print(total)
	return total

def get_inst_count_format():
	format_str = "kName:kernelCount:instrs:FADD:FADD32I:FCHK:FCMP:FFMA:FFMA32I:FMNMX:FMUL:FMUL32I:FSEL:FSET:FSETP:FSWZADD:IPA:MUFU:RRO:DADD:DFMA:DMNMX:DMUL:DSET:DSETP:HADD2:HADD2_32I:HFMA2:HFMA2_32I:HMUL2:HMUL2_32I:HSET2:HSETP2:IDP:IDP4A:BFE:BFI:BMSK:BREV:FLO:IADD:IADD3:IADD32I:ICMP:IMAD:IMAD32I:IMADSP:IMNMX:IMUL:IMUL32I:ISCADD:ISCADD32I:ISET:ISETP:LEA:LOP:LOP3:LOP32I:PLOP3:POPC:SHF:SHL:SHR:XMAD:IMMA:HMMA:VABSDIFF:VADD:VMAD:VMNMX:VSET:VSETP:VSHL:VSHR:VABSDIFF4:F2F:F2I:I2F:I2I:I2IP:FRND:MOV:MOV32I:PRMT:SEL:SGXT:SHFL:CSET:CSETP:PSET:PSETP:P2R:R2P:TEX:TLD:TLD4:TMML:TXA:TXD:TXQ:TEXS:TLD4S:TLDS:STP:LD:LDC:LDG:LDL:LDS:ST:STG:STL:STS:MATCH:QSPC:ATOM:ATOMS:RED:CCTL:CCTLL:ERRBAR:MEMBAR:CCTLT:SUATOM:SULD:SURED:SUST:BRA:BRX:JMP:JMX:SSY:SYNC:CAL:JCAL:PRET:RET:BRK:PBK:CONT:PCNT:EXIT:PEXIT:LONGJMP:PLONGJMP:KIL:BSSY:BSYNC:BREAK:BMOV:BPT:IDE:RAM:RTT:SAM:RPCMOV:WARPSYNC:YIELD:NANOSLEEP:NOP:CS2R:S2R:LEPC:B2R:BAR:R2B:VOTE:DEPBAR:GETCRSPTR:GETLMEMBASE:SETCRSPTR:SETLMEMBASE:PMTRIG:SETCTAID"
	for igid in p.IGID_STR:
		format_str += ":" + igid
	return format_str

#return total number of instructions of each type or opcode, across all the kernels
def get_total_counts(countList):
	length = get_inst_count_format().count(':')-1
	total_icounts = [0] * length
	for l in countList:
		for i in range(length):
			total_icounts[i] += int(l[2+i])
	# print(total_icounts)
	return total_icounts

def get_injection_site_info(countList, inj_num, igid):
	start = 0
	idx = igid + get_inst_count_format().count(':') - p.NUM_INST_GROUPS + 1
	for item in countList:
		# print(start, start + int(item[idx]))
		if start <= inj_num < start + int(item[idx]):
			# print([item[0], item[1], inj_num-start])
			return [item[0], item[1], inj_num-start] # return [kname, kcount, inj_num in this kernel]
		start += int(item[idx])
	return ["", -1, -1]

def gen_faultsite_str(igid, countList, injection_site):
	[inj_kname, inj_kcount, inj_icount] = get_injection_site_info(countList, injection_site, igid) # convert injection index to [kname, kernel count, inst index]
	inj_op_id_seed = random.random()
	inj_bid_seed = random.random() 
	selected_str = inj_kname + " " + str(inj_kcount) + " " + str(inj_icount) + " " + str(inj_op_id_seed) + " " + str(inj_bid_seed) + " "
	return selected_str

def write_fault_site(f, igid, countList, total_count, injection_counter, start=0, end=0, verbose=False, scope='vanilla'):
	if scope == 'vanilla' or scope == 'kernels': # If conducting kernel level / vanilla injection, start is 0, end is the total_count
		start = 0
		end = total_count
	inj_site_idx = random.randint(start, end)

	[inj_kname, inj_kcount, inj_icount] = get_injection_site_info(countList, inj_site_idx, igid) # convert injection index to [kname, kernel count, inst index]
	inj_op_id_seed = random.random()
	inj_bid_seed = random.random() 
	selected_str = inj_kname + " " + str(inj_kcount) + " " + str(inj_icount) + " " + str(inj_op_id_seed) + " " + str(inj_bid_seed) + " "
	if verbose:
		print ("%d/%d: Selected between: %d and %d /%s" %(injection_counter, end - start, start, end, selected_str))
	f.write(selected_str + "\n") # print injection site information