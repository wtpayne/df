import argparse
import memex_lib

def main(args):

    # documents = memex_lib.load_md_directory(args.input)
    documents = memex_lib.load_local_pdf(args.input)
    vectorstore = memex_lib.generate_vectors(documents)
    memex_lib.save_vectors(vectorstore)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create embedings for a set of inputs.')
    parser.add_argument('-i', '--input', type=str, help='input to analyse')
    parser.add_argument('-o', '--output_dir', type=str, help='output directory to save embedings')
    args = parser.parse_args()
    main(args)