# 🍔 CityBites: Food Delivery Order Engine

A pure Python + **Pydantic v2** project that builds the validation and billing layer for a food delivery platform. It accepts clean data, rejects bad data with clear error messages, and computes order bills automatically.

This project was built as a practice exercise to apply everything learned in the Pydantic section of my FastAPI course, on a fresh problem statement.

---

## 📌 Problem Statement

CityBites receives food orders for partner restaurants, but bad data keeps slipping through: lowercase restaurant names, fake partner emails, seniors with no caretaker contact, deliveries to a different city than the restaurant's, and so on.

This project is the **validation and processing layer** that:

- validates restaurants, customers, and orders,
- enforces business rules,
- computes the bill (subtotal, coupon discount, delivery fee),
- prints clean confirmation receipts.

---

## 🧱 Models

| Model | Purpose |
|---|---|
| `Address` | Nested model used inside Restaurant, Customer, and Order (as the delivery address) |
| `Restaurant` | Partner restaurant with rating, cuisines, contact info, and partner email |
| `Customer` | Customer profile with contact numbers, wallet, and premium status |
| `OrderItem` | A single dish with quantity, unit price, and a computed line total |
| `Order` | The main model: customer + restaurant + items + delivery address + optional coupon |

---

## ✅ Validation Rules

### Address
- Pincode must be exactly **6 digits** (accepts both `str` and `int`, and is converted to `int`)
- Floor has a description: `0` means Ground Floor

### Restaurant
- Name: max 50 characters, **auto-converted to uppercase**
- Rating: greater than 0 and at most 5
- Partner email must belong to `citybites.com` or `cbpartner.com`
- `website` is optional (`AnyUrl`)
- `is_open` defaults to `True`

### Customer
- Name is converted to **Title Case**
- Age is accepted as `str` or `int` (cleaned **before** type validation), range 1–99
- Every contact number must be exactly **10 digits**
- `allergies` and `social_media` are optional
- `is_premium` defaults to `False`
- 🔒 **Rule:** customers older than 60 must provide a `caretaker` contact

### OrderItem
- Quantity: greater than 0 and at most 20
- Unit price: greater than 0
- `total_price` is a **computed field** (`quantity × unit_price`)

### Order
- Coupon code (optional) must start with `CB` and is stored uppercase
- 🔒 **Rule 1:** delivery city must match the restaurant's city
- 🔒 **Rule 2:** if the final bill is above ₹5000, the customer must have an `alternate` contact

---

## 💰 Billing Logic

`final_bill` is a **computed field** on `Order`:

1. Sum of all item totals
2. 10% discount if a coupon code is present
3. ₹40 delivery fee for non-premium customers (free for premium)

**Example:** Butter Chicken (2 × 320) + Garlic Naan (4 × 45) = ₹820, then with a coupon: ₹820 × 0.9 = ₹738, plus ₹40 delivery for a non-premium customer = ₹778.

---

## 🧠 Pydantic Concepts Practiced

- `BaseModel` and nested models (Address → Customer / Restaurant → Order)
- `Field()` with `gt`, `ge`, `le`, `title`, `description`, `examples`, and `default`
- `Optional`, `List`, `Dict` from `typing`
- `EmailStr` and `AnyUrl`
- `@field_validator` (default `after` mode and `mode='before'`)
- `@model_validator(mode='after')` for cross-field rules
- `@computed_field` with `@property`
- Passing raw nested dicts and model instances inside dicts
- `**dict` unpacking to create models
- Type coercion (string → int)
- Models as typed function arguments

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Pydantic v2 with email support

### Installation

```bash
pip install pydantic email-validator
```

### Run

```bash
python city_bites_pydantic.py
```

### Sample Output

```
Order Confirmation Receipt
**********
Name: 1
Restaurant: PUNJABI TADKA
Final Bill: 820.0
Order Items: ['Butter Chicken X 2 X 320.0 = 640.0', 'Garlic Naan X 4 X 45.0 = 180.0']
```

---

## 🗂️ Project Structure

```
.
├── city_bites_pydantic.py   # All models, functions, and demo data
└── README.md
```

### Main functions

| Function | Description |
|---|---|
| `onboard_restuarant(restaurant)` | Prints a restaurant registration receipt |
| `register_customer(customer)` | Prints a customer registration receipt |
| `process_order(order)` | Prints the order receipt with the final bill and items |
| `order_printer(order_items)` | Helper that formats each order line |



## 🛠️ Tech Stack

- Python
- Pydantic v2
- email-validator


