import requests

# URL de registro
register_url = 'https://makers-challenge.altscore.ai/v1/register'

# Datos de registro (ajustados según los requisitos)
data = {
    "alias": "alex_strange",           # Tu alias o nombre de usuario
    "country": "MEX",                  # Código de país ISO 3166-1 alpha-3
    "email": "codelogman@gmail.com",       # Tu correo electrónico real
    "apply_role": "engineering"        # Rol válido: "engineering", "data", o "integrations"
}

# Enviar la solicitud de registro
response = requests.post(register_url, json=data)

# Verificar la respuesta y manejar errores
if response.status_code == 200:
    print("Registro exitoso. Respuesta:", response.json())
else:
    print("Error en el registro. Código de estado:", response.status_code)
    print("Contenido de la respuesta:", response.text)

