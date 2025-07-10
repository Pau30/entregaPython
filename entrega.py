#Importacion de modulos
import sqlite3
from colorama import Fore, Back, Style, init


#inicializacion de colorama
init(autoreset=True)

#Conexion a la base de datos    
def inicializar_base_datos():
    """Crea la base de datos y la tabla si no existen."""
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS inventario ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nombre TEXT NOT NULL, 
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        ) 
    ''')

    conexion.commit()
    conexion.close()
    print(Fore.GREEN + "Base de datos creada con éxito.")

# Usuario y contraseña de acceso (pueden ser modificados)
user = "admin"
password = "1234"

#Funcion para agregar un producto al inventario
def agregar_producto():
    """Solicita los datos de un producto, los valida y los agrega al inventario."""
    while True: #Bucle para confirmar si el usuario eligio la opcion correcta en el menu
        confirmacion = input(Fore.YELLOW + "¿Deseás ingresar un producto? (si/no): " + Style.RESET_ALL).strip().lower()
        if confirmacion == "si":
            break  # continúa con la función
        elif confirmacion == "no":
            print(Fore.CYAN + "Operación cancelada. Volviendo al menú principal.")
            return  # vuelve al menú principal
        else:
            print(Fore.RED + "Por favor escribí 'si' o 'no' para continuar.")
    #Conexion a la base de datos
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    print(Fore.MAGENTA + "Registrar nuevo producto")
    #---- Nombre ----
    while True:
        nombre = input("Nombre del producto: ")
        if not nombre.strip(): #Validación para que no este vacío
            print(Fore.RED + "¡Error! El nombre del producto no puede estar vacío.") 
        elif nombre.isdigit():#Validación para que no sea un número
            print(Fore.RED + "¡Error! El nombre del producto no puede ser un número.") 
        else:
            break  # Salir del bucle si es válido

    #---- Descripcion ----
    while True:
        descripcion = input("Descripción del producto: ")
        if not descripcion.strip():
            print(Fore.RED + "¡Error! La descripción del producto no puede estar vacía.")
        elif descripcion.isdigit():#Validación para que no sea un número
            print(Fore.RED + "¡Error! La descripcion del producto no puede ser un número.") 
        else:
            break

    #---- Cantidad ----
    while True:
        cantidad_str = input("Cantidad del producto: ")
        if not cantidad_str.strip():  # Validación para que no este vacío
            print(Fore.RED + "¡Error! La cantidad del producto no puede estar vacía.")
        elif not cantidad_str.isdigit():  # Validación para que sea un número entero positivo
            print(Fore.RED + "¡Error! La cantidad del producto debe ser un número entero positivo.")
        else:
            cantidad = int(cantidad_str)  # Convertir a entero después de la validación
            break  # Salir del bucle si es válido

   #---- Precio ----
    while True:
        precio_str = input("Precio del producto: ")
        if not precio_str.strip(): #Validación para que no este vacío
            print(Fore.RED + "¡Error! El precio del producto no puede estar vacío.") 
            continue # Si el precio esta vacío, vuelve a pedirlo
        try: #Se usa un try-except para manejar errores de conversión ya que el precio puede ser un número decimal 
            precio = float(precio_str)
            if precio <= 0: #Validación para que sea un número positivo
                print(Fore.RED + "¡Error! El precio del producto debe ser un número positivo.")
                continue # Si el valor no es válido, vuelve a pedirlo
            break  # Salir del bucle si es válido
        except ValueError: #Si el valor ingresado tiene un error de conversion el bucle vuelve a pedir el precio hasta que sea válido
            print(Fore.RED + "¡Error! El precio del producto debe ser un número válido (usar punto para decimales, no coma).")
            
      
    #---- Categoria ----
    while True:
        categoria = input("Categoría del producto: ")
        if not categoria.strip(): #Validación para que no este vacío
            print(Fore.RED + "¡Error! La categoría del producto no puede estar vacía.")                     
        else:
            break  # Salir del bucle si es válido

    #Insertar los datos en la base de datos
    try:
        cursor.execute('''
            INSERT INTO inventario (nombre, descripcion, cantidad, precio, categoria) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))

        #Confirmar los cambios
        conexion.commit()
        print(Fore.GREEN + "Producto agregado exitosamente al inventario.")

    except sqlite3.IntegrityError:
        print(Fore.RED + "Error: El producto ya existe en el inventario.")
    
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al agregar el producto: {e}")

    finally:
        #Cerrar la conexion a la base de datos
        conexion.close()

