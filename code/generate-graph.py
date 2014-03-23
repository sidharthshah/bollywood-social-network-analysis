import sys
import csv
import itertools
import networkx as nx

def clean_name(name):
    """
    This method is used to clean name
    """
    if name.find("[") != -1:
        name = name[:name.find("[")]
    return name.split(",")

def not_empty(x):
    """
    Filter function to check for non emptiness
    """
    return x.strip() != ""

def process_data(input_file, output_file):
    """
    This method is used to process data
    """
    X = nx.Graph()
    with open(input_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
        for record in reader:
            #Work with second last column
            cast = map(clean_name, record[-2].split("\xc2\xa0"))

            #We need to filter and flatten producing result
            cast = filter(not_empty, list(itertools.chain.from_iterable(cast)))

            #Extra step to clean white spaces in names
            remove_white_spaces = lambda x: x.strip()
            cast = map(remove_white_spaces, cast)

            #Update our graph G
            if len(cast) >= 2:
                X.add_edges_from([pair for pair in itertools.combinations(cast, 2)])

        nx.write_dot(X.closeness_centrality(), output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Please specify input and output file names"
        sys.exit(0)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_data(input_file, output_file)
