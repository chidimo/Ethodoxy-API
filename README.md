# Ethordoxy

## Json files data structure for DR bible

new_test.json and old_test.json `{book name : [book url, book number]}`

chapters folder json files `{book name : {chapter number : chapter url }}`

verses folder json files `{book name-chapter number : {verse number : verse text}}`

How it works

Each verse is a single unit in the database table.

Each underlined item will link to a url. It will pass the following argument `book, chapter, underlined text`

To Do

Scrap topics from drbo.org
Include footnotes and cross-references for haydock
