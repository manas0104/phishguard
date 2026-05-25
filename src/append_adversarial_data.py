import pandas as pd

# ----------------------------
# LOAD MAIN DATASET
# ----------------------------
df = pd.read_csv("data/url_dataset.csv")

# ----------------------------
# LOAD ADVERSARIAL URLS
# ----------------------------
with open(
    "data/adversarial_phishing_urls.txt",
    "r"
) as f:

    adversarial_urls = [
        line.strip()
        for line in f
        if line.strip()
    ]

# ----------------------------
# CREATE ADVERSARIAL DATAFRAME
# ----------------------------
adversarial_df = pd.DataFrame({
    "url": adversarial_urls,
    "label": -1
})

# ----------------------------
# APPEND TO MAIN DATASET
# ----------------------------
df = pd.concat(
    [df, adversarial_df],
    ignore_index=True
)

# ----------------------------
# SAVE UPDATED DATASET
# ----------------------------
df.to_csv(
    "data/url_dataset.csv",
    index=False
)

print(
    f"Added {len(adversarial_urls)} adversarial phishing URLs."
)