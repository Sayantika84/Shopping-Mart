import re
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
def is_valid_email(email):
    return bool(re.match(email_pattern, email))

class Product:
    instances = []
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        Product.instances.append(self)
        
    def update_quantity(self, new_quantity): 
        self.quantity = new_quantity
    def display_info(self):
        print("Product Name:{}\tPrice:{}\tQuantity:{}".format(self.name,self.price,self.quantity))
    @classmethod
    def getProducts(cls):
        return Product.instances

class Customer:
    instances = []
    def __init__(self,name,email):
        self.name=name
        self.email=email
        #list of dictionaries: {product:quantity}
        self.order_history = []  
        Customer.instances.append(self)
    def add_order(self, order):
        """
        order : dictionary with {product:quantity,...}
        """
        self.order_history.append(order)
    def display_info(self):
        print(f"Customer Name: {self.name}\nEmail: {self.email}\n")
        ordercount=1
        for order in self.order_history:
            print(f"Order No.:{ordercount}\n")
            for key in order:
                print(f"\tProduct Name: {key.name}\tQuantity: {order[key]}\n")
            ordercount+=1;
            print("\n\n")
    @classmethod
    def getCustomers(cls):
        return Customer.instances
    
def process_order(product,quantity):
    if(product.quantity>=quantity):
        product.quantity-=quantity
        print(f"Order processed for {product.name}\tQuantity:{quantity}\tAmount:{product.price*quantity}")
        return True
    else:
        print(f"Order can't be processed for {product.name}")
        return False

class Cart:
    def __init__(self):
        self.item={}

    def add_product(self, product_name):
        """
        product_name : string
        returns : current quantity of the corresponding product in cart
        """
        products = Product.getProducts(); #object list
        product = None
        for p in products:
            if(p.name == product_name):
                product = p
                break
        if product is None:
            print("Order can't be processed! Product doesn't exist!\n")
            return
        
        if product in self.item:
            if(product.quantity-self.item[product]>0): 
                self.item[product]+=1;
            else:
                print("Out of Stock!")
        else:
            if(product.quantity>0): 
                self.item[product]=1
            else:
                print("Out of Stock!")
            
    def check_out(self, customer_name):
        """
        customer_name : string
        """
        customers = Customer.getCustomers() #object list
        customer = None
        for c in customers:
            if(c.name == customer_name):
                customer = c
                break
        if customer is None:
            print("Order can't be processed! Customer doesn't exist\n")
            return
        
        processed_orders={}
        for product in self.item:
            if process_order(product ,self.item[product]):
                processed_orders[product] = self.item[product]
        if processed_orders:
            customer.add_order(processed_orders)
        self.item={}

def save_to_file(filename, content):
    """
    content : list of objects : customers or products
    """
    if(filename == "products.txt"):
        products = content
        with open('products.txt', 'w') as f:
            for product in products:
                f.write(f"{product.name},{product.price},{product.quantity}\n")

    if(filename=="customers.txt"):
        customers = content
        with open('customers.txt', 'w') as f, open('order_history.txt','w') as f1:
            for customer in customers:
                f.write(f"{customer.name},{customer.email}\n")

                ######################################################
                #orderno,email,product_name,quantity,price per quantity
                ordercount=0
                for order in customer.order_history:
                    for key in order:
                        f1.write(f"{ordercount},{customer.email},")
                        f1.write(f"{key.name},{order[key]},{key.price}\n")
                    ordercount+=1

def load_from_file(filename):
    if(filename == "products.txt"):
        with open("products.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                name, price, quantity = line.strip().split(',')
                p1 = Product(name,int(price),int(quantity))
    if(filename == "customers.txt"):
        with open("customers.txt", "r") as f,open ("order_history.txt", "r") as f1 :
            lines = f.readlines()
            for line in lines:
                name, email = line.strip().split(',')
                c1 = Customer(name,email)
                ##########################################
                orders = f1.readlines()
                for order in orders:
                    orderno, email, pname,quantity,price = order.strip().split(',')
                    if(email==c1.email):
                        index = int(orderno)
                        while len(c1.order_history)<=index:
                            c1.order_history.append({})
                            
                        products = Product.getProducts(); #object list
                        product = None
                        for p in products:
                            if(p.name == pname):
                                product = p
                                break
                                
                        c1.order_history[index][product]=int(quantity)
                
def generate_sales_report(customers):
    print("Sales Report:\n")
    revenue=0
    pq={} # product:quantity
    for c in customers:
        for order in c.order_history:    #order : dict   order_history: List of dictionaries
            for product, quantity in order.items():
                revenue+=(quantity*product.price)
                if product in pq:
                    pq[product]+=quantity
                else:
                    pq[product]=quantity
    #most popular product
    print(f"Revenue: {revenue}\n")
    print(f"Most Popular Products:\n")

    sorted_pq = list(sorted(pq.items(), key=lambda x: x[1], reverse=True))
    for key, value in sorted_pq[:3] :
        print(f"{key.name}:{value} sold\n")

    return revenue, sorted_pq[:3]
    
def main():
    load_from_file("products.txt")
    load_from_file("customers.txt")
    while True:
        print("\nE-Commerce Management System\n1. Add Product\n2. Add Customer\n3. Process Order\n4. Generate Sales Report\n5. Exit\n")
        try:
            choice = int(input("Enter your choice: "))
            if(choice==1):
                name = input("Enter Product Name: ")
                price = int(input("Enter Product Price: "))
                quantity = int(input("Enter Product Quantity: "))
                assert quantity>=0, "Quantity can't be negative\n"
                assert price>0, "Price must be positive\n"
                
                products = Product.getProducts();         #product list
                product = None
                for p in products:
                    if(p.name == name):
                        product = p
                        break
    
                if product is None:
                    p1 = Product(name, price, quantity)
                    print("Product added successfully.\n")
                    p1.display_info()
                    print('\n')
                else:
                    print("Product already exists!\n")
                    c = (input("Do you want to update price and quantity?(y/n): "))
                    if(c.lower()=='y' or c.lower()=='yes'):
                        product.quantity+=quantity
                        product.price=price
                        print(f"Quantity & Price updated!\nQuantity:{product.quantity}\tPrice:{product.price}\n")
                    else:
                        print("Quantity & Price not updated!\n")
                    
            elif(choice==2):
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                assert is_valid_email(email), "Please input valid email!!"
                #check if customer is already there
                customers = Customer.getCustomers() #object list
                customer = None
                for c in customers:
                    if(c.email == email and c.name == name):
                        customer = c
                        break
    
                if customer is None:
                    c1 = Customer(name,email)
                    print("Customer added successfully!\n")
                    c1.display_info()
                else:
                    print("Customer already exists!\n")
    
            elif(choice==3):
                customer_name = input("Enter customer name: ")
                product_name = input("Enter product name: ")
                q = int(input("Enter Quantity: "))
                assert q>0, "quantity must be positive!\n"
                c1 = Cart()
                for i in range(q):
                    c1.add_product(product_name)
                c1.check_out(customer_name)
                print(f"Order processed successfully!\n")
                
            elif(choice==4):
                customers = Customer.getCustomers()
                generate_sales_report(customers)
            elif(choice==5):
                products = Product.getProducts();
                customers = Customer.getCustomers()
                save_to_file("products.txt",products)
                save_to_file("customers.txt",customers)
                print("Exiting...\n")
                break
            else:
                print("invalid choice!")
        except ValueError as e:
            print("input should be integer")
        except Exception as e:
            print( f"{type(e).__name__} : {e}")

            
if __name__=="__main__":
    main()
