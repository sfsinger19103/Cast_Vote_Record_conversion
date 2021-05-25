import pandas as pd
from pathlib import Path
from typing import Optional

def cvrs_to_batch_totals(
        votes: Path,
        batches: Path,
        contest: str,
        out_path: Optional[Path],
) -> pd.DataFrame:
    df_votes = pd.read_excel(votes, index_col="Cast Vote Record")
    df_batches = pd.read_excel(batches, index_col="Cast Vote Record", skiprows=5)

    df_all = df_votes.merge(df_batches, how="left")
    df = df_all.groupby(["Batch", contest]).size().reset_index().pivot(index="Batch", columns=contest, values=0)
    if out_path:
        df.to_csv(out_path)
    return df

if __name__ == "__main__":
    v = "/Users/singer3/Documents/VerifiedVoting/ES&S files/Cast Vote Records Export.xlsx"
    b = "/Users/singer3/Documents/VerifiedVoting/ES&S files/CVR ID to Tabluator CVR Table.xlsx"
    c = "FAVORITE DOG BREED (18)"
    out = f"/Users/singer3/Documents/VerifiedVoting/ES&S files/{c.replace(' ', '-')}.csv"
    d_frame = cvrs_to_batch_totals(v, b, c, out)
    exit()
