def genera_contenido_ldif_multiples_unidades_organizativas(filename, lista_ou_name, base_dn):
    """Genera un archivo LDIF con múltiples unidades organizativas."""
    ldif_content = ""
    
    for ou_name in lista_ou_name:
        ldif_content += f"""
# Organisational unit for {ou_name} department
dn: ou={ou_name},{base_dn}
changetype: add
objectClass: organizationalUnit
ou: {ou_name}
"""
    
    try:
        with open(filename, "w") as f:
            f.write(ldif_content)
        print(f"LDIF file '{filename}' created successfully.")
    except Exception as e:
        print(f"Error creating LDIF file '{filename}': {e}")


# Lista inicial de unidades organizativas
lista_ou_name = [
    "directores", "profesores", "alumnos"
]

# Lista extendida con más unidades organizativas
lista_ou_name.extend([
    "personalnodocente", "eso1", "eso2", "eso3", "eso4",
    "bach1ciencias", "bach1humanidades", "bach2ciencias", "bach2humanidades",
    "profesoreseso", "profesoresbach", "profesoreseso1", "profesoreseso2",
    "profesoreseso3", "profesoreseso4", "profesoresbach1ciencias",
    "profesoresbach1humanidades", "profesoresbach2ciencias", "profesoresbach2humanidades"
])

# Parámetros
filename = "ou_multiples.ldif"  # Nombre del archivo LDIF
base_dn = "dc=soler,dc=org"    # Base DN tomado del docker-compose

# Llamar a la función para generar el LDIF
genera_contenido_ldif_multiples_unidades_organizativas(filename, lista_ou_name, base_dn)

# Instrucciones para importar el LDIF en OpenLDAP
def importar_ldif_en_openldap(ldif_file):
    import os
    
    command = f"docker cp {ldif_file} openldap:/tmp/{ldif_file} && " \
              f"docker exec -it openldap ldapadd -x -D 'cn=admin,{base_dn}' -w admin -f /tmp/{ldif_file}"
    
    os.system(command)
    print(f"Archivo {ldif_file} importado en OpenLDAP.")

# Importar automáticamente el archivo generado en OpenLDAP
importar_ldif_en_openldap(filename)
