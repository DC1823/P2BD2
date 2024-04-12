import pandas as pd
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
    query = (
        f"CREATE (n:{label} {properties})"
        "RETURN n"
    )
    result = tx.run(query)
    return result.single()[0]

def ver_relaciones(tx, node_id, node_idb):
    query = (
        f"MATCH (a)-[r]->(b) WHERE id(a) = {node_id} AND id(b) = {node_idb} RETURN r"
    )
    result = tx.run(query)
    return result.single()[0]

#Bienvenida
print("Bienvenido a la base de datos de los Oscars")
user = input("Ingrese su Usuario: ")
password = input("Ingrese su Contraseña: ")
try:
    idnodousuario=get_node_id(driver.session(), "User", "userId", user)
except:
    print("Usuario no encontrado")
    print("Desea registrarse? y/n")
    if input() == "y":
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
while opcion != "a":
    print("Opciones:")
    print("1. Ver todos los registros")
    print("2. Buscar información")
    print("3. Consultar Peliculas que recomiendo")
    print("6. Buscar pelicula")
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
       prop = dict(prop)
       for key, value in prop.items():
           print(f"{key}: {value}")

driver.close()