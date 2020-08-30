#!/usr/bin/env python3

import sys
import subprocess
from ruamel.yaml import YAML

import pkg_resources
DATA_PATH = pkg_resources.resource_filename('terraformer_ui', 'data/resources.yaml')

SKIP_SUB_RESOURCES=1

class TerraformerUIConsole(object):

    resource_type = None
    resources = None
    regions = None
    filters = []
    yaml = None

    def run_terraformer(self):
        cmd = [ "terraformer" ]
        cmd.extend( ("import", self.resource_type) )
        if self.resources != None:
            cmd.extend( ("--resources", ",".join(self.resources)) )
        if self.regions != None:
            cmd.extend( ("--regions", ",".join(self.regions)) )
        if len(self.filters) > 0:
            for f in self.filters:
                cmd.extend(     ( "--filter",   ";".join( ["%s=%s" % (a[0],a[1]) for a in f] )     ) )
        self.log("cmd: %s" % cmd)
        subprocess.check_call(cmd)


    def log(self, msg):
        sys.stderr.write(msg + "\n")

    def outputfmt(self, lst):
        items = list( k for k in lst )
        stuff, it = '', iter(items)
        for i in it:
            stuff += '   {:<34}{:<34}{}'.format(i, next(it, ""), next(it, "") ) + "\n"
        return stuff

    def extract_keys(self, obj, keys, mandatory=False):
        vals = []
        for k in obj:
            for key in keys:
                if type(k) == type(list()):
                    if key in k:
                        # return the one item in the list that matches
                        vals.append(key)
                elif type(k) == type(dict()):
                    if key in k:
                        # return the whole dict if the key exists in it
                        vals.append(k)
                elif type(k) == type(str()):
                    if key == k:
                        # return the string if it exists
                        vals.append(k)
                elif mandatory == True:
                    raise Exception("Missing key '%s'" % key)
        return vals

    def flatten_list(self, obj):
        flat_obj = []
        for k in obj:
            if type(k) == type(list()):
                flat_obj.extend(k)
            elif type(k) == type(dict()):
                flat_obj.extend( list(k.keys()) )
            else:
                flat_obj.append(k)
        return flat_obj

    def find_answer(self, obj, question):
        answer = input(question)
        if answer == "":
            answer_lst = [k for k in obj ]
        else:
            answer_lst = [x.strip() for x in answer.split(',')]
        self.log("Selected: %s\n" % answer_lst)
        return self.extract_keys(obj, answer_lst, mandatory=True)

    def ask_resource_type(self):
        all_resources = [ k for k in self.yaml["resources"] ]
        self.resource_type = self.find_answer( self.yaml["resources"], "What resource type would you like to use? [%s] " % ','.join(all_resources) )[0]

    def ask_resources(self):
        flattened_resources = [ i for k in self.yaml["resources"][self.resource_type] for i in k ]
        resource_fmt = self.outputfmt( flattened_resources )
        resource_a = self.find_answer( self.yaml["resources"][self.resource_type], "What resource(s) would you like to get? [\n%s] " % resource_fmt )
        self.resources = [ i for k in resource_a for i in k ]

    def ask_sub_resources(self):
        if not SKIP_SUB_RESOURCES:
            # NOTE: this doesn't seem to work in terraformer, don't use this function
            sub_resources = []
            for r in resource_a:
                for r_n, r_v in r.items():
                    subresource_fmt = self.outputfmt( r_v )
                    sub_resources.extend( self.find_answer( r_v, "What sub-resources would you like to get? [\n%s] " % subresource_fmt ) )
            self.resources = sub_resources

    def ask_regions(self):
        if "regions" in self.yaml and self.resource_type in self.yaml["regions"]:
            regions_fmt = self.outputfmt( self.yaml["regions"][self.resource_type] )
            self.regions = self.find_answer(self.yaml["regions"][self.resource_type], "What region(s) would you like to retrieve? [\n%s] " % regions_fmt )

    def ask_tags(self):
        print("What tags would you like to filter for? (Leave blank to continue)")
        tags = []
        while True:
            tmpa = []
            name= input("Tag Name: ").strip()
            if len(name) < 1:
                break
            val= input("Tag Value: ")
            if len(val) < 1:
                break
            tmpa = [ ['tags.Name',name], ['Value',val] ]
            typ= input("Resource (leave blank for any): ").strip()
            if len(typ) > 0:
                tmpa.insert(0, ['Type',typ])
            tags.append(tmpa)
            print("")
        if len(tags) > 0:
            self.filters.extend(tags)

    def main(self):
        with open(DATA_PATH) as f:
            self.yaml = YAML(typ='safe').load(f)

        self.ask_resource_type()
        self.ask_resources()
        self.ask_sub_resources()
        self.ask_regions()
        self.ask_tags()
        self.run_terraformer()


def main():
    t = TerraformerUIConsole()
    t.main()

if __name__ == "__main__":
    main()

