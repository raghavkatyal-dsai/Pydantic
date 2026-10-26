from pydantic import BaseModel, Field, field_validator,AnyUrl, EmailStr, model_validator, computed_field

from typing import List, Optional, Dict

class Address(BaseModel):
    house_no:int
    floor:int = Field(title='Floor Number',description='Enter 0 for Ground Floor, 1 for First and so on.')
    area:str
    city:str
    pincode:int

    @field_validator('pincode',mode='before')
    @classmethod
    def pincode_validator(cls,value):
        value = str(value)
        if len(value)!=6:
            raise ValueError("Pincode Length should be exactly 6 digits.")
        return int(value)


class Restaurant(BaseModel):
    name:str
    rating:float = Field(gt=0,le=5)
    cuisines:List[str]
    website: Optional[AnyUrl] = None
    contact: Dict[str,int]
    email: str
    is_open : bool = Field(default=True,title="Restaurant Operator Status", description="True or False", examples=['True','False'])
    address: Address

    @field_validator('name')
    @classmethod
    def name_validator(cls,value):
        if len(value)>0 and len(value)<=50:
            return value.upper()
        raise ValueError("Max.Length of Restaurant Name is 50 characters.")

    @field_validator('email')
    @classmethod
    def partner_email_validator(cls,value):
        valid_domains = ['citybites.com','cbpartner.com']
        if value.split('@')[-1] not in valid_domains:
            raise ValueError("Partner Email is Invalid.")
        return value
    


class Customer(BaseModel):
    name:str
    age:int = Field(ge=1,le=99)
    email: EmailStr
    contact:Dict[str,int]
    allergies:Optional[List] = None
    social_media:Optional[List] = None
    wallet_balance:float = Field(ge=0)
    is_premium: bool = Field(default=False,title="Premium Customer?", description='True or False',examples=['True','False'])
    address: Address

    @model_validator(mode='after')
    def caretaker_over_60(cls,model):
        if model.age>60 and model.contact.get('caretaker',0)==0:
                raise ValueError("One Caretaker Contact is Required!")
        return model
            



    @field_validator('name')
    @classmethod
    def name_title(cls,value):
        return value.title()

    @field_validator('age',mode='before')
    @classmethod
    def age_validator(cls,value):
        return int(value)

    @field_validator('contact')
    @classmethod
    def contact_validator(cls,value):
        for key in value.keys():
            if len(str(value[key]))!=10:
                raise ValueError("Number should be exactly 10 digits.")
        return value
    


class OrderItem(BaseModel):
    dish_name:str
    quantity:int = Field(gt=0,le=20)
    unit_price:float = Field(gt=0)

    @computed_field
    @property
    def total_price(self) ->float:
        return (self.quantity*self.unit_price)


class Order(BaseModel):
    order_id:int
    customer: Customer
    restaurant:Restaurant
    order_items:List[OrderItem]
    delivery_address:Address
    coupon_code:Optional[str] = None


    @computed_field
    @property
    def final_bill(self) ->float:
        final_bill = 0
        for order in self.order_items:
            final_bill += order.total_price
        if self.coupon_code:
            final_bill = final_bill * (9/10)
        if self.customer.is_premium!=True:
            final_bill = final_bill + 40
        return final_bill

    @model_validator(mode='after')
    def alternate_contact_5000(cls,model):
        if model.final_bill>5000 and model.customer.contact.get('alternate',0)==0:
            raise ValueError("For Orders > 5000, a mandatory alternate contact is required.")
        return model

    @model_validator(mode='after')
    def city_validator(cls,model):
        if model.delivery_address.city!=model.restaurant.address.city:
            raise ValueError("Order should be from the same city as yours.")
        return model


    @field_validator('coupon_code')
    @classmethod
    def coupon_validator(cls,value):
        value = value.upper()
        if not value.startswith('CB'):
            raise ValueError("Coupon should start with 'CB'.")
        return value


