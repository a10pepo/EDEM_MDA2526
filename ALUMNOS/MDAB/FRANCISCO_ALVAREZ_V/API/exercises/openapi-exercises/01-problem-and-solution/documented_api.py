"""
Documented Books API using Flask-RESTX
This API automatically generates Swagger UI documentation at /docs
"""

from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Initialize Flask-RESTX with API metadata
api = Api(
    app,
    version='1.0',
    title='Books API',
    description='A well-documented API for managing books. Compare this to the undocumented version!',
    doc='/docs'  # Swagger UI will be available at /docs
)

# Create a namespace for organizing endpoints
ns = api.namespace('api', description='Book operations')

# Define the Book model for Swagger documentation
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description='The book unique identifier'),
    'title': fields.String(required=True, description='Book title', example='1984'),
    'author': fields.String(required=True, description='Book author', example='George Orwell'),
    'year': fields.Integer(description='Publication year', example=1949),
    'isbn': fields.String(description='ISBN number', example='978-0451524935')
})

# Define the input model (without id, since it's auto-generated)
book_input = api.model('BookInput', {
    'title': fields.String(required=True, description='Book title', example='1984'),
    'author': fields.String(required=True, description='Book author', example='George Orwell'),
    'year': fields.Integer(description='Publication year', example=1949),
    'isbn': fields.String(description='ISBN number', example='978-0451524935')
})

# In-memory book storage
books = {
    1: {'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': 1949, 'isbn': '978-0451524935'},
    2: {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960, 'isbn': '978-0061120084'},
    3: {'id': 3, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'year': 1925, 'isbn': '978-0743273565'}
}
next_id = 4

@ns.route('/books')
class BookList(Resource):
    @ns.doc('list_books', params={
        'author': 'Filter books by author name (partial match)',
        'page': 'Page number for pagination (default: 1)',
        'limit': 'Number of books per page (default: 10)'
    })
    @ns.marshal_list_with(book_model)
    def get(self):
        """
        List all books
        Returns a list of books with optional filtering and pagination.
        """
        parser = api.parser()
        parser.add_argument('author', type=str, help='Filter by author name')
        parser.add_argument('page', type=int, default=1, help='Page number')
        parser.add_argument('limit', type=int, default=10, help='Books per page')
        args = parser.parse_args()

        result = list(books.values())

        # Filter by author if provided
        if args['author']:
            result = [b for b in result if args['author'].lower() in b['author'].lower()]

        # Pagination
        page = args['page']
        limit = args['limit']
        start = (page - 1) * limit
        end = start + limit
        paginated = result[start:end]

        return paginated

    @ns.doc('create_book')
    @ns.expect(book_input, validate=True)
    @ns.marshal_with(book_model, code=201)
    @ns.response(400, 'Validation Error')
    def post(self):
        """
        Create a new book
        Provide title and author (required), year and isbn (optional).
        """
        global next_id

        data = api.payload
        book = {
            'id': next_id,
            'title': data['title'],
            'author': data['author'],
            'year': data.get('year'),
            'isbn': data.get('isbn')
        }
        books[next_id] = book
        next_id += 1

        return book, 201

@ns.route('/books/<int:id>')
@ns.param('id', 'The book identifier')
class Book(Resource):
    @ns.doc('get_book')
    @ns.marshal_with(book_model)
    @ns.response(404, 'Book not found')
    def get(self, id):
        """
        Get a book by ID
        Returns a single book if it exists, otherwise returns 404.
        """
        if id not in books:
            api.abort(404, f"Book {id} not found")
        return books[id]

    @ns.doc('update_book')
    @ns.expect(book_input)
    @ns.marshal_with(book_model)
    @ns.response(404, 'Book not found')
    @ns.response(400, 'Validation Error')
    def put(self, id):
        """
        Update a book
        All fields are optional - only provided fields will be updated.
        """
        if id not in books:
            api.abort(404, f"Book {id} not found")

        data = api.payload
        book = books[id]

        if 'title' in data:
            book['title'] = data['title']
        if 'author' in data:
            book['author'] = data['author']
        if 'year' in data:
            book['year'] = data['year']
        if 'isbn' in data:
            book['isbn'] = data['isbn']

        return book

    @ns.doc('delete_book')
    @ns.response(204, 'Book deleted')
    @ns.response(404, 'Book not found')
    def delete(self, id):
        """
        Delete a book
        Permanently removes the book from the system.
        """
        if id not in books:
            api.abort(404, f"Book {id} not found")

        del books[id]
        return '', 204

if __name__ == '__main__':
    print("📚 Documented Books API is running!")
    print("📍 API: http://127.0.0.1:5000")
    print("📖 Swagger UI: http://127.0.0.1:5000/docs")
    print("📄 OpenAPI Spec: http://127.0.0.1:5000/swagger.json")
    print("\n✨ Much better than the undocumented version, right?")
    app.run(debug=True)
