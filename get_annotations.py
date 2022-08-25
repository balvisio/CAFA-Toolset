import argparse
from typeguard import typechecked

from Bio.UniProt.GOA import gafiterator, record_has


DEFAULT_EXPERIMENTAL_CODES = ["EXP", "IDA", "IPI", "IMP", "IGI", "IEP", "TAS", "IC"]

@typechecked
def create_annotation_file(uniprot_goa_path: str, exp_evidence_code: list, output_file_name:str):

    exp_evidence = {'Evidence': set(exp_evidence_code)}
    with open(output_file_name, "w") as annotation_file:
        with open(uniprot_goa_path, 'r') as goa_db:
            for rec in gafiterator(goa_db):
                if record_has(rec, exp_evidence):
                    annotation_file.write(rec["DB_Object_ID"] + "\t" + rec["GO_ID"] + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--uniprot-goa-db",
        help="Path to the UniProt-GOA database (.gaf) to get annotations from",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="annotations.dat",
        help="Output annotations file name"
    )

    parser.add_argument(
        '-e',
        '--evidence',
        nargs='*',
        default=DEFAULT_EXPERIMENTAL_CODES,
        help= "Provides user a choice to specify a set of GO experimental evidence codes " \
            "(example: IPI, IDA, EXP) separated by space. Default is: EXP, IDA, IPI, IMP, " \
            "IGI, IEP, TAS, IC.",
    )

    args = parser.parse_args()


    create_annotation_file(args.uniprot_goa_db, args.evidence, args.output)
