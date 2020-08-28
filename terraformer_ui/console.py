#!/usr/bin/env python3

import sys
import yaml

class TerraformerUIConsole(object):

    def outputfmt(self, lst):
        items = list( k for k in lst )
        stuff, it = '', iter(items)
        for i in it:
            stuff += '   {:<34}{:<34}{}'.format(i, next(it, ""), next(it, "") ) + "\n"
        return stuff

    def find_answer( self, obj, question ):
        answer = input(question)
        if answer == "":
            answer_lst = [k for k in obj ]
        else:
            answer_lst = [x.strip() for x in answer.split(',')]
        print("Selected: %s\n" % answer_lst)
        for answer in answer_lst:
            if not answer in obj:
                raise Exception("Error: invalid selection '%s'" % answer)
        return answer_lst

    ### Main program here ###

    def main(self):
        with open("resources.yaml") as f:
            y = yaml.safe_load(f)
            #print("y %s" % y)

        resources = [ k for k in y["resources"] ]
        resource_type = self.find_answer( y["resources"], "What resource type would you like to use? [%s] " % ','.join(resources) )[0]

        resource_fmt = self.outputfmt( y["resources"][resource_type].keys() )
        resource = self.find_answer( y["resources"][resource_type], "What resource(s) would you like to get? [\n%s] " % resource_fmt )

        #resource_lst = [x.strip() for x in resource.split(',')]
        sub_resources = []
        for r in resource:
            subresource_fmt = self.outputfmt( y["resources"][resource_type][r] )
            #sub_resource = input("What sub-resources would you like to get? ('all' for all) [\n%s] " % subresource_fmt )
            sub_resource = self.find_answer(y["resources"][resource_type][r], "What sub-resources would you like to get? [\n%s] " % subresource_fmt )
            sub_resources.extend( sub_resource )

        print("Sub-resources: %s" % sub_resources)


def main():
    t = TerraformerUIConsole()
    t.main()

if __name__ == "__main__":
    main()

