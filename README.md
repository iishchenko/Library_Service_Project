# Library Management System

## 📚 Overview
The **Library Management System** is a Django-based RESTful API that allows users to manage a library's book inventory and borrowing system. Users can borrow books, make payments for borrowings, and track the borrowing history. The system ensures that each user can only borrow books under their account, and administrators can manage the library's book collection and user data.

---

## 🚀 Features
### ✅ Book Management  
- Create, update, and delete books.  
- List available books with filtering and search options.  

### ✅ Borrowing Management  
- Borrow books with automatic due date calculation.  
- Track borrowed and returned books.  
- View borrowing history.  

### ✅ Payment Management  
- Create payments for borrowings.  
- Mark payments as completed.  
- Track payment status.  

### ✅ User Authentication  
- Secure user login using Django's authentication system.  
- Access control to ensure only the borrower can manage their borrowings.  

---

## 🏗️ Models
### 1. **Book**  
Represents a book in the library.  

| Field | Type | Description |
|-------|------|-------------|
| title | CharField | Title of the book |
| author | CharField | Author of the book |

### 2. **Borrowing**  
Tracks book borrowings.  

| Field | Type | Description |
|-------|------|-------------|
| book | ForeignKey | Related book |
| user | ForeignKey | Borrower |
| borrowed_at | DateTimeField | Timestamp of borrowing |
| due_date | DateTimeField | Due date for returning |
| returned_at | DateTimeField | Timestamp of return (nullable) |

### 3. **Payment**  
Handles payments for borrowings.  

| Field | Type | Description |
|-------|------|-------------|
| borrowing | OneToOneField | Related borrowing |
| user | ForeignKey | Borrower |
| amount | DecimalField | Payment amount |
| paid_at | DateTimeField | Timestamp of payment |
| payment_status | CharField | Status of payment (pending/completed/failed) |

---

## 🖥️ API Endpoints
### 📖 **Books**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Create a new book |
| GET | `/api/books/{id}/` | Retrieve book details |
| PUT | `/api/books/{id}/` | Update book details |
| DELETE | `/api/books/{id}/` | Delete a book |

### 🔄 **Borrowing**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/borrowings/{id}/` | Borrow a book |
| GET | `/api/borrowings/` | List all borrowings |
| GET | `/api/borrowings/{id}/` | Retrieve borrowing details |
| PATCH | `/api/borrowings/{id}/return/` | Mark a book as returned |

### 💳 **Payments**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/borrowings/{id}/payment/` | Create a payment |
| GET | `/api/borrowings/{id}/payment/` | Retrieve payment details |
| PATCH | `/api/borrowings/{id}/payment/` | Mark payment as completed |

---

## 💾 Installation
1. **Clone the repository:**
```bash
git clone https://github.com/iishchenko/Library_Service_Project/tree/developer
cd library-management
