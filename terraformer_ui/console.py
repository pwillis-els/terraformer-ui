#!/usr/bin/env python3

import sys
from ruamel.yaml import YAML

import pkg_resources

DATA_PATH = pkg_resources.resource_filename('terraformer_ui', 'data/resources.yaml')

class TerraformerUIConsole(object):

    resource_type = None
    resources = None
    regions = None

    def run_terraformer(self):
        cmd = [ "terraformer" ]
        cmd.extend( ("import", self.resource_type) )
        if self.resources != None:
            cmd.extend( ("--resources", ",".join(self.resources)) )
        if self.regions != None:
            cmd.extend( ("--regions", ",".join(self.regions)) )
        self.log("cmd: %s" % cmd)

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

    def main(self):
        with open(DATA_PATH) as f:
            y = YAML(typ='safe').load(f)

        all_resources = [ k for k in y["resources"] ]
        self.resource_type = self.find_answer( y["resources"], "What resource type would you like to use? [%s] " % ','.join(all_resources) )[0]

        flattened_resources = [ i for k in y["resources"][self.resource_type] for i in k ]
        resource_fmt = self.outputfmt( flattened_resources )
        resource_a = self.find_answer( y["resources"][self.resource_type], "What resource(s) would you like to get? [\n%s] " % resource_fmt )

        sub_resources = []
        for r in resource_a:
            for r_n, r_v in r.items():
                subresource_fmt = self.outputfmt( r_v )
                sub_resources.extend( self.find_answer( r_v, "What sub-resources would you like to get? [\n%s] " % subresource_fmt ) )

        self.resources = sub_resources

        if "regions" in y and self.resource_type in y["regions"]:
            regions_fmt = self.outputfmt( y["regions"][self.resource_type] )
            self.regions = self.find_answer(y["regions"][self.resource_type], "What region(s) would you like to retrieve? [\n%s] " % regions_fmt )

        self.run_terraformer()


def main():
    t = TerraformerUIConsole()
    t.main()

if __name__ == "__main__":
    main()

