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
    opcion = "0"
    while opcion != "7":
        print("Bienvenido Administrador")
        print("Opciones:")
        print("1. Crear Nodo")
        print("2. Crear Relación")
        print("3. Modificar Nodo")
        print("4. Modificar Relación")
        print("5. Eliminar Nodo")
        print("6. Eliminar Relación")
        print("7. Salir")
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
                    language = []
                    while True:
                        l = input("Ingrese el idioma de la película: ")
                        if l == "":
                            break
                        language.append(l)
                    plot = input("Ingrese la trama de la película: ")
                    genres = []
                    while True:
                        g = input("Ingrese el género de la película: ")
                        if g == "":
                            break
                        genres.append(g)
                    revenue_M = input("Ingrese los ingresos de la película: ")
                    budget_M = input("Ingrese el presupuesto de la película: ")
                    classification = input("Ingrese la clasificación de la película: ")
                    propiedades = "{name:'"+name+"',duration:"+duration+",language:"+str(language)+",plot:'"+plot+"',genres:"+str(genres)+",revenue_M:"+revenue_M+",budget_M:"+budget_M+",classification:'"+classification+"'}"
                    session.execute_write(crear_nodo, "Film", propiedades)
            elif subopcion == "2":
                #name,birthDate,deathDate,bio,memberID,nationality
                with driver.session() as session:
                    name = input("Ingrese el nombre del equipo de la película: ")
                    birthDate = input("Ingrese la fecha de nacimiento del miembro: ")
                    deathDate = input("Ingrese la fecha de muerte del miembro: ")
                    bio = input("Ingrese la biografía del miembro: ")
                    memberID = input("Ingrese el ID del miembro: ")
                    propiedades = "{name:'"+name+"',birthDate:'"+birthDate+"',deathDate:'"+deathDate+"',bio:'"+bio+"',memberID:'"+memberID+"'}"
                    session.execute_write(crear_nodo, "MovieTeam", propiedades)
            elif subopcion == "3":
                #name,topics,description,elements,endingType
                with driver.session() as session:
                    name = input("Ingrese el nombre del género: ")
                    topics = []
                    while True:
                        t = input("Ingrese los temas del género: ")
                        if t == "":
                            break
                        topics.append(t)
                    description = input("Ingrese la descripción del género: ")
                    elements = []
                    while True:
                        e = input("Ingrese los elementos del género: ")
                        if e == "":
                            break
                        elements.append(e)
                    endingType = []
                    while True:
                        e = input("Ingrese el tipo de final del género: ")
                        if e == "":
                            break
                        endingType.append(e)
                    propiedades = "{name:'"+name+"',topics:"+str(topics)+",description:'"+description+"',elements:"+str(elements)+",endingType:"+str(endingType)+"}"
                    session.execute_write(crear_nodo, "Genre", propiedades)
            elif subopcion == "4":
                #name,priceId,creationYear,description,impact
                with driver.session() as session:
                    name = "Oscar"
                    priceId = input("Ingrese el ID del premio: ")
                    creationYear = input("Ingrese el año de creación del premio: ")
                    description = input("Ingrese la descripción del premio: ")
                    impact = input("Ingrese el impacto del premio: ")
                    propiedades = "{name:'"+name+"',priceId:'"+priceId+"',creationYear:"+creationYear+",description:'"+description+"',impact:"+impact+"}"
                    session.execute_write(crear_nodo, "Price", propiedades)
            elif subopcion == "5":
                #name,creationYear,duration,original,description,topics
                with driver.session() as session:
                    name = input("Ingrese el nombre de la canción: ")
                    creationYear = input("Ingrese el año de creación de la canción: ")
                    duration = input("Ingrese la duración de la canción: ")
                    original = input("Ingrese si la canción es original: ")
                    description = input("Ingrese la descripción de la canción: ")
                    topics = []
                    while True:
                        t = input("Ingrese los temas de la canción: ")
                        if t == "":
                            break
                        topics.append(t)
                    propiedades = "{name:'"+name+"',creationYear:"+creationYear+",duration:"+duration+",original:'"+original+"',description:'"+description+"',topics:"+str(topics)+"}"
                    session.execute_write(crear_nodo, "Song", propiedades)  
        elif opcion == "2":
            print("Seleccione una opción:")
            print("1. Añadir Miembro del equipo en una película")
            print("2. Añadir Premio a una película")
            print("3. Añadir Premio a un miembro del equipo")
            print("4. Añadir Soundtrack a una película")
            print("5. Añadir Género a una película")
            print("6. Añadir Miembro del equipo a una canción")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    #properties.Role,properties.Since,properties.Until
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    role = input("Ingrese el rol del miembro: ")
                    since = input("Ingrese la fecha de inicio del miembro: ")
                    until = input("Ingrese la fecha de finalización del miembro: ")
                    propiedades = "{Role:'"+role+"',Since:'"+since+"',Until:'"+until+"'}"
                    relationship(driver.session(), idpeli, idmiembro, "PARTICIPATED_IN", propiedades)
            elif subopcion == "2":
                with driver.session() as session:
                    #properties.Year,properties.Percentage,properties.VotesReceived
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombrepremio = input("Ingrese el nombre del premio: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idpremio=get_node_id(driver.session(), "Price", "name", nombrepremio)
                    year = input("Ingrese el año del premio: ")
                    percentage = input("Ingrese el porcentaje del premio: ")
                    votes = input("Ingrese los votos recibidos del premio: ")
                    propiedades = "{Year:"+year+",Percentage:"+percentage+",VotesReceived:"+votes+"}"
                    relationship(driver.session(), idpeli, idpremio, "WON", propiedades)
            elif subopcion == "3":
                with driver.session() as session:
                    #properties.Year,properties.TimesWon,properties.WasInGala
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    year = input("Ingrese el año del premio: ")
                    times = input("Ingrese las veces que ha ganado el premio: ")
                    gala = 1 if input("Ingrese si estuvo en la gala del premio y/n") == "y" else 0
                    propiedades = "{Year:"+year+",TimesWon:"+times+",WasInGala:"+gala+"}"
                    relationship(driver.session(), idmiembro, idpeli, "WON", propiedades) 
            elif subopcion == "4":
                #properties.SelectionDate,properties.MomentShowed,properties.SceneDescription
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombresong = input("Ingrese el nombre de la canción: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idsong=get_node_id(driver.session(), "Song", "name", nombresong)
                    selection = input("Ingrese la fecha de selección de la canción: ")
                    moment = input("Ingrese el momento de la canción: ")
                    scene = input("Ingrese la descripción de la escena de la canción: ")
                    propiedades = "{SelectionDate:'"+selection+"',MomentShowed:'"+moment+"',SceneDescription:'"+scene+"'}"
                    relationship(driver.session(), idpeli, idsong, "SOUNDED_IN", propiedades)
            elif subopcion == "5":
                #properties.PrimaryGenre,properties.SubGenre,properties.Description
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombregenero = input("Ingrese el nombre del género: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idgenero=get_node_id(driver.session(), "Genre", "name", nombregenero)
                    primary = input("Ingrese el género principal de la película: ")
                    sub = input("Ingrese el subgénero de la película: ")
                    description = input("Ingrese la descripción del género de la película: ")
                    propiedades = "{PrimaryGenre:'"+primary+"',SubGenre:'"+sub+"',Description:'"+description+"'}"
                    relationship(driver.session(), idpeli, idgenero, "BELONGS_TO", propiedades)
            elif subopcion == "6":
                #properties.Role,properties.DateReleased,properties.ContributionType
                with driver.session() as session:
                    nombrecancion = input("Ingrese el nombre de la canción: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idcancion=get_node_id(driver.session(), "Song", "name", nombrecancion)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    role = input("Ingrese el rol del miembro en la canción: ")
                    date = input("Ingrese la fecha de lanzamiento de la canción: ")
                    contribution = input("Ingrese el tipo de contribución del miembro: ")
                    propiedades = "{Role:'"+role+"',DateReleased:'"+date+"',ContributionType:'"+contribution+"'}"
                    relationship(driver.session(), idmiembro, idcancion, "PARTICIPATED_IN", propiedades)
        elif opcion == "3":
            print("Seleccione una opción:")
            print("1. Modificar Película")
            print("2. Modificar Equipo de Película")
            print("3. Modificar Género")
            print("4. Modificar Premio")
            print("5. Modificar Canción")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la película: ")
                    query = (
                        f"MATCH (n:Film) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Duración")
                    print("2. Idioma")
                    print("3. Trama")
                    print("4. Géneros")
                    print("5. Ingresos")
                    print("6. Presupuesto")
                    print("7. Clasificación")
                    print("8. Nombre")
                    subopcion = input()
                    if subopcion == "1":
                        duration = input("Ingrese la nueva duración de la película: ")
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.duration = {duration}"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        lenguaje=[]
                        while True:
                            l = input("Ingrese el nuevo idioma de la película: ")
                            if l == "":
                                break
                            lenguaje.append(l)
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.language = {lenguaje}"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        plot = input("Ingrese la nueva trama de la película: ")
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.plot = '{plot}'"
                        )
                        session.run(query)
                    elif subopcion == "4":
                        genres = []
                        while True:
                            g = input("Ingrese el nuevo género de la película: ")
                            if g == "":
                                break
                            genres.append(g)
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.genres = {genres}"
                        )
                        session.run(query)
                    elif subopcion == "5":
                        revenue = input("Ingrese los nuevos ingresos de la película: ")
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.revenue_M = {revenue}"
                        )
                        session.run(query)
                    elif subopcion == "6":
                        budget = input("Ingrese el nuevo presupuesto de la película: ")
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.budget_M = {budget}"
                        )
                        session.run(query)
                    elif subopcion == "7":
                        classification = input("Ingrese la nueva clasificación de la película: ")
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.classification = '{classification}'"
                        )
                        session.run(query)
                    elif subopcion == "8":
                        name = input("Ingrese el nuevo nombre de la película: ")
                        query = (
                            f"MATCH (n:Film) WHERE n.name = '{nombre}' SET n.name = '{name}'"
                        )
                        session.run(query)
            elif subopcion == "2":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del equipo de la película: ")
                    query = (
                        f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Fecha de Nacimiento")
                    print("2. Fecha de Muerte")
                    print("3. Biografía")
                    print("4. ID")
                    print("5. Nombre")
                    print("6. Nacionalidad")
                    subopcion = input()
                    if subopcion == "1":
                        birthDate = input("Ingrese la nueva fecha de nacimiento del miembro: ")
                        query = (
                            f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' SET n.birthDate = '{birthDate}'"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        deathDate = input("Ingrese la nueva fecha de muerte del miembro: ")
                        query = (
                            f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' SET n.deathDate = '{deathDate}'"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        bio = input("Ingrese la nueva biografía del miembro: ")
                        query = (
                            f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' SET n.bio = '{bio}'"
                        )
                        session.run(query)
                    elif subopcion == "4":
                        memberID = input("Ingrese el nuevo ID del miembro: ")
                        query = (
                            f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' SET n.memberID = '{memberID}'"
                        )
                        session.run(query)
                    elif subopcion == "5":
                        name = input("Ingrese el nuevo nombre del equipo de la película: ")
                        query = (
                            f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' SET n.name = '{name}'"
                        )
                        session.run(query)
                    elif subopcion == "6":
                        nationality = input("Ingrese la nueva nacionalidad del miembro: ")
                        query = (
                            f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' SET n.nationality = '{nationality}'"
                        )
                        session.run(query)
            elif subopcion == "3":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del género: ")
                    query = (
                        f"MATCH (n:Genre) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Temas")
                    print("2. Descripción")
                    print("3. Elementos")
                    print("4. Tipo de Final")
                    print("5. Nombre")
                    subopcion = input()
                    if subopcion == "1":
                        topics = []
                        while True:
                            t = input("Ingrese los nuevos temas del género: ")
                            if t == "":
                                break
                            topics.append(t)
                        query = (
                            f"MATCH (n:Genre) WHERE n.name = '{nombre}' SET n.topics = {topics}"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        description = input("Ingrese la nueva descripción del género: ")
                        query = (
                            f"MATCH (n:Genre) WHERE n.name = '{nombre}' SET n.description = '{description}'"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        elements = []
                        while True:
                            e = input("Ingrese los nuevos elementos del género: ")
                            if e == "":
                                break
                            elements.append(e)
                        query = (
                            f"MATCH (n:Genre) WHERE n.name = '{nombre}' SET n.elements = {elements}"
                        )
                        session.run(query)
                    elif subopcion == "4":
                        ending = []
                        while True:
                            e = input("Ingrese el nuevo tipo de final del género: ")
                            if e == "":
                                break
                            ending.append(e)
                        query = (
                            f"MATCH (n:Genre) WHERE n.name = '{nombre}' SET n.endingType = {ending}"
                        )
                        session.run(query)
                    elif subopcion == "5":
                        name = input("Ingrese el nuevo nombre del género: ")
                        query = (
                            f"MATCH (n:Genre) WHERE n.name = '{nombre}' SET n.name = '{name}'"
                        )
                        session.run(query)
            elif subopcion == "4":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del premio: ")
                    query = (
                        f"MATCH (n:Price) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. ID")
                    print("2. Año de Creación")
                    print("3. Descripción")
                    print("4. Impacto")
                    print("5. Nombre")
                    subopcion = input()
                    if subopcion == "1":
                        priceId = input("Ingrese el nuevo ID del premio: ")
                        query = (
                            f"MATCH (n:Price) WHERE n.name = '{nombre}' SET n.priceId = '{priceId}'"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        creationYear = input("Ingrese el nuevo año de creación del premio: ")
                        query = (
                            f"MATCH (n:Price) WHERE n.name = '{nombre}' SET n.creationYear = {creationYear}"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        description = input("Ingrese la nueva descripción del premio: ")
                        query = (
                            f"MATCH (n:Price) WHERE n.name = '{nombre}' SET n.description = '{description}'"
                        )
                        session.run(query)
                    elif subopcion == "4":
                        impact = input("Ingrese el nuevo impacto del premio: ")
                        query = (
                            f"MATCH (n:Price) WHERE n.name = '{nombre}' SET n.impact = {impact}"
                        )
                        session.run(query)
                    elif subopcion == "5":
                        name = input("Ingrese el nuevo nombre del premio: ")
                        query = (
                            f"MATCH (n:Price) WHERE n.name = '{nombre}' SET n.name = '{name}'"
                        )
                        session.run(query)
            elif subopcion == "5":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la canción: ")
                    query = (
                        f"MATCH (n:Song) WHERE n.name = '{nombre}' RETURN n"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Año de Creación")
                    print("2. Duración")
                    print("3. Original")
                    print("4. Descripción")
                    print("5. Temas")
                    print("6. Nombre")
                    subopcion = input()
                    if subopcion == "1":
                        creationYear = input("Ingrese el nuevo año de creación de la canción: ")
                        query = (
                            f"MATCH (n:Song) WHERE n.name = '{nombre}' SET n.creationYear = {creationYear}"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        duration = input("Ingrese la nueva duración de la canción: ")
                        query = (
                            f"MATCH (n:Song) WHERE n.name = '{nombre}' SET n.duration = {duration}"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        original = input("Ingrese si la canción es original: ")
                        query = (
                            f"MATCH (n:Song) WHERE n.name = '{nombre}' SET n.original = '{original}'"
                        )
                        session.run(query)
                    elif subopcion == "4":
                        description = input("Ingrese la nueva descripción de la canción: ")
                        query = (
                            f"MATCH (n:Song) WHERE n.name = '{nombre}' SET n.description = '{description}'"
                        )
                        session.run(query)
                    elif subopcion == "5":
                        topics = []
                        while True:
                            t = input("Ingrese los nuevos temas de la canción: ")
                            if t == "":
                                break
                            topics.append(t)
                        query = (
                            f"MATCH (n:Song) WHERE n.name = '{nombre}' SET n.topics = {topics}"
                        )
                        session.run(query)
                    elif subopcion == "6":
                        name = input("Ingrese el nuevo nombre de la canción: ")
                        query = (
                            f"MATCH (n:Song) WHERE n.name = '{nombre}' SET n.name = '{name}'"
                        )
                        session.run(query)
        elif opcion == "4":
            print("Seleccione una opción:")
            print("1. Modificar Relación de Miembro del equipo en una película")
            print("2. Modificar Relación de Premio a una película")
            print("3. Modificar Relación de Premio a un miembro del equipo")
            print("4. Modificar Relación de Soundtrack a una película")
            print("5. Modificar Relación de Género a una película")
            print("6. Modificar Relación de Miembro del equipo a una canción")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    query = (
                        f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idmiembro} RETURN r"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Rol")
                    print("2. Fecha de Inicio")
                    print("3. Fecha de Finalización")
                    subopcion = input()
                    if subopcion == "1":
                        role = input("Ingrese el nuevo rol del miembro: ")
                        query = (
                            f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idmiembro} SET r.Role = '{role}'"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        since = input("Ingrese la nueva fecha de inicio del miembro: ")
                        query = (
                            f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idmiembro} SET r.Since = '{since}'"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        until = input("Ingrese la nueva fecha de finalización del miembro: ")
                        query = (
                            f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idmiembro} SET r.Until = '{until}'"
                        )
                        session.run(query)
            elif subopcion == "2":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombrepremio = input("Ingrese el nombre del premio: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idpremio=get_node_id(driver.session(), "Price", "name", nombrepremio)
                    query = (
                        f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idpeli} AND id(b) = {idpremio} RETURN r"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Año")
                    print("2. Porcentaje")
                    print("3. Votos Recibidos")
                    subopcion = input()
                    if subopcion == "1":
                        year = input("Ingrese el nuevo año del premio: ")
                        query = (
                            f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idpeli} AND id(b) = {idpremio} SET r.Year = {year}"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        percentage = input("Ingrese el nuevo porcentaje del premio: ")
                        query = (
                            f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idpeli} AND id(b) = {idpremio} SET r.Percentage = {percentage}"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        votes = input("Ingrese los nuevos votos recibidos del premio: ")
                        query = (
                            f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idpeli} AND id(b) = {idpremio} SET r.VotesReceived = {votes}"
                        )
                        session.run(query)
            elif subopcion == "3":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    query = (
                        f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idpeli} RETURN r"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Año")
                    print("2. Veces Ganadas")
                    print("3. Estuvo en Gala")
                    subopcion = input()
                    if subopcion == "1":
                        year = input("Ingrese el nuevo año del premio: ")
                        query = (
                            f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idpeli} SET r.Year = {year}"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        times = input("Ingrese las nuevas veces que ha ganado el premio: ")
                        query = (
                            f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idpeli} SET r.TimesWon = {times}"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        gala = 1 if input("Ingrese si estuvo en la gala del premio y/n") == "y" else 0
                        query = (
                            f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idpeli} SET r.WasInGala = {gala}"
                        )
                        session.run(query)
            elif subopcion == "4":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombresong = input("Ingrese el nombre de la canción: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idsong=get_node_id(driver.session(), "Song", "name", nombresong)
                    query = (
                        f"MATCH (a)-[r:SOUNDED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idsong} RETURN r"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Fecha de Selección")
                    print("2. Momento")
                    print("3. Descripción de Escena")
                    subopcion = input()
                    if subopcion == "1":
                        selection = input("Ingrese la nueva fecha de selección de la canción: ")
                        query = (
                            f"MATCH (a)-[r:SOUNDED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idsong} SET r.SelectionDate = '{selection}'"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        moment = input("Ingrese el nuevo momento de la canción: ")
                        query = (
                            f"MATCH (a)-[r:SOUNDED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idsong} SET r.MomentShowed = '{moment}'"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        scene = input("Ingrese la nueva descripción de la escena de la canción: ")
                        query = (
                            f"MATCH (a)-[r:SOUNDED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idsong} SET r.SceneDescription = '{scene}'"
                        )
                        session.run(query)
            elif subopcion == "5":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombregenero = input("Ingrese el nombre del género: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idgenero=get_node_id(driver.session(), "Genre", "name", nombregenero)
                    query = (
                        f"MATCH (a)-[r:BELONGS_TO]->(b) WHERE id(a) = {idpeli} AND id(b) = {idgenero} RETURN r"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Género Principal")
                    print("2. Subgénero")
                    print("3. Descripción")
                    subopcion = input()
                    if subopcion == "1":
                        primary = input("Ingrese el nuevo género principal de la película: ")
                        query = (
                            f"MATCH (a)-[r:BELONGS_TO]->(b) WHERE id(a) = {idpeli} AND id(b) = {idgenero} SET r.PrimaryGenre = '{primary}'"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        sub = input("Ingrese el nuevo subgénero de la película: ")
                        query = (
                            f"MATCH (a)-[r:BELONGS_TO]->(b) WHERE id(a) = {idpeli} AND id(b) = {idgenero} SET r.SubGenre = '{sub}'"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        description = input("Ingrese la nueva descripción del género de la película: ")
                        query = (
                            f"MATCH (a)-[r:BELONGS_TO]->(b) WHERE id(a) = {idpeli} AND id(b) = {idgenero} SET r.Description = '{description}'"
                        )
                        session.run(query)
            elif subopcion == "6":
                with driver.session() as session:
                    nombrecancion = input("Ingrese el nombre de la canción: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idcancion=get_node_id(driver.session(), "Song", "name", nombrecancion)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    query = (
                        f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idcancion} RETURN r"
                    )
                    result = session.run(query)
                    propiedades = result.single()[0]
                    propiedades = dict(propiedades)
                    print("Propiedades actuales:")
                    for key, value in propiedades.items():
                        print(f"{key}: {value}")
                    print("Propiedades a modificar:")
                    print("1. Rol")
                    print("2. Fecha de Lanzamiento")
                    print("3. Tipo de Contribución")
                    subopcion = input()
                    if subopcion == "1":
                        role = input("Ingrese el nuevo rol del miembro en la canción: ")
                        query = (
                            f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idcancion} SET r.Role = '{role}'"
                        )
                        session.run(query)
                    elif subopcion == "2":
                        date = input("Ingrese la nueva fecha de lanzamiento de la canción: ")
                        query = (
                            f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idcancion} SET r.DateReleased = '{date}'"
                        )
                        session.run(query)
                    elif subopcion == "3":
                        contribution = input("Ingrese el nuevo tipo de contribución del miembro: ")
                        query = (
                            f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idcancion} SET r.ContributionType = '{contribution}'"
                        )
                        session.run(query)
        elif opcion == "5":
            print("Seleccione una opción:")
            print("1. Eliminar Película")
            print("2. Eliminar Equipo de Película")
            print("3. Eliminar Género")
            print("4. Eliminar Premio")
            print("5. Eliminar Canción")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la película: ")
                    query = (
                        f"MATCH (n:Film) WHERE n.name = '{nombre}' DETACH DELETE n"
                    )
                    session.run(query)
            elif subopcion == "2":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del equipo de la película: ")
                    query = (
                        f"MATCH (n:MovieTeam) WHERE n.name = '{nombre}' DETACH DELETE n"
                    )
                    session.run(query)
            elif subopcion == "3":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del género: ")
                    query = (
                        f"MATCH (n:Genre) WHERE n.name = '{nombre}' DETACH DELETE n"
                    )
                    session.run(query)
            elif subopcion == "4":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre del premio: ")
                    query = (
                        f"MATCH (n:Price) WHERE n.name = '{nombre}' DETACH DELETE n"
                    )
                    session.run(query)
            elif subopcion == "5":
                with driver.session() as session:
                    nombre = input("Ingrese el nombre de la canción: ")
                    query = (
                        f"MATCH (n:Song) WHERE n.name = '{nombre}' DETACH DELETE n"
                    )
                    session.run(query)
        elif opcion == "6":
            print("Seleccione una opción:")
            print("1. Eliminar Relación de Miembro del equipo en una película")
            print("2. Eliminar Relación de Premio a una película")
            print("3. Eliminar Relación de Premio a un miembro del equipo")
            print("4. Eliminar Relación de Soundtrack a una película")
            print("5. Eliminar Relación de Género a una película")
            print("6. Eliminar Relación de Miembro del equipo a una canción")
            subopcion = input()
            if subopcion == "1":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    query = (
                        f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idmiembro} DELETE r"
                    )
                    session.run(query)
            elif subopcion == "2":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombrepremio = input("Ingrese el nombre del premio: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idpremio=get_node_id(driver.session(), "Price", "name", nombrepremio)
                    query = (
                        f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idpeli} AND id(b) = {idpremio} DELETE r"
                    )
                    session.run(query)
            elif subopcion == "3":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    query = (
                        f"MATCH (a)-[r:WON]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idpeli} DELETE r"
                    )
                    session.run(query)
            elif subopcion == "4":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombresong = input("Ingrese el nombre de la canción: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idsong=get_node_id(driver.session(), "Song", "name", nombresong)
                    query = (
                        f"MATCH (a)-[r:SOUNDED_IN]->(b) WHERE id(a) = {idpeli} AND id(b) = {idsong} DELETE r"
                    )
                    session.run(query)
            elif subopcion == "5":
                with driver.session() as session:
                    nombrepelicula = input("Ingrese el nombre de la película: ")
                    nombregenero = input("Ingrese el nombre del género: ")
                    idpeli=get_node_id(driver.session(), "Film", "name", nombrepelicula)
                    idgenero=get_node_id(driver.session(), "Genre", "name", nombregenero)
                    query = (
                        f"MATCH (a)-[r:BELONGS_TO]->(b) WHERE id(a) = {idpeli} AND id(b) = {idgenero} DELETE r"
                    )
                    session.run(query)
            elif subopcion == "6":
                with driver.session() as session:
                    nombrecancion = input("Ingrese el nombre de la canción: ")
                    nombremiembro = input("Ingrese el nombre del miembro del equipo: ")
                    idcancion=get_node_id(driver.session(), "Song", "name", nombrecancion)
                    idmiembro=get_node_id(driver.session(), "MovieTeam", "name", nombremiembro)
                    query = (
                        f"MATCH (a)-[r:PARTICIPATED_IN]->(b) WHERE id(a) = {idmiembro} AND id(b) = {idcancion} DELETE r"
                    )
                    session.run(query)
        
driver.close()