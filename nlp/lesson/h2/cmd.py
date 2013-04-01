import sys
import os

#os.system("python count_cfg_freq.py parse_train.dat > cfg.count")
#os.system("python pretty_print_tree.py parse_dev.key")
#os.system("python rare_replace.py cfg.count parse_train.dat > parse_train_rare.dat")
os.system("python count_cfg_freq.py parse_train_rare.dat > parse_train.counts.out")