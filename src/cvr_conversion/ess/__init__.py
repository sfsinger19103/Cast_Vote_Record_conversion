import pandas as pd
from pathlib import Path
import os
from typing import Optional, List

def cvrs_to_batch_totals(
        votes: Path,
        batches: Path,
        contest: str,
        out_path: Optional[Path],
        left_join_column: str,
        right_join_column: str,
) -> (pd.DataFrame, List[str]):
    """<votes> is a path to an ES&S Cast Vote Records Export (as of 2021)
    <batches> is a path to an ES&S CVR ID to Tabluator CVR Table file [sic]
    <contest> is the name of the contest (must match a column in the <votes> file)
    <out_path> is a path for the desired output. Returns a dataframe of the contest
    (rows are batch names, columns are totals for candidates) and, if <out_path> is given,
    writes to a csv file."""
    df = df_votes = df_batches = pd.DataFrame()  # for syntax-checker
    err = list()
    for f in [votes, batches]:
        if not os.path.isfile(f):
            err.append(f"Not a file: {f}")
    if out_path:
        out_dir = Path(out_path).parent
        if not os.path.isdir(out_dir):
            err.append(f"Directory for output not recognized: {out_dir}")
    if err:
        return df, err
    else:
        try:
            df_votes = pd.read_excel(votes)
            df_votes[left_join_column] = pd.to_numeric(
                df_votes[left_join_column], errors="coerce"
            ).fillna(0).astype("int64")
        except Exception as exc:
            err.append(f"Exception while reading {votes}:\n{exc}")
        try:
            df_batches = pd.read_excel(batches, skiprows=5)
            df_batches[right_join_column] = pd.to_numeric(
                df_batches[right_join_column], errors="coerce"
            ).fillna(0).astype("int64")

        except Exception as exc:
            err.append(f"Exception while reading {batches}:\n{exc}")
    if err:
        return df, err

    try:
        df_all = df_votes.merge(
            df_batches, how="left", left_on=left_join_column, right_on=right_join_column, suffixes=["_votes", ""]
        )
        df = df_all.groupby(["Batch", contest]).size().reset_index().pivot(index="Batch", columns=contest, values=0)
    except Exception as exc:
        err.append(f"Error during data manipulation: {exc}")
        return df, err
    if out_path:
        df.to_csv(out_path)
    return df, err

if __name__ == "__main__":
    v = "/Users/singer3/PycharmProjects/Cast_Vote_Record_conversion/samples/ess_2021/Cast Vote Records Export.xlsx"
    b = "/Users/singer3/PycharmProjects/Cast_Vote_Record_conversion/samples/ess_2021/CVR ID to Tabluator CVR Table.xlsx"
    c = "FAVORITE DOG BREED (18)"
    out = f"/Users/singer3/Documents/VerifiedVoting/ES&S files/{c.replace(' ', '-')}.csv"
    join_col = "Cast Vote Record"
    d_frame, e = cvrs_to_batch_totals(v, b, c, out, join_col, join_col)
    exit()
