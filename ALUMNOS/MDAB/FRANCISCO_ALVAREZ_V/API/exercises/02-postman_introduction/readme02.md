
# Exercise: Exploring a Public API with Postman

## Quick Start

- This exercise uses Postman only; no Flask app to run.
- Install Postman, import or create requests, and follow the steps below.


## **Objective**
- Install and configure Postman.
- Perform a query to a public API to retrieve data.

---

## **Part 1: Installing Postman**

### 1. **Download Postman**
- Visit the official [Postman website](https://www.postman.com/downloads/).
- Download the version compatible with your operating system.

### 2. **Install Postman**
- Follow the installer instructions to complete the installation.

### 3. **Log in**
- Open Postman and create an account if you don't already have one. Alternatively, you can proceed as a guest.

---

## **Part 2: Choosing a Public API**
- We will use the [JSONPlaceholder](https://jsonplaceholder.typicode.com/) public API, which provides mock data for testing and learning.

---

## **Part 3: Making a Request**

### 1. **Open Postman**
- Start the Postman application.

### 2. **Create a new request**
- Click on **New Tab** or the **+** button on the top bar.

### 3. **Configure the request**
- **HTTP Method:** Select **GET**.
- **URL:** Enter the following URL:
  ```
  https://jsonplaceholder.typicode.com/posts/1
  ```
  (This retrieves a specific post with ID 1).

### 4. **Send the request**
- Click on the **Send** button.

### 5. **Analyze the response**
- Observe the response displayed in the lower panel. You should see something like:
  ```json
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  }
  ```

---

## **Part 4: Advanced Queries**

### 1. **Test other endpoints**
- Change the URL to:
  - `https://jsonplaceholder.typicode.com/posts` (Retrieves all posts).
  - `https://jsonplaceholder.typicode.com/users/1` (Retrieves information about a user).

### 2. **Add parameters**
- Try adding parameters like `?_limit=5` to the URL:
  ```
  https://jsonplaceholder.typicode.com/posts?_limit=5
  ```
  This limits the results to 5 posts.

---

## **Part 5: Additional steps**


### 1. **Additional tasks (optional)**
- Make a request using the **POST** method to add a new post:
  - Change the method to **POST**.
  - URL: `https://jsonplaceholder.typicode.com/posts`.
  - In the **Body** tab, select **raw** and choose **JSON**.
  - Enter a JSON object like this:
    ```json
    {
      "title": "My New Post",
      "body": "This is the content of the post",
      "userId": 1
    }
    ```
  - Click **Send** and observe the response.

---

## **Conclusion**
This exercise introduces basic concepts on how to use Postman to interact with a public API. You can experiment with other HTTP methods and endpoints to gain more familiarity with API capabilities.
