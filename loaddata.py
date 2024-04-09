import pandas as pd
from py2neo import Graph, Node, Relationship

# Conexión a Neo4j Aura
uri = "neo4j+s://e56e5356.databases.neo4j.io"
user = "neo4j"
password = "k9RVhm16fe4wjI1pjvx7xlbDfbOCbk2JKLlbMFGhCuw"
graph = Graph(uri, auth=(user, password))

# Rutas a los archivos CSV
user_csv = "user.csv"
movie_team_csv = "mteam.csv"
genre_csv = "genre.csv"
film_csv = "film.csv"
price_csv = "price.csv"
song_csv = "song.csv"

# Función para cargar nodos desde CSV
def load_nodes_from_csv(file_path, label):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        node = Node(label, **row)
        graph.create(node)

# Función para crear relaciones desde CSVs usando nombres en lugar de IDs
def create_relationships_from_csv(file_path, rel_type, start_node_label, end_node_label):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        start_node_name = row["start_node_id"]
        end_node_name = row["end_node_id"]
        start_node = graph.nodes.match(start_node_label, name=start_node_name).first()
        end_node = graph.nodes.match(end_node_label, name=end_node_name).first()
        if start_node and end_node:
            relationship = Relationship(start_node, rel_type, end_node, **row["properties"])
            graph.create(relationship)
        else:
            print(f"Error: Nodes {start_node_name} or {end_node_name} not found.")

# Cargar nodos desde CSVs
load_nodes_from_csv(user_csv, "User")
load_nodes_from_csv(movie_team_csv, "MovieTeam")
load_nodes_from_csv(genre_csv, "Genre")
load_nodes_from_csv(film_csv, "Film")
load_nodes_from_csv(price_csv, "Price")
load_nodes_from_csv(song_csv, "Song")

# Crear relaciones desde CSVs
create_relationships_from_csv("partin.csv", "PARTICIPED_IN", "MovieTeam", "Film")