#Funcion para mostrar los productos del inventario
def mostrar_productos():
    """Muestra todos los productos del inventario."""
    #Conexion a la base de datos
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    
    try: #traer todos los productos de la base de datos
        cursor.execute('SELECT * FROM inventario')
        productos = cursor.fetchall()

        if not productos: #Validación para que no este vacío
            print(Fore.YELLOW + "El inventario está vacío.")
            return

        print(Fore.CYAN + "Productos en el inventario:") #Mostrar los productos
        for producto in productos:
            print("-" * 50)
            print(Fore.BLUE + "ID: " + Fore.RESET + f"{producto[0]}")
            print(Fore.BLUE + "Nombre: " + Fore.RESET + f"{producto[1]}")
            print(Fore.BLUE + "Descripción: " + Fore.RESET + f"{producto[2]}")
            print(Fore.BLUE + "Cantidad: " + Fore.RESET + f"{producto[3]}")
            print(Fore.BLUE + "Precio: " + Fore.RESET + f"${producto[4]:.2f}")
            print(Fore.BLUE + "Categoría: " + Fore.RESET + f"{producto[5]}")
            print("-" * 50)

    except sqlite3.Error as e: #Si ocurre un error al mostrar los productos
        print(Fore.RED + f"Error al mostrar los productos: {e}")

    finally: 
        #Cerrar la conexion a la base de datos
        conexion.close()

