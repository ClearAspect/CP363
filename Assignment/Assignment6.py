import mysql.connector


def connect_db(use_database=True):
    if use_database:
        return mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="MovieMusicStore",
        )
    else:
        return mysql.connector.connect(
            host="localhost",
            user="",
            password="",
        )


def create_tables():
    """Create all tables from the CreateTables.sql file"""
    print("Creating database and tables...")
    conn = connect_db(use_database=False)
    cursor = conn.cursor()

    # Drop the database if it exists
    cursor.execute("DROP DATABASE IF EXISTS MovieMusicStore;")

    # Read the CREATE TABLE SQL commands from file
    with open("CreateTables.sql", "r") as file:
        create_commands = file.read()

    # Execute each command separately (split by semicolon)
    for command in create_commands.split(";"):
        if command.strip():
            try:
                cursor.execute(command + ";")
            except mysql.connector.Error as err:
                print(f"Warning: {err}")
                # Continue anyway as some errors might be expected

    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables created successfully!")


def populate_tables():
    """Populate tables with sample data from PopulateTables.sql"""
    print("Populating tables with sample data...")
    conn = connect_db()
    cursor = conn.cursor()

    # Read the INSERT SQL commands from file
    with open("PopulateTables.sql", "r") as file:
        populate_commands = file.read()

    # Execute each command separately (split by semicolon)
    for command in populate_commands.split(";"):
        if command.strip():
            try:
                cursor.execute(command + ";")
            except mysql.connector.Error as err:
                print(f"Error executing: {err}")
                continue

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables populated successfully!")


def display_results(cursor):
    columns = [i[0] for i in cursor.description]
    rows = cursor.fetchall()

    # Calculate appropriate column width based on content
    col_width = max(15, max([len(str(col)) for col in columns]) + 2)

    # Create format string based on number of columns using indexes to avoid issues with curly braces
    format_str = "".join(
        ["{" + str(i) + ":<" + str(col_width) + "}" for i in range(len(columns))]
    )

    print("-" * (col_width * len(columns)))
    print(format_str.format(*[str(col) for col in columns]))
    print("-" * (col_width * len(columns)))

    for row in rows:
        # Convert all values to string
        str_row = [str(col) for col in row]
        print(format_str.format(*str_row))

    print("-" * (col_width * len(columns)))


def menu():
    print("\n=== Movie Music Store Menu ===")
    print("1. Create Database Tables")
    print("2. Populate Tables with Sample Data")
    print("3. Create Customer Order Summary View")
    print("4. Create Movie Stock Ranking View")
    print("5. Create High Value Customer Orders View")
    print("6. View Customer Order Summary")
    print("7. View Movie Stock Ranking")
    print("8. View High Value Customer Orders")
    print("9. Exit")
    return input("Enter your choice: ")


def create_view(view_sql):
    """Create a view using the provided SQL"""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(view_sql)

        conn.commit()
        cursor.close()
        conn.close()
        print("View created successfully!")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")


def main():
    while True:
        choice = menu()
        if choice == "1":
            create_tables()
        elif choice == "2":
            populate_tables()
        elif choice == "3":
            create_view("""
CREATE OR REPLACE VIEW CustomerOrderSummaryView AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
    (SELECT COUNT(*) FROM `Order` o WHERE o.customer_id = c.customer_id) AS TotalOrders,
    (SELECT IFNULL(SUM(o.total_amount), 0) FROM `Order` o WHERE o.customer_id = c.customer_id) AS TotalSpent,
    (SELECT IFNULL(AVG(o.total_amount), 0) FROM `Order` o WHERE o.customer_id = c.customer_id) AS AvgOrderAmount
FROM Customer c;
            """)
        elif choice == "4":
            create_view("""
CREATE OR REPLACE VIEW MovieStockRanking AS
SELECT movie_id, title, stock_count,
       RANK() OVER (ORDER BY stock_count DESC) AS StockRank
FROM Movie;
            """)
        elif choice == "5":
            create_view("""
CREATE OR REPLACE VIEW HighValueCustomerOrders AS
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount
FROM `Order` o
WHERE o.customer_id IN (
    SELECT c.customer_id
    FROM Customer c
    JOIN `Order` o2 ON c.customer_id = o2.customer_id
    GROUP BY c.customer_id
    HAVING SUM(o2.total_amount) > (SELECT AVG(total_amount) FROM `Order`)
)
ORDER BY o.total_amount DESC;
            """)
        elif choice in ["6", "7", "8"]:
            try:
                conn = connect_db()
                cursor = conn.cursor()

                if choice == "6":
                    query = "SELECT * FROM CustomerOrderSummaryView;"
                elif choice == "7":
                    query = "SELECT * FROM MovieStockRanking;"
                elif choice == "8":
                    query = "SELECT * FROM HighValueCustomerOrders;"

                cursor.execute(query)
                display_results(cursor)

                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
