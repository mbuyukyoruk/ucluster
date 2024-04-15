import argparse
import sys
import subprocess
import re
import textwrap
import os
import time

try:
    from Bio import SeqIO
except:
    print("SeqIO module is not installed! Please install SeqIO and try again.")
    sys.exit()

try:
    import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

parser = argparse.ArgumentParser(prog='python ucluster.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\

# ucluster

Author: Murat Buyukyoruk

        ucluster help:

This script is developed to extract and cluster sequences from an uclust output.

SeqIO package from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.

Syntax:

        python ucluster.py -i demo.fasta -l uclust_out.txt

ucluster dependencies:

Bio module and SeqIO available in this package      refer to https://biopython.org/wiki/Download

tqdm                                                    refer to https://pypi.org/project/tqdm/

Input Paramaters (REQUIRED):
----------------------------
	-i/--input		Fasta		    Specify an original fasta file exctract clusters.

	-l/--list       Uclust          Specify an uclust output file that contains cluster informations.

	-f/--filter     Number          Specify number to report clusters that have more than a number of sequences in it.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

      	'''))

parser.add_argument('-i', '--input', required=True, type=str, dest='filename',
                    help='Specify an original fasta file exctract clusters.\n')
parser.add_argument('-l', '--list', required=True, type=str, dest='list',
                    help='Specify an uclust output file that contains cluster informations.\n')
parser.add_argument('-f', '--filter', required=False, type=int, dest='filter', default=None,
                    help='Specify number to report clusters that have more than a number of sequences in it.\n')

results = parser.parse_args()
filename = results.filename
list = results.list
filter = results.filter

orig_stdout = sys.stdout

acc_list = []
clst_list = []
out_file = []

timestr = time.strftime("%Y%m%d_%H%M%S")

proc = subprocess.Popen("wc -l < " + list, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length)) as pbar:
    pbar.set_description('Reading uclust cluster list...')
    with open(list, 'r') as file:
        for line in file:
            pbar.update()
            arr = line.split("\t")
            if arr[0] != "C":
                clst = arr[1]
                clst_list.append(clst)
                acc = arr[8].split()[0]
                acc_list.append(acc)

proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length)) as pbar:
    pbar.set_description('Grabbing...')
    for record in SeqIO.parse(filename, "fasta"):
        pbar.update()

        crr_acc = record.id
        try:

            ind = acc_list.index(crr_acc)
            dest_clst = clst_list[ind]

            out = filename.split(".fasta")[0] + "_cluster_" + str(dest_clst) + "_" + timestr + ".fasta"
            out_file.append(out)

            f = open(out, 'a')
            sys.stdout = f
            print(">" + record.description)
            print(re.sub("(.{60})", "\\1\n", str(record.seq), 0, re.DOTALL))

        except:
            sys.stdout = orig_stdout
            print(crr_acc + " is missing in the provided fasta file. Skipping the accession.")

res = [i for n, i in enumerate(out_file) if i not in out_file[:n]]

if filter != None:
    with tqdm.tqdm(range(len(res))) as pbar:
        pbar.set_description('Filtering clusters have less than ' + str(filter) + ' sequences...')
        for i in range(len(res)):
            pbar.update()
            proc = subprocess.Popen("grep -c '>' " + res[i], shell=True, stdout=subprocess.PIPE, text=True)
            length_question = int(proc.communicate()[0].split('\n')[0])
            if length_question < filter:
                os.system("rm " + res[i])