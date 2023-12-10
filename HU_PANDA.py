from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from PyQt6.QtWidgets import QMessageBox

server = 'LAPTOP-G29PD2R1'
database = 'HUPanda'                    # Name of database
use_windows_authentication = True       


# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# global variables to access in other classes
current_customer_id = ''
cart_items = []
    
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
    
        uic.loadUi('Login Form.ui', self)

        # Find the login button and connect it to the handleLogin function
        self.loginButton = self.findChild(QtWidgets.QPushButton, 'LoginButton')  
        self.loginButton.clicked.connect(self.handleLogin)

        # Find the username and password line edits
        self.userIDLineEdit = self.findChild(QtWidgets.QLineEdit, 'userID')  
        self.passwordLineEdit = self.findChild(QtWidgets.QLineEdit, 'Password')  
        
        self.signUpButton = self.findChild(QtWidgets.QPushButton, 'SignUpButton')
        self.signUpButton.clicked.connect(self.openRegistrationWindow)
        
        self.AdminButton = self.findChild(QtWidgets.QPushButton, 'AdminButton')
        self.AdminButton.clicked.connect(self.OpenAdminLogin)
        
    def openRegistrationWindow(self):
        self.close()
        self.registrationWindow = RegistrationWindow()
        self.registrationWindow.show()
        
    def OpenAdminLogin(self):
        self.close()
        self.adminWindow = AdminWindow()
        self.adminWindow.show()
        
    
    def openCustomerHome(self):
        self.close()
        self.customerHome = CustomerHome()  
        self.customerHome.show()    
        
    def handleLogin(self):
        username = self.userIDLineEdit.text()
        password = self.passwordLineEdit.text()
        
        global current_customer_id
        current_customer_id = username
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        username_query = "SELECT CustomerID FROM Customers"
        cursor.execute(username_query)
        usernames = [row[0] for row in cursor.fetchall()]

        if username not in usernames:
            QMessageBox.warning(self, 'Error', 'Username is incorrect')
            connection.close()
            return
        
        password_query = """
            Select CustomerPassword from Customers where CustomerID = ?
        """
        cursor.execute(password_query, username)
        result = cursor.fetchone()
        connection.close()

        # Check if a result was found and compare the password
        if result and result[0] == password:
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.openCustomerHome()  
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Password')
        

class RegistrationWindow(QMainWindow):
    def __init__(self):
        super(RegistrationWindow, self).__init__()
        uic.loadUi('User Registration Form.ui', self)
        self.registerButton = self.findChild(QtWidgets.QPushButton, 'AddUser')  
        self.registerButton.clicked.connect(self.registerUser)

    def registerUser(self):
        # Retrieve data from line edits
        userID = self.findChild(QtWidgets.QLineEdit, 'EnterID').text()
        userName = self.findChild(QtWidgets.QLineEdit, 'EnterName').text()
        userPassword = self.findChild(QtWidgets.QLineEdit, 'EnterPassword').text()
        userPhone = self.findChild(QtWidgets.QLineEdit, 'EnterPhone').text()
        userAddress = self.findChild(QtWidgets.QLineEdit, 'EnterAddress').text()
        
        if not userID or not userName or not userPassword or not userPhone or not userAddress:
            QMessageBox.warning(self, 'Error', 'Enter all details')
        else:
            try:
                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor() 

                # SQL query to insert new user data
                insert_query = "INSERT INTO Customers (CustomerID, CustomerName, CustomerAddress, PhoneNumber, CustomerPassword) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(insert_query, (userID, userName, userAddress,userPhone,userPassword))
                connection.commit()

                QMessageBox.information(self, 'Success', 'Registration successful!')
                
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to register user: {e}')
            finally:
                connection.close()
                self.BackToLogin()
            
            
    def BackToLogin(self):
        self.close()
        self.returntologin = LoginWindow()
        self.returntologin.show()
                    
        
class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        uic.loadUi('Admin Login Form.ui', self)
        self.userIDLineEdit = self.findChild(QtWidgets.QLineEdit, 'userID')  
        self.passwordLineEdit = self.findChild(QtWidgets.QLineEdit, 'Password')  
        self.loginButton = self.findChild(QtWidgets.QPushButton, 'LoginButton')  
        
        self.loginButton.clicked.connect(self.handleLogin)
    
    def handleLogin(self):
        username = self.userIDLineEdit.text()
        password = self.passwordLineEdit.text()
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        username_query = "SELECT AdminID FROM Admins"
        cursor.execute(username_query)
        usernames = [row[0] for row in cursor.fetchall()]

        if username not in usernames:
            QMessageBox.warning(self, 'Error', 'Username is incorrect')
            connection.close()
            return
        
        password_query = """
            Select AdminPassword from Admins where AdminID = ?
        """
        cursor.execute(password_query, username)
        result = cursor.fetchone()
        connection.close()

        # Check if a result was found and compare the password
        if result and result[0] == password:
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.OpenAdminHome()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Password')
    
    def OpenAdminHome(self):
        self.close()
        self.adminHome = AdminHome()  
        self.adminHome.show()   


