SELECT books.bookName, books.Author, books.Summary, tfvalues.tfval
FROM books
INNER JOIN tfvalues 
ON books.bookName = tfvalues.doc
WHERE word = 'කෝට්ටේ' && books.bookID in (SELECT invertindex.indexval FROM invertindex where invertindex.word = 'කෝට්ටේ')



