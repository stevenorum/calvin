# calvin
Random python utilities to help out with problems that I find myself encountering frequently but that don't require full heavyweight packages themselves.
## calvin.aws
Various tools for use with AWS.
### calvin.aws.lambda_deployment
Helpers for publishing lambda functions from python code.
## calvin.cli
Helper for writing CLIs.
## calvin.files
Helpers for standard file interactions (reading and writing, mostly).  Largely just because I find the ```with open(foo) as bar:\n do_stuff``` idiom really annoying (even though I do recognize its utility).
## calvin.json
Helpers for common json stuff I need to do.  Includes...
* a decoder that handles numbers and dates (and complex objects if you add a method to them)
* wrappers around load(s) and dump(s) that use this decoder
* loadf and dumpf for going directly from file to object and back
* a method that'll print out the relevant section of a large json blob when a parse error is encountered
## calvin.setup
Wrapper that does stuff like automatically find packages and scripts and that pulls your dependencies from requirements.txt instead of them being hardcoded in setup.py
## calvin.shell
Wrapper around subprocess to cut out a few lines everytime you want to shell out to run a command.
