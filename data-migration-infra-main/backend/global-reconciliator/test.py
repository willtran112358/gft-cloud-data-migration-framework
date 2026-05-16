fields = ['id2', 'details']
table_name = 'my_table'
# Construir la cadena de la consulta con comillas simples
query = "SELECT " + ", ".join([f"{field}" for field in fields]) + f" FROM {table_name}"

# Mostrar el resultado
print(query)