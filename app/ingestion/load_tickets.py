import pandas as pd
from sqlalchemy import create_engine


def main():
    db_user = "support"
    db_password = "support"
    db_host = "localhost"
    db_port = "5435"
    db_name = "support_analytics"

    print("Connexion à :", db_host, db_port, db_name)

    csv_path = "data/raw/support_tickets.csv"
    df = pd.read_csv(csv_path)

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    df.to_sql("support_tickets", engine, if_exists="append", index=False)

    print(f"{len(df)} tickets chargés !")


if __name__ == "__main__":
    main()