
db = db.getSiblingDB("bookstore");

// Step 3: Drop and reload authors
db.authors.drop();

let doc = JSON.parse(
  fs.readFileSync("authors.json", "utf8")
);
db.authors.insertMany(doc);

// Display authors
db.authors.find().forEach(printjson);

// Step 4: Drop and reload books
db.books.drop();

doc = JSON.parse(
  fs.readFileSync("books.json", "utf8")
);
db.books.insertMany(doc);

// Display books
db.books.find().forEach(printjson);

// Step 5: Find Good Omens
db.books.findOne({ title: "Good Omens" });

// Step 6: Add two books
db.books.insertMany([
  {
    title: "Harry Potter and the Sorcerer's Stone",
    published_year: 1997,
    author_ids: ["author_004"]
  },
  {
    title: "The Hobbit",
    published_year: 1937,
    author_ids: ["author_005"]
  }
]);

// Step 7: Add the missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "J.K. Rowling",
    nationality: "British",
    bio: {
      short: "British author best known for the Harry Potter series.",
      long: "J.K. Rowling is a British author best known for writing the Harry Potter fantasy series."
    }
  },
  {
    _id: "author_005",
    name: "J.R.R. Tolkien",
    nationality: "British",
    bio: {
      short: "English writer best known for The Hobbit and The Lord of the Rings.",
      long: "J.R.R. Tolkien was an English writer and scholar whose fantasy works include The Hobbit and The Lord of the Rings."
    }
  }
]);

// Step 8: Find books by Jane Austen or J.K. Rowling
db.books.find({
  author_ids: {
    $in: ["author_001", "author_004"]
  }
}).forEach(printjson);