import sys
import os

#os.system("python count_cfg_freq.py parse_train.dat > cfg.count")
#os.system("python pretty_print_tree.py parse_dev.key")
#os.system("python rare_replace.py cfg.count parse_train.dat > parse_train_rare.dat")
#os.system("python count_cfg_freq.py parse_train_rare.dat > parse_train.counts.out")
#os.system("python cky.py > parse_dev.out")
#os.system("python eval_parser.py parse_dev.key parse_dev.out")

#os.system("python cky.py > parse_test.p2.out")


#os.system("python rare_replace.py cfg.count parse_train_vert.dat > parse_train_vert_rare.dat")
#os.system("python count_cfg_freq.py parse_train_vert_rare.dat > cfg__rare_vert.count")
#os.system("python cky.py cfg__rare_vert.count parse_dev.dat > parse_dev_vert.out")
#os.system("python eval_parser.py parse_dev.key parse_dev_vert.out")

os.system("python cky.py cfg__rare_vert.count parse_test.dat > parse_test.p3.out")