def onboard_restuarant(restaurant:Restaurant):
    print("")
    print("Confirmation Receipt for Restaurant Registration")
    print("*"*10)
    print(f"Name: {restaurant.name}")
    print(f"Address: {restaurant.address}")
    print(f"Ratings: {restaurant.rating}")
    print(f"Cuisines: {restaurant.cuisines}")

def register_customer(customer:Customer):
    print("")
    print("Confirmation Receipt for Customer Registration")
    print("*"*10)
    print(f"Name: {customer.name}")
    print(f"Address: {customer.address}")
    print(f"Email: {customer.email}")
    print(f"Wallet Balance: {customer.wallet_balance}")

def process_order(order:Order):
    print("")
    print("Order Confirmation Receipt")
    print("*"*10)
    print(f"Name: {order.order_id}")
    print(f"Restaurant: {order.restaurant.name}")
    print(f"Final Bill: {order.final_bill}")
    print(f"Order Items: {order_printer(order.order_items)}")

def order_printer(order_items):
    orders = []
    for order in order_items:
        orders.append(f"{order.dish_name} X {order.quantity} X {order.unit_price} = {order.total_price}")
    return orders

# def fetch_order_data(order:Order,format,includes=None):
#     if format=='json':
#         data = order.model_dump_json(include=list(includes))
    
restaurant1 = Restaurant(**{
    'name': 'PUNJABI TADKA', 'rating': 4.3,
    'cuisines': ['North Indian', 'Mughlai'],
    'website': 'https://www.punjabitadka.in',
    'contact': {'manager': '9810012345', 'support': '9810067890'},
    'email': 'orders@cbpartner.com',
    'address': {'house_no': 4, 'floor': 0, 'area': 'Indiranagar',
                'city': 'Bengaluru', 'pincode': '560038'}
})
onboard_restuarant(restaurant1)

restaurant2 = Restaurant(**{
    'name': 'DOSA CORNER', 'rating': 3.9, 'cuisines': ['South Indian'],
    'contact': {'manager': '9900011122'}, 'email': 'dosa@citybites.com',
    'address': {'house_no': 22, 'floor': 1, 'area': 'Koramangala',
                'city': 'Bengaluru', 'pincode': 560034}
})

onboard_restuarant(restaurant2)
    
customer1 = Customer(**{
    'name': 'Riya Sharma', 'age': '29', 'email': 'riya.s@gmail.com',
    'contact': {'mobile': '9876501234', 'alternate': '9876509999'},
    'allergies': ['peanuts'],
    'social_media_urls': ['https://instagram.com/riya.s'],
    'wallet_balance': 250.5, 'is_premium': True,
    'address':{'house_no': 20, 'floor': 0, 'area': 'Koramangala',
                'city': 'Bengaluru', 'pincode': 560034}
    
})

register_customer(customer1)


customer_2 = Customer(**{
    'name': 'Harbans Singh', 'age': 67, 'email': 'hsingh@mail.com',
    'contact': {'mobile': '9876500000', 'caretaker': '9876511111','alternate':1234567890},
    'wallet_balance': 500.0,
    'address': {'house_no': 20, 'floor': 3, 'area': 'Indiranagar',
                'city': 'Bengaluru', 'pincode': 560038}
})

register_customer(customer_2)

items_small = [
    {'dish_name': 'Butter Chicken', 'quantity': 2, 'unit_price': 320.0},
    {'dish_name': 'Garlic Naan', 'quantity': 4, 'unit_price': 45.0},
]
items_big = [
    {'dish_name': 'Party Biryani Tray', 'quantity': 15, 'unit_price': 380.0},
]

order1 = Order(**{
    'order_id':1,
    'customer': customer1,
    'restaurant' : restaurant1,
    'order_items': items_small,
    'delivery_address':customer1.address
})

process_order(order1)

order2 = Order(**{
    'order_id':2,
    'customer': customer_2,
    'restaurant' : restaurant1,
    'order_items': items_big,
    'delivery_address':customer_2.address
})

process_order(order2)