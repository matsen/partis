#!/usr/bin/env python
import sys
import os
from subprocess import check_call
sys.path.insert(1, './python')

import utils
# original = 'GAGGTGCAGCTGGTGGAGTCTGGGGGAGGCTTGGTCCAGCCTGGGGGGTCCCTGAGACTCTCCTGTGCAGCCTCTGGTTTCACCTTCAGTGACTACTACATGAGCTGGGTCCGCCAGGCTCCCGGGAAGGGGCTGGAGTGGGTAGGTTTCATTAGAAACAAAGCTAATGGTGGGACAACAGAATAGACCACGTCTGTGAAAGGCAGATTCACAATCTCAAGAGATGATTCCAAAAGCATCACCTATCTGCAAATGAACAGCCTGAGAGCCGAGGACACGGCTGTGTATTACTGTGCGAGAGA'
# snpd = 'GAGGTGCAGCTGGTGGAGTCGGGGGGAGGCTTGGTCCAGCCTGGGGGGTCCCTGAGACTCTCCTGTGCAGCCTCTGGTTTCACCTTCAGTGACTACTACATGAGCTCGGTCCGCCAGGCTCCCGGGAAGGGGCTGGAGTGGGTAGGTTTCATTAGAAACAAAGCTAATGGTGAGACAACAGAATAGACCACGTCTGTGAAAGGCATATTCACAATCTCAAGAGATGATTCCAAAAGCATCACCTATCTGCAAATGAACAGCCTGAGAGCCGAGGACACGGCTGTGTATTACTGTGCGAGAGA'
# oh_one = 'GAGGTGCAGCTGGTGGAGTCCGGGGGAGGCTTGGTCCAGCCTGGGGGGTCCCTGAGACTCTCCTGTGCAGCCTCTGGATTCACCTTCAGTGACTACTACATGAGCTGGGTCCGCCAGGCTCCCGGGAAGGGGCTGGAGTGGGTAGGTTTCATTAGAAACAAAGCTAATGGTGGGACAACAGAATAGACCACGTCTGTGAAAGGCAGATTCACAATCTCAAGAGATGATTCCAAAAGCATCACCTATCTGCAAATGAACAGCCTGAGAGCCGAGGACACGGCCGTGTATTACTGTGCGAGAGA'
# utils.color_mutants(original, snpd, print_result=True)
# print utils.color_mutants(original, oh_one)
# sys.exit()
# # python -m cProfile -s tottime -o prof.out ' + 

# ----------------------------------------------------------------------------------------
def run(cmd_str):
    print 'RUN', cmd_str
    sys.stdout.flush()
    check_call(cmd_str.split())

outdir = '_tmp/allele-finder'
# param_dir = os.getcwd() + '/test/reference-results/test/parameters/simu/hmm'
# original_param_dir = '/fh/fast/matsen_e/dralph/work/partis-dev/_output/021-018/simu-3-leaves-1.0-mutate/hmm'
base_cmd = './bin/partis'

# ----------------------------------------------------------------------------------------
def join_gene_names(gene_name_str):
    return ':'.join([utils.sanitize_name(g) for g in gene_name_str.split(':')])

# ----------------------------------------------------------------------------------------
def get_label(existing_genes, new_allele):
    return '_existing_' + join_gene_names(existing_genes) + '_new_' + join_gene_names(new_allele)

# ----------------------------------------------------------------------------------------
def run_test(existing_v_genes, new_v_allele, dj_genes):
    label = 'test'  #get_label(existing_genes, new_allele)
    simfname = outdir + '/simu-' + label + '.csv'
    outpdir = outdir + '/simu-' + label
    plotdir = os.getenv('www') + '/partis/allele-finding/' + label

    existing_genes = existing_v_genes + ':' + dj_genes

    # simulate
    cmd_str = base_cmd + ' simulate --n-sim-events 500 --n-procs 10 --simulate-partially-from-scratch --mutation-multiplier 0.5'
    # cmd_str += ' --parameter-dir ' + original_param_dir
    cmd_str += ' --only-genes ' + existing_genes #+ ':' + new_v_allele
    cmd_str += ' --outfname ' + simfname
    run(cmd_str)
    
    snps_to_add = {'IGHV3-71*01' : 4}
    utils.rewrite_germline_fasta('data/imgt', outdir + '/germlines', only_genes=existing_genes.split(':'), snps_to_add=snps_to_add)
    
    # cache-parameters
    cmd_str = base_cmd + ' cache-parameters --infname ' + simfname + ' --n-procs 10 --find-new-alleles --only-smith-waterman'
    cmd_str += ' --datadir ' + outdir + '/germlines'
    cmd_str += ' --only-genes ' + existing_genes
    cmd_str += ' --parameter-dir ' + outpdir
    cmd_str += ' --plotdir ' + plotdir
    run(cmd_str)

# ----------------------------------------------------------------------------------------

dj_genes = 'IGHD6-19*01:IGHJ4*02'
existing_v_genes = 'IGHV3-71*01:IGHV3-71*03'  # 1-18*01
new_v_allele = 'IGHV3-71*03' #1-18*04

# glfo = utils.read_germline_set('data/imgt')
# allelic_groups = utils.separate_into_allelic_groups(glfo['seqs'])
# for primary_version in allelic_groups['v']:
#     for sub_version in allelic_groups['v'][primary_version]:
#         if len(allelic_groups['v'][primary_version][sub_version]) == 1:
#             continue
#         print '    %15s   %15s   %s' % (primary_version, sub_version, allelic_groups['v'][primary_version][sub_version])

# print ''
# print glfo['seqs']['v']['IGHV3-30*01']
# for g in glfo['seqs']['v']:
#     if '3-30*' not in g:
#         continue
#     print utils.color_mutants(glfo['seqs']['v']['IGHV3-30*01'], glfo['seqs']['v'][g])

run_test(existing_v_genes, new_v_allele, dj_genes)
