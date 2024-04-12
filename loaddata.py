import pandas as pd
from neo4j import GraphDatabase


# Conexión a Neo4j Aura
uri = "neo4j+s://e56e5356.databases.neo4j.io"
user = "neo4j"
password = "k9RVhm16fe4wjI1pjvx7xlbDfbOCbk2JKLlbMFGhCuw"

# Rutas a los archivos CSV
user_csv = "user.csv"
movie_team_csv = "mteam.csv"
genre_csv = "genre.csv"
film_csv = "film.csv"
price_csv = "price.csv"
song_csv = "song.csv"

# Función para crear un nodo en la base de datos
def create_node(tx, label, properties):
    query = (
        f"CREATE (n:{label} {properties})"
        "RETURN n"
    )
    result = tx.run(query)
    return result.single()[0]

def load_data_csv(csv,nodetype):
    df = pd.read_csv(csv)
    for index, row in df.iterrows():
        properties = "{"
        for key, value in row.items():
            #Ver si value es un string o un int
            try:
                value=int(value)
                properties = properties + f"{key}: {value}, " 
            except:
                properties = properties + f"{key}: '{value}', " 
        properties = properties[:-2]
        properties += "}"
        properties = properties.replace("'[", "[")
        properties = properties.replace("]'", "]")
        with driver.session() as session:
            session.execute_write(create_node, nodetype, properties)

def load_relationship_csv(csv,rela, label, prop, labelb, propb,driver):
    df = pd.read_csv(csv)
    info = []
    for index, row in df.iterrows():
        properties = "{"
        for key, value in row.items():
            if key != "start_node_id" and key != "end_node_id":
                try:
                    value=int(value)
                    properties = properties + f"{key}: {value}, " 
                except:
                    properties = properties + f"{key}: '{value}', " 
            elif key == "start_node_id":
                info.append(value)
            elif key == "end_node_id":
                info.append(value)
        properties = properties[:-2]
        properties += "}"
        properties = properties.replace("'[", "[")
        properties = properties.replace("]'", "]")
        properties = properties.replace("properties.", "")
        info.append(properties)
        id_1 = get_node_id(driver.session(), label, prop, info[0])
        id_2 = get_node_id(driver.session(), labelb, propb, info[1])
        relationship(driver.session(), id_1, id_2, rela, info[2])
        info = []

def relationship(tx, start_node_id, end_node_id, rela, properties):
    query = (
        f"MATCH (a) WHERE id(a) = {start_node_id}"
        f" MATCH (b) WHERE id(b) = {end_node_id}"
        f" CREATE (a)-[r:{rela} {properties}]->(b)"
        "RETURN r"
    )
    result = tx.run(query)
    return result.single()[0]

def get_node_id(tx, label, property, value):
    query = (
        f"MATCH (n:{label}) WHERE n.{property} = '{value}'"
        "RETURN id(n)"
    )
    result = tx.run(query)
    return result.single()[0]

driver = GraphDatabase.driver(uri, auth=(user, password))
load_data_csv(user_csv, "User")
load_data_csv(movie_team_csv, "MovieTeam")
load_data_csv(genre_csv, "Genre")
load_data_csv(film_csv, "Film")
load_data_csv(price_csv, "Price")
load_data_csv(song_csv, "Song")

# Crear relaciones
load_relationship_csv("partin.csv", "PARTICIPATED_IN", "MovieTeam", "name", "Film", "name",driver)
load_relationship_csv("won.csv", "WON", "Film", "name", "Price", "name",driver)
load_relationship_csv("obtained.csv", "OBTAINED","MovieTeam", "name", "Price", "name",driver)
load_relationship_csv("soundtrack.csv", "SOUNDTRACK_OF", "Song", "name", "Film", "name",driver)
load_relationship_csv("likes.csv", "LIKES", "User", "name", "MovieTeam", "name",driver)
load_relationship_csv("hasgenre.csv", "HAS_GENRE", "Film", "name", "Genre", "name",driver)
load_relationship_csv("recom.csv", "RECOMMENDS", "User", "name", "Film", "name",driver)
load_relationship_csv("pgenre.csv", "PREFERS_GENRE", "User", "name", "Genre", "name",driver)
load_relationship_csv("mcountr.csv", "MUSIC_CONTRIBUTION", "MovieTeam", "name", "Song", "name",driver)
load_relationship_csv("rated.csv", "RATED", "User", "name", "Film", "name",driver)

driver.close()