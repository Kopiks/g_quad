import os
import sys
import subprocess


fo = open("interval_summary", "r")

def filterInput(): 
	tab=[]
	out=[]
	no_ints = -1
	for n in fo:
		no_ints += 1
		line = n.split("\t")
		tab.append(line)
	out.append(tab[0][:])

	for i, line in enumerate(tab[1:]):
		out.append([line[0]])
		for item in line[1:]:
			if float(item) >= 10:
				temp = 1
			else:
				temp = 0
			out[i+1].extend([temp])




	out.append(["sum"]+[0]*(len(out[1])-1))

	for line in out[1:-1]:
		for i, n in enumerate(line[1:]):
			out[-1][i+1] += n


	for i, n in enumerate(out[0]):
		
		out[0][i] = n.split("_")[0]
		





	bads=()
	quart = float(no_ints)*75/100
	for i, n in enumerate(out[-1][1:]):

		if n<quart:
			bads += (i+1,) 

	for n in out:
		for m in bads:
			n[m] = None
	for i, n in enumerate(out):
		out[i] = filter(lambda x: x!=None, n)


	out[0].extend(["sum"])
	for item in out[1:]:
		item.extend([sum(item[1:])])

	quart = float((len(out[0])-2))*75/100
	print quart
	for i, n in enumerate(out[1:]):
		if n[-1] < quart:
			out[i+1] = None
	out = filter(lambda x: x!=None, out)

	print no_ints

	no_ints = -2
	for n in out:
		no_ints += 1

	print no_ints

	return out


def newBed(input):
	out_file = open("filtered.bed","w+")
	for n in input[1:-1]:
		line = n[0].replace(":","-")
		line = line.split("-")
		out_file.write(line[0]+"\t"+line[1]+"\t"+line[2]+"\n")
	out_file.close()

def reCount(inp):
	files = ["-I "+x+".bam" for x in inp[0][1:-1]]
	refseq = sys.argv[1]						#path to reference fasta
	path = os.getcwd()
	cmd = 	(	
				"java -jar $GATK " 
				"-T DepthOfCoverage "
				"-omitBaseOutput "
				"-L %s "  
				"-o recount "
				"-R %s "
				%(path+"/filtered.bed ", refseq+" ")
				+(" ".join(files))
			)

	subprocess.call(cmd, shell=True)



#newBed(filterInput())


def varCall(input):
	ids = [x for x in input[0][1:-1]]
	refseq = sys.argv[1]
	path = os.getcwd()
	for item in ids:
		
		vc = (
				"java -jar $GATK -T HaplotypeCaller "
				"-R %s"
				"-I %s"
				"-L %s"
				"-o %s"
				%(refseq+" ", item+".bam ", path+"/filtered.bed ", item + "_raw.vcf ")
			)

		print vc
		subprocess.call(vc, shell=True)

#reCount(filterInput())
#varCall(filterInput())


def hardFilter(idx):


	
	snp_xt	 = (
					"java -jar $GATK "
					"-T SelectVariants "
					"-R %s "
					"-V %s "
					"-selectType SNP "
					"-o %s "
					%(refseq, idx+"_raw.vcf", idx+"_pre_snp.vcf")
				)	

	snp_filt = (
					"java -jar $GATK "
					"-T VariantFiltration "
					"-R %s "
					"-V %s "
					"--filterExpression 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0' "
					"-filterName 'my_snp_filter' "
					"-o %s "
					%(refseq, idx+"_pre_snp.vcf", idx+"_snp.vcf" )
				)

	indel_xt = (
					"java -jar $GATK "
					"-T SelectVariants "
					"-R %s "
					"-V %s "
					"-selectType INDEL "
					"-o %s "
					%(refseq, idx+"_raw.vcf", idx+"_pre_indel.vcf")
				)

	indel_filt =(
					"java -jar $GATK "
					"-T VariantFiltration "
					"-R %s "
					"-V %s "
					"--filterExpression 'QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0' "
					"--filterName 'my_indel_filter' "
					"-o %s "
					%(refseq, idx+"_pre_indel.vcf", idx+"_indel.vcf")
				)
	
	subprocess.call(snp_xt, shell=True)
	subprocess.call(snp_filt, shell=True)
	
	try:
		os.remove(idx+"_pre_snp.vcf")
		os.remove(idx+"_pre_snp.vcf.idx")
	except OSError:
		pass
	
	subprocess.call(indel_xt, shell=True)
	subprocess.call(indel_filt, shell=True)

	try:
		os.remove(idx+"_pre_indel.vcf")
		os.remove(idx+"_pre_indel.vcf.idx")
	except OSError:
		pass



def reCalib(idx, intervals):

	recal = (
				"java -jar $GATK "
				"-T BaseRecalibrator "
				"-R %s "
				"-I %s "
				"-L %s "
				"-knownSites %s "
				"-knownSites %s "
				"-o %s "
				%(refseq, idx+".bam", intervals, idx+"_snp.vcf", idx+"_indel.vcf", idx+"_racal.table")
			)

	sec_pass=(
				"java -jar $GATK "
				"-T BaseRecalibrator "
				"-R %s "
				"-I %s "
				"-L %s "
				"-knownSites %s "
				"-knownSites %s "
				"-BQSR %s"
				"-o %s"
				%(refseq, idx+".bam", intervals, idx+"_snp.vcf", idx+"_idel.vcf", idx+"_recal.table", idx+"post_recal.table")
			)

	plots = (
				"java -jar $GATK "
				"-T AnalyzeCovariates "
				"-R %s "
				"-L %s "
				"-before %s "
				"-after %s "
				"-plots %s "
				%(refseq, intervals, idx+"_recal.table", idx+"_post_recal.table", idx+"_plots.pdf" ) 
			)
	subprocess.call(recal, shell=True)
	subprocess.call(sec_pass, shell=True)
	subprocess.call(plots, shell=True)












refseq = sys.argv[1]
def main():
	input = filterInput()
	ids = [x for x in input[0][1:-1]]
	path = os.getcwd()
	intervals = path+"/filtered.bed"

	for idx in ids:
		hardFilter(idx)



main()

