# -*- coding: utf-8 -*-
import csv
import os
import sys
from importlib import import_module
import yaml

class TestGenerator:
    def __init__(self, args):
        self.output_dir = args.dir
        self.test_name = args.name
        self.test_filename = os.path.join(self.output_dir, self.test_name + ".yml")
        self.target = args.target
        self.period = args.period
        self.processor = import_module('.mymodule.' + args.target, package=__package__)
        self.input_csv = args.csv

    # clean output directories
    def clean(self):
        if os.path.isdir(self.output_dir) is False:
            os.makedirs(self.output_dir)

    # pass1: prepare to process CSV data
    def prepare(self):
        with open(self.input_csv, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                self.titles = dict()
                for i, cell in enumerate(row):
                    self.titles[cell] = i
                break

    # pass2: generate test .yml file
    def generate(self):
        with open(self.input_csv, newline='') as csvfile:
            with open(self.test_filename, "w") as outfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                processor = self.processor.Process(self.period, self.titles)
                outjson = list()
                for i, row in enumerate(csvreader):
                    if i == 0:
                        continue
                    outdict = processor.process(row)
                    outjson.append(outdict)
                outfile.write("# This file is automatically generated by " + self.input_csv + "\n")
                yaml.dump(outjson, outfile, encoding='utf-8', allow_unicode=True, sort_keys=False)
