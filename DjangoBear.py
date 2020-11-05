from email import message
import logging

from coalib.bears.LocalBear import LocalBear


class DjangoBear(LocalBear):
    def run(self, filename, file):
        """

        Looks at a python file and returns start and ends of a function.
        """

        logging.debug("Checking file: ", filename, ".")

        def find_end(l):
            """

            Looks where a given function ends and returns the line number.

            :param i: Indent of start of function.
            :param l: Line number of start of function.

            """
            i = len(file[l]) - len(file[l].lstrip())
            #Start search at next line
            start = l+1
            print("start indent:", i, "line:", l)
            
            for m, line in enumerate(file[start:], start=start):
                print
                indent = len(line) - len(line.lstrip())
                if indent == i:
                    return m
            return len(file)-1

        if "views.py" in filename:

            # start and end of function variables
            start = 0
            end = 0
            for l, line in enumerate(file):
                # Check for tag
                #indent = len(line) - len(line.lstrip())

                # Register start function
                if str.lower(line).startswith("def "):
                    print("finding end of ", line)
                    m = find_end(l)
                    print("start:", file[l])
                    print(m)
                    print("end:", file[m], "\n")

            yield self.new_result(message="Choose option.", file=filename)