class AdminHome(QMainWindow):
    def __init__(self):
        super(AdminHome, self).__init__()
        uic.loadUi('AdminHome.ui', self)
        
        self.addButton = self.findChild(QtWidgets.QPushButton, 'AddtoItems')
        self.addButton.clicked.connect(self.openAddItemToItem)
        
        self.DELETEITEMBUTTON = self.findChild(QtWidgets.QPushButton, 'DeleteItemFromItems')
        self.DELETEITEMBUTTON.clicked.connect(self.openDeleteItemFromItems)

        self.deleteButton = self.findChild(QtWidgets.QPushButton, 'DeleteItem')
        self.deleteButton.clicked.connect(self.openDeleteItemFromMenu)

        self.viewInventoryButton = self.findChild(QtWidgets.QPushButton, 'ViewInventory')
        self.viewInventoryButton.clicked.connect(self.openViewInventory)

        self.manageInventoryButton = self.findChild(QtWidgets.QPushButton, 'ManageInventory')
        self.manageInventoryButton.clicked.connect(self.openManageInventory)

        self.viewOrdersButton = self.findChild(QtWidgets.QPushButton, 'ViewOrders')
        self.viewOrdersButton.clicked.connect(self.openViewOrders)
        
        self.addtomenuButton = self.findChild(QtWidgets.QPushButton, 'AddtoMenu')
        self.addtomenuButton.clicked.connect(self.openAddToMenu)

    def openAddItemToItem(self):
        self.addItemWindow = AddItemToItemWindow()  
        self.addItemWindow.show()

    def openDeleteItemFromMenu(self):
        self.deleteItemWindow = DeleteItemFromMenuWindow() 
        self.deleteItemWindow.show()

    def openViewInventory(self):
        self.viewInventoryWindow = ViewInventoryWindow()  
        self.viewInventoryWindow.show()

    def openManageInventory(self):
        self.manageInventoryWindow = ManageInventoryWindow()  
        self.manageInventoryWindow.show()

    def openViewOrders(self):
        self.viewOrdersWindow = ViewOrdersWindow()  
        self.viewOrdersWindow.show()
        
    def openAddToMenu(self):
        self.viewaddtomenu = AddExistingItemToMenu()  
        self.viewaddtomenu.show()
        
    def openDeleteItemFromItems(self):
        self.deleteitemwindow = DeleteItems()
        self.deleteitemwindow.show()
        

class DeleteItems(QMainWindow):
    def __init__(self):
        super(DeleteItems, self).__init__()
        uic.loadUi('DeleteItemFromItems.ui', self)
        self.deleteitembutton = self.findChild(QtWidgets.QPushButton, 'DeleteItemFromItems')
        
        self.selectItemToDelete = self.findChild(QtWidgets.QComboBox, 'SelectItemToDelete')

        self.deleteitembutton.clicked.connect(self.deleteItem)

        self.populateItemSelector()
        
    def populateItemSelector(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT ItemName FROM Items")
            items = cursor.fetchall()
            self.selectItemToDelete.clear()

            for item in items:
                self.selectItemToDelete.addItem(item[0])

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load items: {e}')
        finally:
            connection.close()

    def deleteItem(self):
        selectedItem = self.selectItemToDelete.currentText()

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Check if the item exists in the Menu table
            cursor.execute("SELECT COUNT(*) FROM Menu WHERE ItemName = ?", selectedItem)
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, 'Error', 'Cannot delete item as it exists in the Menu.')
                return

            # Delete the item from the Items table
            cursor.execute("DELETE FROM Items WHERE ItemName = ?", selectedItem)
            connection.commit()
            QMessageBox.information(self, 'Success', f'Item "{selectedItem}" deleted successfully.')
            self.populateItemSelector()  # Refresh the item selector

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete item: {e}')
        finally:
            connection.close()
        

