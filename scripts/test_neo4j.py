import os
from neo4j import GraphDatabase


def main():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    pwd = os.getenv("NEO4J_PASSWORD")
    db = os.getenv("NEO4J_DATABASE")

    if not uri or not user or not pwd:
        print("NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD must be set in environment variables")
        return 1

    print(f"Testing connectivity to {uri} (database={db or 'default'})")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, pwd))
        with driver:
            driver.verify_connectivity()
            if db:
                session = driver.session(database=db)
            else:
                session = driver.session()

            with session:
                result = session.run("RETURN 'ok' AS result").single()
                print("Query result:", result["result"]) 

        print("Success: Connected and query returned ok")
        return 0

    except Exception as e:
        print("Connection failed:", repr(e))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