#Funcion para actualizar un producto del inventario por ID
def actualizar_producto():
    """Actualiza un producto en el inventario por su ID."""
    while True: #Bucle para confirmar si el usuario eligio la opcion correcta en el menu
        confirmacion = input(Fore.YELLOW + "¿Deseás modificar un producto? (si/no): " + Style.RESET_ALL).strip().lower()
        if confirmacion == "si":
            break  # continúa con la función
        elif confirmacion == "no":
            print(Fore.CYAN + "Operación cancelada. Volviendo al menú principal.")
            return  # vuelve al menú principal
        else:
            print(Fore.RED + "Por favor escribí 'si' o 'no' para continuar.")
    #Conexion a la base de datos
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    
    mostrar_productos()  # Mostrar productos antes de actualizar
        # Bucle para pedir ID válido
    while True:
        id_producto = input("Ingrese el ID del producto a actualizar: ").strip() #Pedir ID del producto y verificar que no este vacío
        if not id_producto:
            print(Fore.RED + "¡Error! El ID del producto no puede estar vacío.")
            continue # Si el ID esta vacío, vuelve a pedirlo
        if not id_producto.isdigit(): # Verifica si el ID es un número entero positivo
            print(Fore.RED + "¡Error! El ID debe ser un número entero.")
            continue # Si el ID no es un número, vuelve a pedirlo
        id_producto = int(id_producto) # Convertir a entero después de la validación

        # Verificar que el producto exista
        cursor.execute('SELECT * FROM inventario WHERE id = ?', (id_producto,)) #Selecciona el producto por ID
        producto = cursor.fetchone() 
        if not producto: # Si no se encuentra el producto, muestra un mensaje de error
            print(Fore.RED + "¡Error! Producto no encontrado.")
            continue # Si el ID no es válido, vuelve a pedirlo
        break #Sale del bucle si el ID es válido y el producto existe

    print(Fore.MAGENTA + f"Actualizando producto: {producto[1]}")
    actualizado = False  # Inicializar variable para verificar si se actualizó algo

    # Recolección de datos para actualizar
    try:
        #---- Nombre-----
        while True: #se usa un bucle en caso de que el usuario quiera cambiar el nombre pero ingrese un valor no válido
            nuevo_nombre = input("Nuevo nombre del producto " + Fore.YELLOW + "(dejar en blanco para no cambiar): " + Style.RESET_ALL)
            if not nuevo_nombre.strip(): # Verifica si el nuevo nombre esta vacío
                break  # Si esta vacío, no se actualiza el nombre y se sale del bucle
            elif nuevo_nombre.isdigit(): #Verifica si el nuevo nombre es un número
                print(Fore.RED + "¡Error! El nombre no puede ser solo números.")
                continue #Si el valor no es válido, se vuelve a pedir
            else:
                cursor.execute('UPDATE inventario SET nombre = ? WHERE id = ?', (nuevo_nombre, id_producto)) # Si es válido, actualiza el nombre
                actualizado = True # La variable actualizado se pone en True si se actualiza algo
                break # Sale del bucle

        #---- Descripcion ----
        while True:
            nueva_descripcion = input("Nueva descripción del producto " + Fore.YELLOW + "(dejar en blanco para no cambiar): " + Style.RESET_ALL) # Verifica si la nueva descripción esta vacía
            if not nueva_descripcion.strip():
                break  # No se quiere modificar
            elif nueva_descripcion.isdigit(): # Verifica si la nueva descripción es un número
                print(Fore.RED + "¡Error! La descripción no puede ser solo números.")
                continue # Si el valor no es válido, se vuelve a pedir
            else: # Si es válido, actualiza la descripción
                cursor.execute('UPDATE inventario SET descripcion = ? WHERE id = ?', (nueva_descripcion, id_producto))
                actualizado = True # La variable actualizado se pone en True si se actualiza algo
                break # Sale del bucle

        #---- Cantidad ----
        while True: #Se usa un bucle en caso de que el usuario quiera cambiar la candidad pero ingrese un valor no válido
            nueva_cantidad_str = input("Nueva cantidad del producto" + Fore.YELLOW + "(dejar en blanco para no cambiar): " + Style.RESET_ALL)
            if not nueva_cantidad_str.strip(): #Verifica si la nueva cantidad esta vacía 
                break  # Si esta vacía, no se actualiza la cantidad y se sale del bucle

            if not nueva_cantidad_str.isdigit(): # Verifica si la nueva cantidad es un número entero positivo
                print(Fore.RED + "¡Error! La cantidad debe ser un número entero positivo.")
                continue  # Si el valor no es válido, se vuelve a pedir

            nueva_cantidad = int(nueva_cantidad_str) # Convertir a entero después de la validación
            cursor.execute('UPDATE inventario SET cantidad = ? WHERE id = ?', (nueva_cantidad, id_producto)) # Si es válido, actualiza la cantidad
            actualizado = True # La variable actualizado se pone en True si se actualiza algo
            break

        #---- Precio ----
        while True: # Se usa un bucle en caso de que el usuario quiera cambiar el precio pero ingrese un valor no válido
            nuevo_precio_str = input("Nuevo precio del producto" + Fore.YELLOW + "(dejar en blanco para no cambiar): " + Style.RESET_ALL)
            if not nuevo_precio_str.strip(): # Verifica si el nuevo precio esta vacío
                break # Si esta vacío, no se actualiza el precio y se sale del bucle

            try: #Se usa un try-except para manejar errores de conversión ya que el precio puede ser un número decimal 
                nuevo_precio = float(nuevo_precio_str)
                if nuevo_precio <= 0:# Verifica si el nuevo precio es un número positivo
                    print(Fore.RED + "¡Error! El precio debe ser un número positivo.")
                    continue  # Si el valor no es válido, se vuelve a pedir
                cursor.execute('UPDATE inventario SET precio = ? WHERE id = ?', (nuevo_precio, id_producto)) # Si es válido, actualiza el precio
                actualizado = True # La variable actualizado se pone en True si se actualiza algo
                break # Sale del bucle
            except ValueError: #Si el valor ingresado tiene un error de conversion el bucle vuelve a pedir el precio hasta que sea válido
                print(Fore.RED + "¡Error! El precio debe ser un número válido (usar punto para decimales, no coma).")

        #---- Categoria ----
        while True:
            nueva_categoria = input("Nueva categoría del producto " + Fore.YELLOW + "(dejar en blanco para no cambiar): " + Style.RESET_ALL)
            if not nueva_categoria.strip(): # Verifica si la nueva categoría esta vacía
                break  # Si esta vacía, no se actualiza la categoría y se sale del
                
            cursor.execute('UPDATE inventario SET categoria = ? WHERE id = ?', (nueva_categoria.strip(), id_producto)) # Si es válido, actualiza la categoría
            actualizado = True # La variable actualizado se pone en True si se actualiza algo
            break # Sale del bucle
    
        if actualizado: # Si se actualizó al menos un campo
            conexion.commit()
            print(Fore.GREEN + "Producto actualizado exitosamente.")
        else: # Si no se actualizó nada
            print(Fore.YELLOW + "No se realizó ninguna modificación.")
    
    except sqlite3.Error as e: # Si ocurre un error al actualizar el producto
        print(Fore.RED + f"Error al actualizar el producto: {e}")
    
    finally:
        conexion.close() # Cerrar la conexión a la base de datos

