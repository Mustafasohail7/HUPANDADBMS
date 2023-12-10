create table Admins
(AdminID varchar(5),
FullName varchar(40),
AdminPassword varchar(20),
primary key (AdminID));

create table Cafes
(CafeID varchar(5),
CafeName varchar(20),
CafeLocation varchar(20),
primary key(CafeID));

create table Items
(ItemID varchar(5),
ItemName varchar(20),
Price varchar(5),
ItemDescription varchar(200),
primary key (ItemID));

create table Menu
(CafeID varchar(5),
CafeName varchar(20),
ItemID varchar(5),
foreign key (CafeID) references Cafes,
foreign key (ItemID) references Items,
primary key (CafeID, ItemID));

create table CafeManagers
(AdminID varchar(5),
CafeID varchar(5),
foreign key (CafeID) references Cafes,
foreign key (AdminID) references Admins,
primary key (AdminID, CafeID));

create table Ingredients
(IngredientID varchar(5),
IngredientName varchar(20),
CostPerUnit varchar(10),
Quantity varchar(10),
primary key (IngredientID));

create table Recipes
(ItemID varchar(5),
IngredientID varchar(5),
foreign key (ItemID) references Items,
foreign key (IngredientID) references Ingredients,
primary key(ItemID,IngredientID));

create table Orders 
(OrderID varchar(10),
TimeOfOrder datetime,
OrderStatus varchar(10),
OrderBill int,
primary key (OrderID));

create table OrderItems
(ItemID varchar(5),
OrderID varchar(10),
OrderedQuantity int, 
Price int,
foreign key (ItemID) references Items,
foreign key (OrderID) references Orders,
primary key (ItemID, OrderID));

create table CafeOrders
(CafeID varchar(5),
OrderID varchar(10),
foreign key (CafeID) references Cafes,
foreign key (OrderID) references Orders,
primary key (CafeID, OrderID));

create table Customers
(CustomerID varchar(5),
CustomerName varchar(20),
CustomerAddress varchar(100),
PhoneNumber varchar(20),
CustomerPassword varchar(20),
primary key (CustomerID));


create table CustomerOrders
(CustomerID varchar(5),
OrderID varchar(10),
Feedback varchar(100),
Instructions varchar(100),
foreign key (CustomerID) references Customers,
foreign key (OrderID) references Orders,
primary key(CustomerID, OrderID));

