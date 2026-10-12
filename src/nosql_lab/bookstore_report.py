
#!/usr/bin/env python3
"""Print a bookstore inventory report grouped by author."""

import logging
import os

import pymongo

# Read MongoDB Atlas credentials from environment variables.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Configure logging to display status and error messages.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def main():
    """Connect to MongoDB and print books grouped by author."""
    client = None

    try:
        # Check that all required environment variables are available.
        if not all(
            [MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]
        ):
            raise ValueError(
                "One or more MongoDB Atlas environment variables are missing."
            )

        # Connect to the Atlas cluster using the supplied credentials.
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000,
        )

        # Verify that the connection works.
        client.admin.command("ping")
        logging.info("Successfully connected to MongoDB Atlas.")

        # Select the bookstore database and its collections.
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Include two original authors and one author added in Case Study 1.
        author_ids = ["author_002", "author_003", "author_004"]

        # Count the authors selected for this report.
        author_count = authors.count_documents(
            {"_id": {"$in": author_ids}}
        )
        print(f"Authors: {author_count}\n")

        # Look up each author and find every book linked to that author.
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author not found: %s", author_id)
                continue

            print(author["name"])

            # A book can appear under multiple authors if it is co-authored.
            author_books = books.find(
                {"author_ids": author_id}
            ).sort("published_year", 1)

            found_book = False

            for book in author_books:
                print(
                    f"  {book['title']} ({book['published_year']})"
                )
                found_book = True

            if not found_book:
                print("  No books found.")

            print()

    except (pymongo.errors.PyMongoError, ValueError) as error:
        logging.error("Could not generate bookstore report: %s", error)

    finally:
        # Always close the client if it was created.
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()