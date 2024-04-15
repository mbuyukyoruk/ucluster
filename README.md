# ucluster

Author: Murat Buyukyoruk

        ucluster help:

This script is developed to extract and cluster sequences from an uclust output.

SeqIO package from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and 
many sequences.

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

