import pandas as pd
import json
import os
from datetime import datetime


# ---------------------------------------
# Detect Exact Duplicates
# ---------------------------------------

def detect_exact_duplicates(df):

    exact_count = df.duplicated().sum()

    dup_rows = df[df.duplicated(
        keep=False
    )].sort_values(by=df.columns.tolist())


    print("\nEXACT DUPLICATE DETECTION")
    print("=" * 60)

    print(f"Exact duplicates found: {exact_count}")
    print(
        f"Total duplicate rows including originals: {len(dup_rows)}"
    )


    if len(dup_rows) > 0:
        print("\nSample duplicates:")
        print(
            dup_rows.head(10).to_string()
        )


    return exact_count, dup_rows



# ---------------------------------------
# Detect Near Duplicates
# ---------------------------------------

def detect_near_duplicates(df, key_columns):

    duplicate_keys = df[
        df.duplicated(
            subset=key_columns,
            keep=False
        )
    ]


    print("\nNEAR DUPLICATE DETECTION")
    print("=" * 60)

    print(
        f"Records with duplicate keys: {len(duplicate_keys)}"
    )

    print(
        f"Duplicate key groups: {duplicate_keys.groupby(key_columns).ngroups}"
    )


    if len(duplicate_keys):

        print("\nSample duplicate groups:")

        for keys, group in list(
            duplicate_keys.groupby(key_columns)
        )[:3]:

            print("\nKey:", keys)
            print(group)


    return duplicate_keys



# ---------------------------------------
# Remove Exact Duplicates
# ---------------------------------------

def remove_exact_duplicates(df, keep="first"):

    before = len(df)


    df = df.drop_duplicates(
        keep=keep
    )


    after = len(df)


    print("\nEXACT DUPLICATE REMOVAL")
    print("=" * 60)

    print("Rows before:", before)
    print("Rows after:", after)
    print("Removed:", before-after)


    return df



# ---------------------------------------
# Remove Near Duplicates
# ---------------------------------------

def remove_near_duplicates(
        df,
        key_columns,
        keep_strategy="most_complete"
):

    before = len(df)


    if keep_strategy == "most_complete":


        def choose_best(group):

            null_count = group.isnull().sum(axis=1)

            return group.loc[
                [null_count.idxmin()]
            ]


        df = (
            df.groupby(
                key_columns,
                group_keys=False
            )
            .apply(choose_best)
            .reset_index(drop=True)
        )


    elif keep_strategy == "last":

        df = df.drop_duplicates(
            subset=key_columns,
            keep="last"
        )


    else:

        df = df.drop_duplicates(
            subset=key_columns,
            keep="first"
        )



    after = len(df)


    print("\nNEAR DUPLICATE REMOVAL")
    print("=" * 60)

    print("Rows before:", before)
    print("Rows after:", after)
    print("Removed:", before-after)


    return df



# ---------------------------------------
# Audit Logging
# ---------------------------------------

def log_removed_duplicates(
        original,
        deduped
):


    removed = original[
        ~original.index.isin(
            deduped.index
        )
    ]


    os.makedirs(
        "output",
        exist_ok=True
    )


    removed.to_csv(
        "output/removed_duplicates_audit.csv",
        index=False
    )


    summary = {

        "timestamp":
            datetime.now().isoformat(),

        "removed_records":
            len(removed),

        "reason":
            "Duplicate detection and removal"

    }


    with open(
        "output/dedup_audit_summary.json",
        "w"
    ) as f:

        json.dump(
            summary,
            f,
            indent=4
        )


    print("\nAudit file created")

    return removed



# ---------------------------------------
# Before After Comparison
# ---------------------------------------

def compare_before_after(
        original,
        deduped
):


    result = {

        "rows_before":
            len(original),

        "rows_after":
            len(deduped),

        "rows_removed":
            len(original)-len(deduped),

        "columns":
            len(original.columns),

        "nulls_before":
            int(original.isnull().sum().sum()),

        "nulls_after":
            int(deduped.isnull().sum().sum()),

        "timestamp":
            datetime.now().isoformat()

    }



    with open(
        "output/dedup_summary.json",
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )


    print("\nFINAL SUMMARY")
    print("="*60)

    print(result)


    return result



# ---------------------------------------
# Main Workflow
# ---------------------------------------

if __name__ == "__main__":


    os.makedirs(
        "data/processed",
        exist_ok=True
    )


    df = pd.read_csv(
        "data/raw/Slack_queries.csv"
    )


    original_df = df.copy()



    print("="*70)

    print("STARTING DEDUPLICATION")

    print("="*70)

    print(
        "Initial rows:",
        len(df)
    )



    # Task 1

    detect_exact_duplicates(df)



    # Task 2

    key_columns = [

        "Student or WP",

        "Program Name",

        "Created Time (Ticket)",

        "Project Phase"

    ]


    detect_near_duplicates(
        df,
        key_columns
    )



    # Task 3

    df = remove_exact_duplicates(
        df,
        keep="first"
    )



    # Task 4

    df = remove_near_duplicates(
        df,
        key_columns,
        "most_complete"
    )



    # Task 5

    log_removed_duplicates(
        original_df,
        df
    )



    # Task 6

    compare_before_after(
        original_df,
        df
    )



    df.to_csv(
        "data/processed/deduplicated_tickets.csv",
        index=False
    )


    print(
        "\nSaved:",
        "data/processed/deduplicated_tickets.csv"
    )