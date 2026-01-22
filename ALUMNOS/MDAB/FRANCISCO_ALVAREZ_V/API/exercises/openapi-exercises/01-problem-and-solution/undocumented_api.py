"""
Undocumented Books API
This API has NO documentation - students must figure it out through trial and error.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory book storage
books = {
    1: {'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': 1949, 'isbn': '978-0451524935'},
    2: {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960, 'isbn': '978-0061120084'},
    3: {'id': 3, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'year': 1925, 'isbn': '978-0743273565'}
}
next_id = 4

@app.route('/')
def index():
    return 'Books API is running. But where are the endpoints? 🤔'

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    global next_id

    if request.method == 'GET':
        # Support filtering by author (but students don't know this!)
        author = request.args.get('author')
        # Support pagination (but students don't know the param names!)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        result = list(books.values())

        if author:
            result = [b for b in result if author.lower() in b['author'].lower()]

        # Simple pagination
        start = (page - 1) * limit
        end = start + limit
        paginated = result[start:end]

        return jsonify({
            'books': paginated,
            'total': len(result),
            'page': page,
            'limit': limit
        })

    else:  # POST
        data = request.get_json()

        # No validation error messages - students must guess what's wrong
        if not data:
            return jsonify({'error': 'Bad request'}), 400

        if 'title' not in data or 'author' not in data:
            return jsonify({'error': 'Bad request'}), 400

        book = {
            'id': next_id,
            'title': data['title'],
            'author': data['author'],
            'year': data.get('year'),
            'isbn': data.get('isbn')
        }
        books[next_id] = book
        next_id += 1

        return jsonify(book), 201

@app.route('/api/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(book_id):
    if request.method == 'GET':
        if book_id not in books:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(books[book_id])

    elif request.method == 'PUT':
        if book_id not in books:
            return jsonify({'error': 'Not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Bad request'}), 400

        # Update fields
        book = books[book_id]
        if 'title' in data:
            book['title'] = data['title']
        if 'author' in data:
            book['author'] = data['author']
        if 'year' in data:
            book['year'] = data['year']
        if 'isbn' in data:
            book['isbn'] = data['isbn']

        return jsonify(book)

    else:  # DELETE
        if book_id not in books:
            return jsonify({'error': 'Not found'}), 404

        deleted = books.pop(book_id)
        return jsonify({'message': 'Book deleted', 'book': deleted})

if __name__ == '__main__':
    print("🚀 Undocumented Books API is running!")
    print("📍 http://127.0.0.1:5000")
    print("❓ Can you figure out how to use it?")
    app.run(debug=True)
