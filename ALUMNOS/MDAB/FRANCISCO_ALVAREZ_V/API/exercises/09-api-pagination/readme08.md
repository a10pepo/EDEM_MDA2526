# Exercise 9: Implementing Pagination in Endpoints

## Quick Start

```bash
cd exercises/09-api-pagination
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-JWT-Extended Werkzeug
python app.py
```

## Objective

- **Implement Pagination in Endpoints:** Learn to handle large datasets by dividing them into smaller pages.
- **Response Optimization:** Improve API efficiency and usability by limiting the amount of data returned in each request.
- **Query Parameter Handling:** Use query parameters to control pagination.

## Description

In this exercise, you will implement pagination functionality in the `GET /students` route. Pagination will allow you to divide the list of students into smaller pages, controlled by query parameters such as `page` and `per_page`.

## Requirements

1. **Install Additional Dependencies:**
   - Make sure you have the `Flask` library and extensions used in previous exercises installed.
   - Use the `math` library (included by default in Python) to calculate the total number of pages.

2. **API Structure:**
   - **Paginated Route (`GET /students`):** Returns a paginated list of students, allowing you to specify the page number and the number of students per page through query parameters.

3. **Pagination Implementation:**
   - Use query parameters such as `page` and `per_page` to control pagination.
   - Calculate the start and end indices to return the correct subset of students.
   - Return additional information such as the total number of pages and the current page number.

4. **Testing:**
   - Use tools like Postman or `curl` to test pagination, requesting different pages and page sizes.
   - Ensure that pagination works correctly and that errors are handled appropriately (for example, pages out of range).

## Detailed Steps

1. **Configure the `/students` Route**:
   - Modify the route that handles `GET /students` to accept query parameters `page` and `per_page`.
   - Calculate the indices to get the subset of students according to the requested page.

2. **Calculate Total Pages:**
   - Use the formula `ceil(total / per_page)` to calculate the total number of pages, making sure to correctly handle non-integer divisions.

3. **Build Navigation Links:**
   - Use `request.base_url` and `urlencode` to generate `prev` and `next` links.

4. **Return the Response:**
   - Include the list of students from the requested page, pagination information, and navigation links.

## Code Example

```python
@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    try:
        # Get the query parameters 'page' and 'per_page' with default values
        page = request.args.get('page', 1, type=int)  # Current page
        per_page = request.args.get('per_page', 10, type=int)  # Students per page

        # Validate the 'per_page' value
        if per_page <= 0 or per_page > 100:
            return jsonify({'message': 'per_page must be between 1 and 100.'}), 400

        # Calculate the total number of students and pages
        total_students = len(students)  # Total registered students
        total_pages = math.ceil(total_students / per_page)  # Total number of pages

        # Validate the requested page range
        if page < 1 or page > total_pages:
            return jsonify({'message': 'Page not found.'}), 404

        # Determine the start and end indices of the student list
        start = (page - 1) * per_page  # Start index
        end = start + per_page  # End index
        students_list = list(students.keys())[start:end]  # Subset of students

        # Build links to navigate between pages
        base_url = request.base_url  # Base URL of the request
        query_params = request.args.to_dict()  # Current query parameters

        def build_url(new_page):
            # Build a URL with the updated page number
            query_params['page'] = new_page
            return f"{base_url}?{urlencode(query_params)}"

        # Create navigation links (prev and next)
        links = {}
        if page > 1:
            links['prev'] = build_url(page - 1)  # Link to previous page
        if page < total_pages:
            links['next'] = build_url(page + 1)  # Link to next page

        # Return the response with paginated data
        return jsonify({
            'students': students_list,  # List of students on the current page
            'total_pages': total_pages,  # Total number of pages
            'current_page': page,  # Current page
            'per_page': per_page,  # Number of students per page
            'total_students': total_students,  # Total registered students
            'links': links  # Navigation links
        }), 200

    except Exception as e:
        # General error handling
        return jsonify({'error': 'An error occurred while processing the request.', 'details': str(e)}), 500
```

## Testing with Postman or `curl`

1. **Request Specific Page:**

   ```bash
   curl -X GET "http://127.0.0.1:5000/students?page=2&per_page=5" -H "Authorization: Bearer <your_jwt_token>"
   ```

2. **Expected Result:**

   ```json
   {
     "students": ["student6", "student7", "student8", "student9", "student10"],
     "total_pages": 3,
     "current_page": 2,
     "per_page": 5,
     "total_students": 13,
     "links": {
       "prev": "http://127.0.0.1:5000/students?page=1&per_page=5",
       "next": "http://127.0.0.1:5000/students?page=3&per_page=5"
     }
   }
   ```

3. **Page Out of Range:**

   ```bash
   curl -X GET "http://127.0.0.1:5000/students?page=100&per_page=5" -H "Authorization: Bearer <your_jwt_token>"
   ```

   Response:

   ```json
   {
     "message": "Page not found."
   }
   ```

## Points to Consider

- Adjust the default and maximum values of `per_page` according to your API needs.
- Make sure to handle errors for requests with malformed or out-of-range parameters.
- Clearly document the accepted parameters in your API so clients can use them correctly.

Good luck with the implementation! If you have questions, don't hesitate to ask.
