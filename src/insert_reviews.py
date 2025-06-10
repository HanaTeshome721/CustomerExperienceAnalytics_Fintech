import oracledb
import pandas as pd

# Load data
df = pd.read_csv("../data/sentiment_reviews.csv")

# Connect to Oracle as SYS with SYSDBA mode
connection = oracledb.connect(
    user="sys",
    password="2112",  # Replace with your actual SYS password
    dsn="DESKTOP-5LBUK25/XEPDB1",
    mode=oracledb.AUTH_MODE_SYSDBA  # Important for SYS user!
)

cursor = connection.cursor()

# Insert unique banks and fetch their generated IDs
banks = df["bank"].unique()
bank_id_map = {}

for bank in banks:
    bank_id_var = cursor.var(int)
    cursor.execute(
        "INSERT INTO banks (bank_name) VALUES (:1) RETURNING bank_id INTO :2",
        [bank, bank_id_var]
    )
    bank_id_map[bank] = bank_id_var.getvalue()[0]  # getvalue() returns a list

# Insert reviews
for _, row in df.iterrows():
    date_str = pd.to_datetime(row["date"]).strftime('%Y-%m-%d')  # Convert to string for TO_DATE
    values = [
        bank_id_map.get(row["bank"]),
        row["review"],
        int(row["rating"]),
        date_str,
        row.get("sentiment_label"),
        row.get("sentiment_score"),
        row.get("identified_theme") or None
    ]
    cursor.execute("""
        INSERT INTO reviews (
            bank_id,
            review_text,
            rating,
            review_date,
            sentiment_label,
            sentiment_score,
            theme
        )
        VALUES (
            :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7
        )
    """, values)

connection.commit()
cursor.close()
connection.close()

print("✅ Data inserted into Oracle using oracledb.")