#Funcion para eliminar un producto del inventario por ID
def eliminar_producto():    
    """Elimina un producto del inventario por su ID."""
    while True: #Bucle para confirmar si el usuario eligio la opcion correcta en el menu
        confirmacion = input(Fore.YELLOW + "¿Deseás eliminar un producto? (si/no): " + Style.RESET_ALL).strip().lower()
        if confirmacion == "si":
            break  # continúa con la función
        elif confirmacion == "no":
            print(Fore.CYAN + "Operación cancelada. Volviendo al menú principal.")
            return  # vuelve al menú principal
        else:
            print(Fore.RED + "Por favor escribí 'si' o 'no' para continuar.")
    #Conexion a la base de datos
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    mostrar_productos()  # Mostrar productos antes de eliminar
    while True:  # Bucle para pedir ID válido
        id_producto = input(Fore.YELLOW + "Ingrese el ID del producto a eliminar: " + Style.RESET_ALL).strip() #Pedir ID del producto y verificar que no este vacío
        if not id_producto:
            print(Fore.RED + "¡Error! El ID del producto no puede estar vacío.")
            continue # Si el ID esta vacío, vuelve a pedirlo
        if not id_producto.isdigit(): # Verifica si el ID es un número entero positivo
            print(Fore.RED + "¡Error! El ID debe ser un número entero.")
            continue # Si el ID no es un número, vuelve a pedirlo
        id_producto = int(id_producto) # Convertir a entero después de la validación

        # Verificar que el ID del producto exista
        cursor.execute('SELECT * FROM inventario WHERE id = ?', (id_producto,)) #Selecciona el producto por ID
        producto = cursor.fetchone()
        if not producto: # Si no se encuentra el producto, muestra un mensaje de error
            print(Fore.RED + "¡Error! Producto no encontrado.")
            continue # Si el ID no es válido, vuelve a pedirlo
        break  # Sale del bucle si el ID es válido y el producto existe

    # Confirmación del usuario antes de eliminar
    while True:
        confirmar = input(Fore.YELLOW + f"¿Estás seguro que querés eliminar el producto '{producto[1]}'? "+ "(si/no): " + Style.RESET_ALL).strip().lower()
        if confirmar == "si": # Si el usuario confirma la eliminación
            break  # continuar con eliminación
        elif confirmar == "no": # Si el usuario cancela la eliminación
            print(Fore.CYAN + "Operación cancelada. No se eliminó el producto.")
            conexion.close()
            return # Si se cancela, cerrar la conexión y salir de la función
        else: # Si el usuario ingresa un valor no válido
            print(Fore.RED + "Respuesta no válida. Por favor escribí 'si' o 'no'.")
    
    try: # Eliminar el producto de la base de datos
        cursor.execute('DELETE FROM inventario WHERE id = ?', (id_producto,))
        conexion.commit()
        print(Fore.GREEN + f"Producto '{producto[1]}' eliminado exitosamente.")

    except sqlite3.Error as e:  # Si ocurre un error al eliminar el producto
        print(Fore.RED + f"Error al eliminar el producto: {e}")

    finally:
        conexion.close()  # Cerrar la conexión a la base de datos
                    
