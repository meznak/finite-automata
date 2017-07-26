import argparse
from automata import automata
from utilities import utilities


def main(in_file: str, out_type: str, out_file: str, verbose: bool = False):
    if verbose:
        print(locals())

    fa1 = utilities.read_file(in_file)

    if verbose:
        print(fa1)
        print()

    # TODO: convert to use objects
    # TODO: finish implementing union
    fa2_file = [operations[k] for k in operations if operations[k] is not None]
    # if fa2_file[0]:
    #     fa2 = dict()
    #     fa2['fa_type'], fa2['sigma'], fa2['gamma'], fa2['states'], fa2['start'], fa2['final'], fa2[
    #         'delta'] = utilities.read_file(operations['union'])
    #     if verbose:
    #         print(fa2)
    #
    #     if operations['union'] is not None:
    #         result = automata.union(fa1, fa2)
    #         print(result)

    if out_type.upper() == 'CFG':
        if fa1.fa_type.upper() == 'PDA':
            fa_out = automata.pda_to_cfg(fa1, out_file and out_file[-3:] == 'tex')

    if fa_out and verbose:
        if out_file and out_file[-3:] == 'tex':
            print(fa_out.__str__(format='tex'))
        else:
            print(fa_out)
        print()

    if fa_out and out_file:
        with open(out_file, 'w') as f:
            if out_file[-3:] == 'tex':
                f.write(fa_out.__str__(format='tex'))
            else:
                f.write(str(fa_out))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--in-file", dest='in_file', required=True, help="Input file name")
    parser.add_argument("-ot", "--out-type", dest='out_type', help="Output file type")
    parser.add_argument("-of", "--out-file", dest='out_file', default=None, help="Output file name")
    parser.add_argument("-u", "--union", dest='union_file', help="Union with another FA")
    parser.add_argument("-i", "--isect", dest='isect_file', help="Intersect with another FA")
    parser.add_argument("-c", "--concat", dest='concat_file', help="Concatenate with another FA")
    parser.add_argument("-s", "--star", dest='star', action='store_true', help="Star")
    parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', default=False, help="Print debug info")
    args = parser.parse_args()
    operations = dict(
        [('union', args.union_file), ('isect', args.isect_file), ('concat', args.concat_file), ('star', args.star)])
    main(args.in_file, args.out_type, args.out_file, args.verbose)
