import json


book_pages = {}


def read(path: str) -> str:
    global book_pages
    count = 0
    with open(path, 'r', encoding='utf-8') as file:
        while True:
            count += 1
            content = file.read(1050)
            if not content:
                break
            book_pages[str(count)] = content
    with open('services\\init_book.json', 'w', encoding='utf-8') as file1:
        json.dump(book_pages, file1, indent=4, ensure_ascii=False)
