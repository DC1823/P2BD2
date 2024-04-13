import datetime
from neo4j import GraphDatabase

# Conexión a Neo4j Aura
uri = "neo4j+s://e56e5356.databases.neo4j.io"
user = "neo4j"
password = "k9RVhm16fe4wjI1pjvx7xlbDfbOCbk2JKLlbMFGhCuw"

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_node_id(tx, label, property, value):
    query = (
        f"MATCH (n:{label}) WHERE n.{property} = '{value}'"
        "RETURN id(n)"
    )
    result = tx.run(query)
    return result.single()[0]

def crear_nodo(tx, label, properties):
    try:
        query = (
            f"CREATE (n:{label} {properties})"
            "RETURN n"
        )
        result = tx.run(query)
        return result.single()[0]
    except:
        return []

#1 o mas relaciones
def ver_relaciones(tx, node_id, node_idb):
    try:
        query = (
            f"MATCH (a)-[r]->(b) WHERE id(a) = {node_id} AND id(b) = {node_idb} RETURN r"
        )
        result = tx.run(query)
        return [record["r"] for record in result]
    except:
        return []

def relationship(tx, start_node_id, end_node_id, rela, properties):
    query = (
        f"MATCH (a) WHERE id(a) = {start_node_id}"
        f" MATCH (b) WHERE id(b) = {end_node_id}"
        f" CREATE (a)-[r:{rela} {properties}]->(b)"
        "RETURN r"
    )
    result = tx.run(query)
    return result.single()[0]