#Funcion para buscar un producto por ID - Nombre - Categoria
def buscar_producto():

    """Permite buscar productos por ID, nombre o categoría."""
    while True: #Bucle para confirmar si el usuario eligio la opcion correcta en el menu
        confirmacion = input(Fore.YELLOW + "¿Deseás buscar un producto? (si/no): " + Style.RESET_ALL).strip().lower()
        if confirmacion == "si":
            break  # continúa con la función
        elif confirmacion == "no":
            print(Fore.CYAN + "Operación cancelada. Volviendo al menú principal.")
            return  # vuelve al menú principal
        else:
            print(Fore.RED + "Por favor escribí 'si' o 'no' para continuar.")
    #Conexion a la base de datos
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    print(Fore.MAGENTA + "Buscar producto")

    while True: # Bucle para seleccionar el tipo de búsqueda
        print("1. Buscar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por categoría")
        opcion = input(Fore.YELLOW + "Seleccione una opción (1-3): " + Style.RESET_ALL).strip()

        if opcion in {"1", "2", "3"}:
            break # Sale del bucle si la opción es válida
        else: # Si la opción no es válida, muestra un mensaje de error y vuelve a pedir la opción
            print(Fore.RED + "Opción no válida. Por favor, ingrese 1, 2 o 3.")

    try:
        #Buscar por ID
        if opcion == "1":
            id_producto = input("Ingrese el ID del producto: ").strip().lower() #Pedir ID del producto, verificar que no este vacío y convertirlo a minúsculas
            if not id_producto.isdigit(): # Verifica si el ID es un número entero positivo
                print(Fore.RED + "¡Error! El ID debe ser un número entero.")
                return # Si el ID no es un número, sale de la función
            cursor.execute("SELECT * FROM inventario WHERE id = ?", (int(id_producto),)) #Selecciona el producto por ID
            producto = cursor.fetchone()
            if producto:
                print(Fore.CYAN + "Producto encontrado:")
                print("-" * 50)
                print(Fore.BLUE + "ID: " + Fore.RESET + f"{producto[0]}")
                print(Fore.BLUE + "Nombre: " + Fore.RESET + f"{producto[1]}")
                print(Fore.BLUE + "Descripción: " + Fore.RESET + f"{producto[2]}")
                print(Fore.BLUE + "Cantidad: " + Fore.RESET + f"{producto[3]}")
                print(Fore.BLUE + "Precio: " + Fore.RESET + f"${producto[4]:.2f}")
                print(Fore.BLUE + "Categoría: " + Fore.RESET + f"{producto[5]}")
                print("-" * 50)
            else: # Si no se encuentra el producto, muestra un mensaje de error
                print(Fore.RED + "Producto no encontrado.")
        
        #Buscar por nombre
        elif opcion == "2": 
            nombre = input("Ingrese el nombre del producto: ").strip().lower() #Pedir nombre del producto, verificar que no este vacío y convertirlo a minúsculas
            cursor.execute("SELECT * FROM inventario WHERE nombre LIKE ?", (f"%{nombre}%",)) #Selecciona el producto por nombre
            productos = cursor.fetchall()
            if productos: # Si se encuentran productos, muestra sus detalles
                print(Fore.CYAN + "Resultados encontrados:")
                for producto in productos: # Itera sobre los productos encontrados
                    print("-" * 50)
                    print(Fore.BLUE + "ID: " + Fore.RESET + f"{producto[0]}")
                    print(Fore.BLUE + "Nombre: " + Fore.RESET + f"{producto[1]}")
                    print(Fore.BLUE + "Descripción: " + Fore.RESET + f"{producto[2]}")
                    print(Fore.BLUE + "Cantidad: " + Fore.RESET + f"{producto[3]}")
                    print(Fore.BLUE + "Precio: " + Fore.RESET + f"${producto[4]:.2f}")
                    print(Fore.BLUE + "Categoría: " + Fore.RESET + f"{producto[5]}")
                    print("-" * 50)
            else: # Si no se encuentran productos, muestra un mensaje de error
                print(Fore.RED + "No se encontraron productos con ese nombre.")
       
        #Buscar por categoria
        elif opcion == "3":
            categoria = input("Ingrese la categoría del producto: ").strip() #Pedir categoria del producto y verificar que no este vacío
            cursor.execute("SELECT * FROM inventario WHERE categoria LIKE ?", (f"%{categoria}%",))
            productos = cursor.fetchall()
            if productos: # Si se encuentran productos, muestra sus detalles
                print(Fore.CYAN + "Resultados encontrados:")
                for producto in productos: # Itera sobre los productos encontrados
                    print("-" * 50)
                    print(Fore.BLUE + "ID: " + Fore.RESET + f"{producto[0]}")
                    print(Fore.BLUE + "Nombre: " + Fore.RESET + f"{producto[1]}")
                    print(Fore.BLUE + "Descripción: " + Fore.RESET + f"{producto[2]}")
                    print(Fore.BLUE + "Cantidad: " + Fore.RESET + f"{producto[3]}")
                    print(Fore.BLUE + "Precio: " + Fore.RESET + f"${producto[4]:.2f}")
                    print(Fore.BLUE + "Categoría: " + Fore.RESET + f"{producto[5]}")
                    print("-" * 50)
            else: # Si no se encuentran productos, muestra un mensaje de error
                print(Fore.RED + "No se encontraron productos en esa categoría.")

    except sqlite3.Error as e:# Si ocurre un error al buscar el producto
        print(Fore.RED + f"Error en la base de datos: {e}")

    finally: # Cerrar la conexión a la base de datos
        conexion.close()