# Class for "Add Item to Menu" Window
class AddItemToItemWindow(QMainWindow):
    def __init__(self):
        super(AddItemToItemWindow, self).__init__()
        uic.loadUi('additemtoitems.ui', self)
        self.itemIDLineEdit = self.findChild(QtWidgets.QLineEdit, 'ItemID')
        self.itemNameLineEdit = self.findChild(QtWidgets.QLineEdit, 'ItemName')
        self.itemPriceLineEdit = self.findChild(QtWidgets.QLineEdit, 'ItemPrice')
        self.itemDescriptionTextEdit = self.findChild(QtWidgets.QPlainTextEdit, 'ItemDescription')
        self.addItemButton = self.findChild(QtWidgets.QPushButton, 'addItemBtn')  
        print(self.findChild(QtWidgets.QPushButton, 'addItemBtn'))

        
        self.addItemButton.clicked.connect(self.addItemToDatabase)
        self.loadIngredients()
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        query = "SELECT MAX(ItemID) FROM Items"  
        cursor.execute(query)
        item_id = cursor.fetchall()
        item_id = int(item_id[0][0])
        item_id += 1
        item_id = str(item_id)
        self.itemIDLineEdit.setText(item_id)
        self.itemIDLineEdit.setDisabled(True)
        
        
    def loadIngredients(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT IngredientID,IngredientName FROM Ingredients"  
            cursor.execute(query)
            ingredients = cursor.fetchall()

            self.itemIngredientsListWidget = self.findChild(QtWidgets.QListWidget, 'ItemIngredients')
            self.itemIngredientsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
            self.ingredientNameToID = dict()
            for ingredient in ingredients:
                self.itemIngredientsListWidget.addItem(ingredient[1])
                self.ingredientNameToID[ingredient[1]] = ingredient[0]

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load ingredients: {e}')
        finally:
            connection.close()


    def addItemToDatabase(self):
        itemID = self.itemIDLineEdit.text()
        itemName = self.itemNameLineEdit.text()
        itemPrice = self.itemPriceLineEdit.text()
        itemDescription = self.itemDescriptionTextEdit.toPlainText()
        selectedItems = self.itemIngredientsListWidget.selectedItems()
        selectedIngredientIDs = [self.ingredientNameToID[item.text()] for item in selectedItems]
        selectedIngredients = [item.text() for item in selectedItems]
            
        # Validate inputs 
        if not itemName or not itemPrice:
            QMessageBox.warning(self, 'Error', 'All fields must be filled')
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # SQL query to insert new item data
            insert_query = "INSERT INTO Items (ItemID, ItemName, Price, ItemDescription) VALUES (?, ?, ?, ?)"
            insert_query_2 = "INSERT INTO Recipes (ItemID,IngredientID) VALUES (?,?)"
            cursor.execute(insert_query, (itemID, itemName, itemPrice, itemDescription))
            
            for i in selectedIngredientIDs:
                # print(i)
                # pass
                cursor.execute(insert_query_2, (itemID,i))

            connection.commit()
            QMessageBox.information(self, 'Success', 'Item added successfully')

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to add item: {e}')
        finally:
            connection.close()
    
      
class AddExistingItemToMenu(QMainWindow):
    def __init__(self):
        super(AddExistingItemToMenu, self).__init__()
        uic.loadUi('AddExistingItemtoMenu.ui', self)

        
        self.itemSelector = self.findChild(QtWidgets.QComboBox, 'ItemSelector')
        self.cafeSelector = self.findChild(QtWidgets.QComboBox, 'CafeSelector')
        self.addToMenuButton = self.findChild(QtWidgets.QPushButton, 'AddToMenu')

        
        self.addToMenuButton.clicked.connect(self.addMenuItemToMenu)

        
        self.populateItemSelector()

    def populateItemSelector(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT ItemName FROM Items"  
            cursor.execute(query)
            items = cursor.fetchall()

            for item in items:
                self.itemSelector.addItem(item[0])

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load items: {e}')
        finally:
            connection.close()

    def addMenuItemToMenu(self):
        selectedCafe = self.cafeSelector.currentText()
        selectedItem = self.itemSelector.currentText()

        if not selectedItem or not selectedCafe:
            QMessageBox.warning(self, 'Error', 'Item or Cafe not selected')
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Check if the item is already in the menu for the selected cafe
            check_query = "SELECT * FROM Menu WHERE CafeName = ? AND ItemName = ?"
            cursor.execute(check_query, selectedCafe, selectedItem)
            existing_entry = cursor.fetchone()

            if existing_entry:
                QMessageBox.warning(self, 'Error', 'Item already in the menu for the selected cafe')
            else:
                # Fetch ItemID and Price from the Items table
                fetch_query = "SELECT ItemID, Price FROM Items WHERE ItemName = ?"
                cursor.execute(fetch_query, selectedItem)
                item_data = cursor.fetchone()
                if item_data:
                    item_id, price = item_data
                    # Insert the selected item into the Menu table for the selected cafe
                    if selectedCafe == 'Cafe2Go':
                        insert_query = "INSERT INTO Menu (CafeID, CafeName, ItemID, ItemName, Price) VALUES (2, ?, ?, ?, ?)"
                        cursor.execute(insert_query, selectedCafe, item_id, selectedItem, price)
                        connection.commit()
                        QMessageBox.information(self, 'Success', 'Item added to the menu successfully')
                    else:
                        insert_query = "INSERT INTO Menu (CafeID, CafeName, ItemID, ItemName, Price) VALUES (1, ?, ?, ?, ?)"
                        cursor.execute(insert_query, selectedCafe, item_id, selectedItem, price)
                        connection.commit()
                        QMessageBox.information(self, 'Success', 'Item added to the menu successfully')

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to add item to the menu: {e}')
        finally:
            connection.close()


# Class for "Delete Item from Menu" Window
class DeleteItemFromMenuWindow(QMainWindow):
    def __init__(self):
        super(DeleteItemFromMenuWindow, self).__init__()
        uic.loadUi('deleteitemfrommenu.ui', self)

        self.deleteButton = self.findChild(QtWidgets.QPushButton, 'DeleteItem')
        self.itemIDLineEdit = self.findChild(QtWidgets.QComboBox, 'ItemID')  
        self.CafeNameLineEdit = self.findChild(QtWidgets.QComboBox, 'CafeName')  
        
        self.CafeNameLineEdit.currentIndexChanged.connect(self.onCafeChange)
        
        self.deleteButton.clicked.connect(self.deleteMenuItem)
        
        self.populateMenu(self.CafeNameLineEdit.currentText())
        
    def onCafeChange(self):
        self.itemIDLineEdit.clear()

        
        selectedOption = self.CafeNameLineEdit.currentText()
        self.populateMenu(selectedOption)
        
    def populateMenu(self,selectedOption):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT ItemID,ItemName FROM Menu Where CafeName=?"  
            cursor.execute(query,selectedOption)
            ingredients = cursor.fetchall()
            # self.itemIDLineEdit.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
            self.itemNametoID = dict()
            for ingredient in ingredients:
                self.itemIDLineEdit.addItem(ingredient[1])
                self.itemNametoID[ingredient[1]] = ingredient[0]

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load ingredients: {e}')
        finally:
            connection.close()
        
    # def loadItems(self):
    #     try:
    #         connection = pyodbc.connect(connection_string)
    #         cursor = connection.cursor()

    #         query = "SELECT ItemID,ItemName FROM Menu Where CafeName='Tapal Cafeteria'"  
    #         cursor.execute(query)
    #         ingredients = cursor.fetchall()
    #         # self.itemIDLineEdit.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
    #         self.itemNametoID = dict()
    #         for ingredient in ingredients:
    #             self.itemIDLineEdit.addItem(ingredient[1])
    #             self.itemNametoID[ingredient[1]] = ingredient[0]

    #     except Exception as e:
    #         QMessageBox.warning(self, 'Error', f'Failed to load ingredients: {e}')
    #     finally:
    #         connection.close()

    def deleteMenuItem(self):
        itemID = self.itemIDLineEdit.currentText()
        cafeName = self.CafeNameLineEdit.currentText()

        if not itemID or not cafeName:
            QMessageBox.warning(self, 'Error', 'Item ID or Cafe Name not entered')
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Check if the specified CafeName sells the item with the given ItemID
            check_cafe_query = "SELECT COUNT(*) FROM Menu WHERE ItemID = ? AND CafeName = ?"
            cursor.execute(check_cafe_query, self.itemNametoID[itemID], cafeName)
            if cursor.fetchone()[0] == 0:
                QMessageBox.warning(self, 'Error', 'The specified cafe does not sell this item!')
                return

            # Proceed with deletion since the item and cafe match exists
            delete_menu_query = "DELETE FROM Menu WHERE ItemID = ? AND CafeName = ?"
            cursor.execute(delete_menu_query, self.itemNametoID[itemID], cafeName)

            connection.commit()
            QMessageBox.information(self, 'Success', 'Item deleted successfully from the menu')

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete item: {e}')
        finally:
            connection.close()
        

# Class for "View Inventory" Window
class ViewInventoryWindow(QMainWindow):
    def __init__(self):
        super(ViewInventoryWindow, self).__init__()
        uic.loadUi('viewinventory.ui', self)

        
        self.inventoryTable = self.findChild(QtWidgets.QTableWidget, 'InventoryTable')  

        
        self.loadInventoryData()

    def loadInventoryData(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # SQL query to get data from Ingredients table
            query = "SELECT IngredientName, CostPerUnit, Quantity FROM Ingredients"
            cursor.execute(query)
            results = cursor.fetchall()

            
            self.populateInventoryTable(results)

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load inventory data: {e}')
        finally:
            connection.close()

    def populateInventoryTable(self, inventoryItems):
        self.inventoryTable.setRowCount(len(inventoryItems))

        for i, item in enumerate(inventoryItems):
            self.inventoryTable.setItem(i, 0, QtWidgets.QTableWidgetItem(item[0]))  # Ingredient Name
            self.inventoryTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Price
            self.inventoryTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Stock


# Class for "Manage Inventory" Window
class ManageInventoryWindow(QMainWindow):
    def __init__(self):
        super(ManageInventoryWindow, self).__init__()
        uic.loadUi('updateinventory.ui', self)

        
        self.updateButton = self.findChild(QtWidgets.QPushButton, 'Update')
        self.ingredientIDLineEdit = self.findChild(QtWidgets.QComboBox, 'IngredientID')
        self.newPriceLineEdit = self.findChild(QtWidgets.QLineEdit, 'NewPrice')
        self.newQuantityLineEdit = self.findChild(QtWidgets.QLineEdit, 'NewQuantity')
        
        self.loadIngredients()

        
        self.updateButton.clicked.connect(self.updateInventory)
        
    def loadIngredients(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT IngredientName FROM Ingredients"  
            cursor.execute(query)
            ingredients = cursor.fetchall()

            for ingredient in ingredients:
                self.ingredientIDLineEdit.addItem(ingredient[0])  # Add each ingredient name to the combo box

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load ingredients: {e}')
        finally:
            connection.close()

    def updateInventory(self):
        ingredientID = self.ingredientIDLineEdit.currentText()
        newPrice = self.newPriceLineEdit.text()
        newQuantity = self.newQuantityLineEdit.text()           

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Update Ingredients table with new values
            if not newPrice and not newQuantity:
                QMessageBox.warning(self, 'Error', f'Enter atleast one value!')
            elif not newPrice and newQuantity:
                update_query = "UPDATE Ingredients SET Quantity = ? WHERE IngredientName = ?"
                cursor.execute(update_query, newQuantity, ingredientID)
                QMessageBox.information(self, 'Success', 'Inventory updated successfully')
            elif newQuantity and not newPrice:
                update_query = "UPDATE Ingredients SET CostPerUnit = ? WHERE IngredientName = ?"
                cursor.execute(update_query,newPrice, ingredientID)
                QMessageBox.information(self, 'Success', 'Inventory updated successfully')
            else:
                update_query = "UPDATE Ingredients SET CostPerUnit = ?, Quantity = ? WHERE IngredientName = ?"
                cursor.execute(update_query,newPrice, newQuantity, ingredientID)
                QMessageBox.information(self, 'Success', 'Inventory updated successfully')

            connection.commit()
            

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to update inventory: {e}')
        finally:
            connection.close()


# Class for "View Orders" Window
class ViewOrdersWindow(QMainWindow):
    def __init__(self):
        super(ViewOrdersWindow, self).__init__()
        uic.loadUi('vieworder.ui', self)

        self.ordersTable = self.findChild(QtWidgets.QTableWidget, 'Orders')
        self.customerOrdersTable = self.findChild(QtWidgets.QTableWidget, 'CustomerOrders')
        self.orderItemsTable = self.findChild(QtWidgets.QTableWidget, 'OrderItems')
        self.cafeOrdersTable = self.findChild(QtWidgets.QTableWidget, 'CafeOrders')

        self.populateOrdersTable()
        self.populateCustomerOrdersTable()
        self.populateOrderItemsTable()
        self.populateCafeOrdersTable()

    def populateOrdersTable(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT OrderID, TimeOfOrder, OrderStatus, OrderBill FROM Orders")
            orders = cursor.fetchall()
            self.populateTable(self.ordersTable, orders)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load Orders: {e}')
        finally:
            connection.close()

    def populateCustomerOrdersTable(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT co.OrderID, co.CustomerID, c.CustomerName, co.Feedback, co.Instructions FROM CustomerOrders co inner join Customers c on co.CustomerID=c.CustomerID")
            customer_orders = cursor.fetchall()
            self.populateTable(self.customerOrdersTable, customer_orders)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load Customer Orders: {e}')
        finally:
            connection.close()

    def populateOrderItemsTable(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT oi.ItemID, i.ItemName, oi.OrderID,  oi.OrderedQuantity, oi.Price FROM OrderItems oi inner join Items i on oi.ItemID=i.ItemID")
            order_items = cursor.fetchall()
            self.populateTable(self.orderItemsTable, order_items)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load Order Items: {e}')
        finally:
            connection.close()

    def populateCafeOrdersTable(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("""SELECT c.CafeName, co.OrderID 
                              FROM CafeOrders co 
                              JOIN Cafes c ON co.CafeID = c.CafeID""")
            cafe_orders = cursor.fetchall()
            self.populateTable(self.cafeOrdersTable, cafe_orders)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load Cafe Orders: {e}')
        finally:
            connection.close()

    def populateTable(self, tableWidget, data):
        tableWidget.setRowCount(len(data))
        for rowIdx, rowData in enumerate(data):
            for colIdx, colData in enumerate(rowData):
                tableWidget.setItem(rowIdx, colIdx, QtWidgets.QTableWidgetItem(str(colData)))


class CustomerHome(QMainWindow):
    def __init__(self):
        super(CustomerHome, self).__init__()
        uic.loadUi('Cafeteria Menu Form.ui', self)

        
        self.radioTapal = self.findChild(QtWidgets.QRadioButton, 'TapalCafeteria')
        self.radioCafe2Go = self.findChild(QtWidgets.QRadioButton, 'Cafe2Go')
        self.selectButton = self.findChild(QtWidgets.QPushButton, 'SelectCafeteria')
        
        
        self.selectButton.clicked.connect(self.displayMenu)
        
        self.goToCartButton = self.findChild(QtWidgets.QPushButton, 'GoToCart')
        self.myOrdersButton = self.findChild(QtWidgets.QPushButton, 'MyOrders')
        
        self.ViewItemButton = self.findChild(QtWidgets.QPushButton, 'ViewItem')


        self.goToCartButton.clicked.connect(self.openCartForm)
        self.myOrdersButton.clicked.connect(self.openOrderTrackingForm)
        self.ViewItemButton.clicked.connect(self.openViewItemForm)

        #Connect double-click event of the list widget
        #self.menuTable.itemDoubleClicked.connect(self.openViewItemForm)

    def displayMenu(self):
        selectedCafe = 'Tapal Cafeteria' if self.radioTapal.isChecked() else 'Cafe2Go' if self.radioCafe2Go.isChecked() else None
        if not selectedCafe:
            QMessageBox.warning(self, 'Error', 'No Cafeteria selected')
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = """
            SELECT ItemName, CafeName, Price
            FROM Menu 
            WHERE CafeName = ?
            """
            cursor.execute(query, selectedCafe)
            results = cursor.fetchall()

            # Populate the Menu table widget
            self.populateMenuTable(results)

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Database query failed: {e}')
        finally:
            connection.close()

    def populateMenuTable(self, menuItems):
        self.menuTable = self.findChild(QtWidgets.QTableWidget, 'Menu')
        self.menuTable.setRowCount(len(menuItems))

        for i, item in enumerate(menuItems):
            self.menuTable.setItem(i, 0, QtWidgets.QTableWidgetItem(item[0]))  # Item Name
            self.menuTable.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))  # Cafeteria
            self.menuTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Price
    
    def openCartForm(self):
        self.cartForm = CartForm()  
        self.cartForm.show()

    def openOrderTrackingForm(self):
        self.orderTrackingForm = OrderTrackingForm()  
        self.orderTrackingForm.show()

    def openViewItemForm(self, item):
        self.viewItemForm = ViewItemForm()  
        self.viewItemForm.show()
        
            
class OrderTrackingForm(QMainWindow):
    def __init__(self):
        super(OrderTrackingForm, self).__init__()
        uic.loadUi('Order Tracking Form.ui', self)

        self.ordersTableWidget = self.findChild(QtWidgets.QTableWidget, 'Orders')
        self.feedbackButton = self.findChild(QtWidgets.QPushButton, 'Feedback')
        
        self.populateOrdersTable()

    def populateOrdersTable(self):
        global current_customer_id

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # SQL query to fetch OrderID, TotalBill, and Status for the current customer
            query = """SELECT co.OrderID, o.OrderBill, o.OrderStatus
                       FROM CustomerOrders co 
                       JOIN Orders o ON co.OrderID = o.OrderID 
                       WHERE co.CustomerID = ?"""
            cursor.execute(query, current_customer_id)
            orders = cursor.fetchall()

            # Setting up the table widget
            self.ordersTableWidget.setRowCount(len(orders))
            self.ordersTableWidget.setColumnCount(3)  
            self.ordersTableWidget.setHorizontalHeaderLabels(['OrderID', 'TotalBill', 'Status'])

            for row_number, row_data in enumerate(orders):
                for column_number, data in enumerate(row_data):
                    self.ordersTableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load orders: {e}')
        finally:
            connection.close()


class CartForm(QMainWindow):
    def __init__(self):
        super(CartForm, self).__init__()
        uic.loadUi('Cart Form.ui', self)
        
        
        #self.cartListWidget = self.findChild(QtWidgets.QListWidget, 'CartList')
        self.placeOrderButton = self.findChild(QtWidgets.QPushButton, 'PlaceOrder')
        self.clearCartButton = self.findChild(QtWidgets.QPushButton, 'ClearCart')
        self.totalBillLineEdit = self.findChild(QtWidgets.QLineEdit, 'TotalBill')
        self.orderInstructionsTextEdit = self.findChild(QtWidgets.QTextEdit, 'OrderInstructions')
        
        self.cartTableWidget = self.findChild(QtWidgets.QTableWidget, 'CartTable')
        self.initializeCartTable()
        self.populateCartTable()
        
        
        self.totalBillLineEdit.setReadOnly(True)  
        self.placeOrderButton.clicked.connect(self.placeOrder)
        self.clearCartButton.clicked.connect(self.clearCart)
        
        #self.populateCartList()

    # def populateCartList(self):
    #     global cart_items
    #     for item in cart_items:
    #         item_str = f"{item['item']} from {item['cafe']} - Quantity: {item['quantity']}, Total: {item['total']}"
    #         self.cartListWidget.addItem(item_str)
    #     
    

    def updateTotalBill(self):
        global cart_items
        total_bill = sum(item['total'] for item in cart_items)
        self.totalBillLineEdit.setText(str(total_bill))
        
        
        

    
    def initializeCartTable(self):
        
        column_headers = ["Item", "Cafe", "Price", "Quantity", "Total"]
        self.cartTableWidget.setColumnCount(len(column_headers))
        self.cartTableWidget.setHorizontalHeaderLabels(column_headers)

        

    def populateCartTable(self):
        global cart_items
        self.cartTableWidget.setRowCount(0)  # Clear existing rows

        for item in cart_items:
            row_position = self.cartTableWidget.rowCount()
            self.cartTableWidget.insertRow(row_position)  # Insert a new row

            
            self.cartTableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(item['item']))
            self.cartTableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item['cafe']))
            self.cartTableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(item['price'])))
            self.cartTableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(item['quantity'])))
            self.cartTableWidget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(item['total'])))
            
        self.updateTotalBill()
        
    def clearCart(self):
        global cart_items
        cart_items.clear()
        self.updateTotalBill()
        self.populateCartTable()
        self.orderInstructionsTextEdit.clear()
        
    def placeOrder(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Generate OrderID
            new_order_id = self.generate_order_id(cursor)
            
            global current_customer_id
            
            # Get Order details
            order_instructions = self.orderInstructionsTextEdit.toPlainText()
            order_bill = self.totalBillLineEdit.text()
            customer_id = current_customer_id  
            
            # Insert into Orders table
            cursor.execute("INSERT INTO Orders (OrderID, TimeOfOrder, OrderStatus, OrderBill) VALUES (?, GETDATE(), ?, ?)", 
                           new_order_id, 'Placed', order_bill)

            # Insert into CustomerOrders table
            cursor.execute("INSERT INTO CustomerOrders (CustomerID,OrderID, Feedback, Instructions) VALUES (?, ?, ?, ?)",
                           current_customer_id,new_order_id,'', order_instructions)

            # Assuming cart_items contain items from only one cafe
            cafe_name = cart_items[0]['cafe']
            if cafe_name == 'Tapal Cafeteria':
                cafe_id = 1
            else:
                cafe_id = 2

            # Insert into CafeOrders table
            cursor.execute("INSERT INTO CafeOrders (CafeID, OrderID) VALUES (?, ?)",
                           cafe_id, new_order_id)

            # Insert into OrderItems table
            for item in cart_items:
                item_id = self.fetch_item_id(cursor, item['item'])  
                cursor.execute("INSERT INTO OrderItems (ItemID, OrderID, OrderedQuantity, Price) VALUES (?, ?, ?, ?)",
                               item_id, new_order_id, item['quantity'], item['price'])

            # Commit transaction
            connection.commit()

            QMessageBox.information(self, 'Order Placed', f'Your order, ID: {new_order_id} has been placed successfully.')
            
            

        except Exception as e:
            connection.rollback()  # Rollback in case of error
            QMessageBox.warning(self, 'Error', f'Failed to place order: {e}')

        finally:
            cart_items.clear()
            self.updateTotalBill()
            self.populateCartTable()
            self.orderInstructionsTextEdit.clear()
            connection.close()
            # clear the cart after placing the order
            

    def generate_order_id(self, cursor):
        cursor.execute("SELECT MAX(OrderID) FROM Orders")
        last_order_id = cursor.fetchone()[0]

        if last_order_id:
            new_order_id = f"{int(last_order_id) + 1:05}"
        else:
            new_order_id = "00001"

        return new_order_id
    
    def fetch_item_id(self, cursor, item_name):
        cursor.execute("SELECT ItemID FROM Items WHERE ItemName = ?", item_name)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None  
    
    
class Recipe(QMainWindow):
    def __init__(self,id):
        super(Recipe, self).__init__()
        uic.loadUi('Recipes.ui', self)
        
        self.ItemID = id[0]
        self.ItemName = self.findChild(QtWidgets.QLineEdit, 'ItemName')
        self.ItemIngredients = self.findChild(QtWidgets.QListWidget, 'IngredientsList')
        self.ItemName.setDisabled(True)
        
        self.populateRecipe()
        
    def populateRecipe(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT ItemName FROM Items Where ItemID = ?"
            cursor.execute(query,self.ItemID)
            name = cursor.fetchone()
            
            if name:
                self.ItemName.setText(str(name[0]))

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load cafes: {e}')
        finally:
            connection.close()
            
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "Select IngredientName from Recipes r inner join Ingredients i on i.IngredientID=r.IngredientID where ItemID = ?"
            cursor.execute(query,self.ItemID)
            ings = cursor.fetchall()
            
            if ings:
                for ing in ings:
                    self.ItemIngredients.addItem(str(ing[0]))

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load cafes: {e}')
        finally:
            connection.close()
    
     
class ViewItemForm(QMainWindow):
    def __init__(self):
        super(ViewItemForm, self).__init__()
        uic.loadUi('View Item Form.ui', self)

        
        self.cafeSelector = self.findChild(QtWidgets.QComboBox, 'CafeSelector')
        self.itemSelector = self.findChild(QtWidgets.QComboBox, 'ItemSelector')
        self.itemPriceLineEdit = self.findChild(QtWidgets.QLineEdit, 'ItemPrice')
        self.itemDescriptionLineEdit = self.findChild(QtWidgets.QLineEdit, 'ItemDescription')
        self.itemQuantitySpinBox = self.findChild(QtWidgets.QSpinBox, 'ItemQuantity')
        self.backToMenuButton = self.findChild(QtWidgets.QPushButton, 'BackToMenu')
        self.itemRecipeButton = self.findChild(QtWidgets.QPushButton, 'ItemRecipe')
        self.addToCartButton = self.findChild(QtWidgets.QPushButton, 'AddToCart')

        self.itemPriceLineEdit.setDisabled(True)
        self.itemDescriptionLineEdit.setDisabled(True)
        self.itemQuantitySpinBox.setValue(1)

        
        self.itemRecipeButton.clicked.connect(self.showRecipe)
        self.backToMenuButton.clicked.connect(self.goBackToMenu)
        self.addToCartButton.clicked.connect(self.addToCart)

        
        self.populateCafeSelector()
        self.loadItemDetails()
        self.updateItemPrice()
        self.updateItemDescription()
        # Load item details when cafe selector changes
        self.cafeSelector.currentIndexChanged.connect(self.loadItemDetails)
    
        # Update item price when item selector changes
        self.itemSelector.currentIndexChanged.connect(self.updateItemPrice)
        self.itemSelector.currentIndexChanged.connect(self.updateItemDescription)


    def populateCafeSelector(self):
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT DISTINCT CafeName FROM Menu"
            cursor.execute(query)
            cafes = cursor.fetchall()

            for cafe in cafes:
                self.cafeSelector.addItem(cafe[0])

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load cafes: {e}')
        finally:
            connection.close()

    def loadItemDetails(self):
        selectedCafe = self.cafeSelector.currentText()
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT ItemName, Price FROM Menu WHERE CafeName = ?"
            cursor.execute(query, selectedCafe)
            items = cursor.fetchall()

            # Clear previous items and set the new ones
            self.itemSelector.clear()
            for item in items:
                self.itemSelector.addItem(item[0])
            

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load items: {e}')
        finally:
            connection.close()

    def goBackToMenu(self):
        # Close the current window and return to the Cafeteria Menu Form
        self.close()
        
    def updateItemPrice(self):
        selectedCafe = self.cafeSelector.currentText()
        selectedItem = self.itemSelector.currentText()

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT Price FROM Menu WHERE CafeName = ? AND ItemName = ?"
            cursor.execute(query, selectedCafe, selectedItem)
            price = cursor.fetchone()

            if price:
                self.itemPriceLineEdit.setText(str(price[0]))
            else:
                self.itemPriceLineEdit.clear()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load item price: {e}')
        finally:
            connection.close()
            
    def updateItemDescription(self):
        selectedCafe = self.cafeSelector.currentText()
        selectedItem = self.itemSelector.currentText()

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT ItemDescription FROM Items WHERE ItemName = ?"
            cursor.execute(query,selectedItem)
            description = cursor.fetchone()

            if description:
                self.itemDescriptionLineEdit.setText(str(description[0]))
            else:
                self.itemDescriptionLineEdit.clear()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load item description: {e}')
        finally:
            connection.close()
        
    def showRecipe(self):
        selectedCafe = self.cafeSelector.currentText()
        selectedItem = self.itemSelector.currentText()
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            query = "SELECT ItemID FROM Menu WHERE CafeName = ? AND ItemName = ?"
            cursor.execute(query, selectedCafe, selectedItem)
            ID = cursor.fetchone()

            if ID:
                self.IDtoRecipe = ID

        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Failed to load item ID')
        finally:
            connection.close()
        
        self.showRecipeUI = Recipe(self.IDtoRecipe)
        self.showRecipeUI.show()
                
    def addToCart(self):
        # Get selected item details
        selectedCafe = self.cafeSelector.currentText()
        selectedItem = self.itemSelector.currentText()
        selectedPrice = self.itemPriceLineEdit.text()
        selectedQuantity = self.itemQuantitySpinBox.value()

        if cart_items and cart_items[0]['cafe'] != selectedCafe:
            QMessageBox.warning(self, 'Different Cafe', 'Your cart contains items from a different cafe. Please complete your current order or clear your cart before adding items from another cafe.')
            return

        # Check if the item already exists in the cart
        existing_item = next((item for item in cart_items if item['item'] == selectedItem and item['cafe'] == selectedCafe), None)

        if existing_item:
            # Update the quantity of the existing item
            existing_item['quantity'] += selectedQuantity
            existing_item['total'] = int(existing_item['price']) * existing_item['quantity']
            QMessageBox.information(self, 'Item Quantity Updated', 'Item already in cart, current quantity increased.')
        else:
            # Add a new item to the cart
            cart_items.append({
                'cafe': selectedCafe,
                'item': selectedItem,
                'price': selectedPrice,
                'quantity': selectedQuantity,
                'total': int(selectedPrice) * selectedQuantity
            })
            QMessageBox.information(self, 'Item Added to Cart', f"Selected Item: {selectedItem}\nPrice: {selectedPrice}\nQuantity: {selectedQuantity}\nTotal: {int(selectedPrice) * selectedQuantity}")
        

def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()