#Bienvenida
print("Bienvenido a la base de datos de los Oscars")
user = input("Ingrese su Usuario: ")
password = input("Ingrese su Contraseña: ")
if user != "admin" and password != "admin":
    try:
        idnodousuario=get_node_id(driver.session(), "User", "userId", user)
    except:
        print("Usuario no encontrado")
        print("Desea registrarse? y/n")
        if input() == "y" or input() == "Y" or input() == "yes" or input() == "Yes":
            with driver.session() as session:
                name = input("Ingrese su nombre: ")
                nationality = input("Ingrese su nacionalidad: ")
                sex= input("Ingrese su sexo: ")
                email = input("Ingrese su email: ")
                propiedades = "{name:'"+name+"',userId:'"+user+"',sex:'"+sex+"',email:'"+email+"',nationality:'"+nationality+"',password:'"+password+"'}"
                session.execute_write(crear_nodo, "User", propiedades)
        else:
            driver.close()
            exit()
    #Menu
    opcion = "0"
    while opcion != "9":
        print("Opciones:")
        print("1. Ver todos los registros")
        print("2. Buscar información")
        print("3. Consultar Peliculas que recomiendo")
        print("4. Consultar Miembros del equipo que me gustan")
        print("5. Consultar los géneros de las películas que me gustan")
        print("6. Votar por una película")
        print("7. Recomendar películas")
        print("8. Añadir Miembro del equipo que me gusta")
        print("9. Salir")
        opcion = input()
        if opcion=="1":
            print("Seleccione una opción:")
            print("1. Películas")
            print("2. Equipos de películas")
            print("3. Géneros")
            print("4. Premios")
            print("5. Canciones")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    query = (
                        "MATCH (n:Film) RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        print("Título: "+propiedades["name"])
            elif subopcion == "2":
                with driver.session() as session:
                    query = (
                        "MATCH (n:MovieTeam) RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        print("Nombre: "+propiedades["name"])
            elif subopcion == "3":
                with driver.session() as session:
                    query = (
                        "MATCH (n:Genre) RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        print("Nombre: "+propiedades["name"])
            elif subopcion == "4":
                with driver.session() as session:
                    query = (
                        "MATCH (n:Price) RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        print("Nombre: "+propiedades["name"])
            elif subopcion == "5":
                with driver.session() as session:
                    query = (
                        "MATCH (n:Song) RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        print("Nombre: "+propiedades["name"])
            elif subopcion == "6":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la película: ")
                    query = (
                        f"MATCH (n:Film) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        print("Nombre: "+propiedades["name"])
        elif opcion=="2":
            print("Seleccione una opción para buscar:")
            print("1. Películas")
            print("2. Equipos de películas")
            print("3. Géneros")
            print("4. Premios")
            print("5. Canciones")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la película: ")
                    query = (
                        f"MATCH (n:Film) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        for key, value in propiedades.items():
                            print(f"{key}: {value}")
            elif subopcion == "2":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del equipo de la película: ")
                    query = (
                        f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        for key, value in propiedades.items():
                            print(f"{key}: {value}")
            elif subopcion == "3":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del género: ")
                    query = (
                        f"MATCH (n:Genre) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        for key, value in propiedades.items():
                            print(f"{key}: {value}")
            elif subopcion == "4":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del premio: ")
                    query = (
                        f"MATCH (n:Price) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        for key, value in propiedades.items():
                            print(f"{key}: {value}")
            elif subopcion == "5":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la canción: ")
                    query = (
                        f"MATCH (n:Song) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    for record in result:
                        propiedades = record["n"]
                        propiedades = dict(propiedades)
                        for key, value in propiedades.items():
                            print(f"{key}: {value}")    
        elif opcion=="3":
           nombrepelicula = input("Ingrese el nombre de la película: ")
           idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
           prop=(ver_relaciones(driver.session(), idnodousuario, idpeli))
           for i in prop:
             prop = dict(i)
             for key, value in prop.items():
                  print(f"{key}: {value}")
        elif opcion=="4":
            nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
            idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
            prop=(ver_relaciones(driver.session(), idnodousuario, idmiembro))
            for i in prop:
                prop = dict(i)
                for key, value in prop.items():
                    print(f"{key}: {value}")
        elif opcion=="5":
            nombregenero = input("Ingrese el nombre del género: ")
            idgenero=get_node_id(driver.session(), "Genre", "name", nombregenero)
            prop=(ver_relaciones(driver.session(), idnodousuario, idgenero))
            for i in prop:
                prop = dict(i)
                for key, value in prop.items():
                    print(f"{key}: {value}")
        elif opcion=="6":
            nombrepelicula = input("Ingrese el nombre de la película: ")
            idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
            voto = input("Ingrese su rating(0-5): ")
            recomendacion = input("Ingrese su recomendación(0-5): ")
            fecha = str(datetime.datetime.now().date())
            propiedades = "{Rating:"+voto+",Recommended:'"+recomendacion+"',DateRated:'"+fecha+"'}"
            relationship(driver.session(), idnodousuario, idpeli, "RATED", propiedades)
        elif opcion=="7":
            nombrepelicula = input("Ingrese el nombre de la película: ")
            idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
            duration = input("Ingrese la duración que vio la película: ")
            tags = input("Ingrese los tags que le gustaron de la película: ")
            fecha = str(datetime.datetime.now().date())
            propiedades = "{DurationWatched:"+duration+",Tags:'"+tags+"',Date:'"+fecha+"'}"
            relationship(driver.session(), idnodousuario, idpeli, "RECOMMENDS", propiedades)
        elif opcion=="8":
            nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
            idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
            niveldeinteres = input("Ingrese su nivel de interés(0-5): ")
            comentarios = input("Ingrese sus comentarios: ")
            fecha = str(datetime.datetime.now().date())
            propiedades = "{InterestLevel:"+niveldeinteres+",Comment:'"+comentarios+"',Date_Liked:'"+fecha+"'}"
            relationship(driver.session(), idnodousuario, idmiembro, "LIKES", propiedades)
        elif opcion=="9":
            print("Vuelva pronto!")
else:
    print("Bienvenido Administrador")
    print("Opciones:")
    print("1. Crear Nodo")
    print("2. Crear Relación")
    print("3. Modificar Nodo")
    print("4. Modificar Relación")
    print("5. Eliminar Nodo")
    print("6. Eliminar Relación")
    opcion = input()
    if opcion == "1":
        print("Seleccione una opción:")
        print("1. Películas")
        print("2. Equipos de películas")
        print("3. Géneros")
        print("4. Premios")
        print("5. Canciones")
        subopcion = input()
        if subopcion == "1":
            with driver.session() as session:
                name = input("Ingrese el nombre de la película: ")
                duration = input("Ingrese la duración de la película: ")
                language = [input("Ingrese los idiomas de la película: ")]
                plot = input("Ingrese la trama de la película: ")
                genres = [input("Ingrese los géneros de la película: ")]
                revenue_M = input("Ingrese los ingresos de la película: ")
                budget_M = input("Ingrese el presupuesto de la película: ")
                classification = input("Ingrese la clasificación de la película: ")
                propiedades = "{name:'"+name+"',duration:"+duration+",language:"+language+",plot:'"+plot+"',genres:"+genres+",revenue_M:"+revenue_M+",budget_M:"+budget_M+",classification:'"+classification+"'}"
                session.execute_write(crear_nodo, "Film", propiedades)
            
driver.close()