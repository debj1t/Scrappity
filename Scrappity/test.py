import argparse


# Parser handle to parse the arguments
parser = argparse.ArgumentParser()

# Add positional argument
parser.add_argument("url",
                    help="url address to crawl")

# Add optional arguments
parser.add_argument("-p",
                    "--path",
                    help="path to store downloaded files")


parser.add_argument("-g",
                    "--genre",
                    help="download files specific to genre")

parser.add_argument("-l",
                    "--limit",
                    type=int,
                    default=1,
                    help="limit downloaded files count")

parser.add_argument("-v",
                    "--verbose",
                    action="store_true",
                    help="increase output verbosity")

# Parse all the arguments
args = parser.parse_args()

# Print limit value
print (args.limit)