#Funcion para reportar bajo stock
def bajo_stock():
    """Muestra los productos con cantidad igual o inferior a un límite definido por el usuario."""
    while True: #Bucle para confirmar si el usuario eligio la opcion correcta en el menu
        confirmacion = input(Fore.YELLOW + "¿Deseás ver un reporte de bajo stock? (si/no): " + Style.RESET_ALL).strip().lower()
        if confirmacion == "si":
            break  # continúa con la función
        elif confirmacion == "no":
            print(Fore.CYAN + "Operación cancelada. Volviendo al menú principal.")
            return  # vuelve al menú principal
        else:
            print(Fore.RED + "Por favor escribí 'si' o 'no' para continuar.")
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    print(Fore.RED + "Reporte de productos con stock bajo")
    while True:
        limite = input(Fore.YELLOW + "Ingrese el límite de stock (número entero): " + Style.RESET_ALL).strip()
        if not limite.isdigit():
            print(Fore.RED + "¡Error! Ingrese un número entero positivo.")
            continue
        limite = int(limite)
        break

    cursor.execute("SELECT * FROM inventario WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()

    if productos:
        print(Fore.RED + f"Productos con stock igual o menor a {limite}:")
        for producto in productos: # Itera sobre los productos encontrados
                    print("-" * 50)
                    print(Fore.RED + "ID: " + Fore.RESET + f"{producto[0]}")
                    print(Fore.RED + "Nombre: " + Fore.RESET + f"{producto[1]}")
                    print(Fore.RED + "Descripción: " + Fore.RESET + f"{producto[2]}")
                    print(Fore.RED + "Cantidad: " + Fore.RESET + f"{producto[3]}")
                    print(Fore.RED + "Precio: " + Fore.RESET + f"${producto[4]:.2f}")
                    print(Fore.RED + "Categoría: " + Fore.RESET + f"{producto[5]}")
                    print("-" * 50)
    else:
        print(Fore.GREEN + "No hay productos con stock bajo según el límite ingresado.")

    conexion.close()

# Definición de usuario y contraseña
def iniciar_sesion():
    """Solicita al usuario que inicie sesión con un usuario y contraseña predefinidos."""
    print(Fore.MAGENTA + "Iniciar sesión")
    intentos = 3 #se inicializa el número de intentos a 3
    while intentos > 0: #Bucle que se mantiene hasta que se agoten los intentos
        usuario = input("Usuario: ").strip()
        clave = input("Contraseña: ").strip()
        if usuario == user and clave == password: #Verifica si el usuario y la contraseña son correctos
            print(Fore.GREEN + "¡Inicio de sesión exitoso!\n")
            return True #Si el usuario y la contraseña son correctos, se retorna True
        else:
            intentos -= 1 #Si el usuario o la contraseña son incorrectos, se resta un intento
            print(Fore.RED + f"Usuario o contraseña incorrectos. Intentente nuevamente.")
    
    print(Fore.RED + "\nDemasiados intentos fallidos. El programa se cerrará.")
    return False # Si se agotan los intentos, se retorna False y el programa finaliza


#Menu principal
def menu_principal():
    while True:
        print(Fore.BLUE + "\n" + "="*40)
        print("      SISTEMA DE GESTIÓN DE INVENTARIO")
        print("="*40 + Style.RESET_ALL)

        print(Fore.CYAN + "1." + Style.RESET_ALL + " Alta de producto")
        print(Fore.CYAN + "2." + Style.RESET_ALL + " Mostrar productos")
        print(Fore.CYAN + "3." + Style.RESET_ALL + " Modificacion de producto")
        print(Fore.CYAN + "4." + Style.RESET_ALL + " Baja de producto")
        print(Fore.CYAN + "5." + Style.RESET_ALL + " Buscar producto")
        print(Fore.CYAN + "6." + Style.RESET_ALL + " Reporte de stock bajo")
        print(Fore.MAGENTA + "7." + Style.RESET_ALL + " Salir")

        opcion = input(Fore.YELLOW + "\nSeleccione una opción (1-7): " + Style.RESET_ALL).strip()

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "\nGracias por usar el sistema. ¡Hasta luego!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente." + Style.RESET_ALL)

# Ejecutar el menú principal
inicializar_base_datos()
# Iniciar sesión antes de mostrar el menú
if iniciar_sesion(): #si se inicia sesión correctamente pasamos al menú principal
# Mostrar el menú principal 
    menu_principal()