# -*- coding: utf-8 -*-
import argparse
import insilico_translation as ist
import longread_functions as lrf
import pandas as pd
import numpy as np
from gtfparse import read_gtf
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from pybiomart import Server # for retrieval of Uniprot IDs
import constants
import os
from time import sleep

# Main function
def main():
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gtf', help='path to gtf file', required=True)
    parser.add_argument('-b', '--bed', help='path to bed file', required=True)
    parser.add_argument('-f', '--fasta', help='path to fasta file', required=True)
    parser.add_argument('-p', '--file_prefix', help='filename prefix (not path)', required=True)
    parser.add_argument('-o', '--outpath', help='Output path. Note JCASTLR autonames files', required=True)
    args = parser.parse_args()
    # set constants
    gtf =  args.gtf
    bed = args.bed
    fasta = args.fasta
    prefix = args.file_prefix
    out_location = args.outpath
    g = ist.Gtf(gtf)
    b = ist.Bed(bed)
    # define how many reads need to be looped through and level lists
    with open(fasta) as f:
        Canonical = []
        L1 = []
        L2 = []
        L3 = []
        L4 = []
        L5 = []
        n = 0
        n1 = 0
        for line in f:
            if line.startswith(">"):
                n += 1
    # loop through each record to get info and translate
    with open(fasta) as f:
        for record in SeqIO.parse(f, 'fasta'):
            # n1 += 1
            # lrf.progress_bar(n1, n, 50)
            r = record
            s = ist.Sequences(g, r)
            s.subset_gtf()
            s.get_meta()
            conditions = ['Canonical','L1']
            if any(conditions) and not all(conditions):
                s.annotated_trancript_trim()
            # a = ist.Canonical_test(s)
            # a.get_canonical_aa()
            # a.make_header()
            # print(a.level, a.rid, a.biotype)
            if s.level == "Canonical":
                # a = ist.Canonical_test(s)
                # a.get_canonical_aa()
                # a.make_header()
                # s.annotated_trancript_trim()
                p = ist.Peptide(s)
                prot_seq = p.annotated_translate()
                p.get_canonical_aa_uniprot_local()
                p.make_header()
                seq = p.str_to_seqrec(prot_seq)
                Canonical.append(seq)
            elif s.level == "L1":
                # a = ist.Canonical_test(s)
                # a.get_canonical_aa()
                # a.make_header()
                # s.annotated_trancript_trim()
                p = ist.Peptide(s)
                prot_seq = p.annotated_translate()
                p.get_canonical_aa_uniprot_local()
                p.make_header()
                seq = p.str_to_seqrec(prot_seq)
                L1.append(seq)
            elif s.level == "L2":
                # a = ist.Canonical_test(s)
                # a.get_canonical_aa()
                # a.make_header()
                # s.annotated_trancript_trim()
                p = ist.Peptide(s)
                prot_seq = p.multi_phase_translate()
                p.get_canonical_aa_uniprot_local()
                p.make_header()
                seq = p.str_to_seqrec(prot_seq)
                L2.append(seq)
            elif s.level == "L3":
                # a = ist.Canonical_test(s)
                # a.get_canonical_aa()
                # a.make_header()
                p = ist.Peptide(s)
                prot_seq = p.multi_phase_translate()
                p.get_canonical_aa_uniprot_local()
                p.make_header()
                seq = p.str_to_seqrec(prot_seq)
                L3.append(seq)
            elif s.level == "L4":
                # a = ist.Canonical_test(s)
                # a.get_canonical_aa()
                # a.make_header()
                p = ist.Peptide(s)
                prot_seq = p.multi_phase_translate()
                p.get_canonical_aa_uniprot_local()
                p.make_header()
                seq = p.str_to_seqrec(prot_seq)
                L4.append(seq)
            elif s.level == "L5":
                # a = ist.Canonical_test(s)
                # a.make_header()
                p = ist.Peptide(s)
                prot_seq = p.multi_phase_translate()
                p.get_canonical_aa_uniprot_local()
                p.make_header()
                seq = p.str_to_seqrec(prot_seq)
                L5.append(seq)

            else:
                print("Orphan Read")
    print(L1)
    print(L2)
    for i in Canonical:
        lrf.prot_to_fasta(i, out_location, prefix, "Canonical")
    print(f'{len(Canonical)} Canonical Isoforms')
    for i in L1:
        lrf.prot_to_fasta(i, out_location, prefix,"_Level1")
    print(f'{len(L1)} Level 1 Isoforms')
    for i in L2:
        lrf.prot_to_fasta(i, out_location,prefix, "_Level2")
    print(f'{len(L2)} Level 2 Isoforms')
    for i in L3:
        lrf.prot_to_fasta(i, out_location, prefix,"_Level3")
    print(f'{len(L3)} Level 3 Isoforms')
    for i in L4:
        lrf.prot_to_fasta(i, out_location, prefix,"_Level4")
    print(f'{len(L4)} Level 4 Isoforms')
    for i in L5:
        lrf.prot_to_fasta(i, out_location, prefix,"_Level5")
    print(f'{len(L5)} Level 5 Isoforms')






