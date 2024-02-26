import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Lê as variáveis de ambiente
# POSTGRES_USER = os.getenv('POSTGRES_USER')
# POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
# POSTGRES_HOST = os.getenv('POSTGRES_HOST')
# POSTGRES_PORT = os.getenv('POSTGRES_PORT')
# POSTGRES_DB = os.getenv('POSTGRES_DB')

POSTGRES_USER='dbnameworkshop_hlyr_user'
POSTGRES_PASSWORD='BeYZh0z3NPo6mvI9IONBfXFAi9pHyxYd'
POSTGRES_HOST='dpg-cncvv9acn0vc73f4dp7g-a.oregon-postgres.render.com'
POSTGRES_PORT=5432
POSTGRES_DB='dbnameworkshop_hlyr'


# Cria a URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def test_read_data_and_check_schema():
    df = pd.read_sql('SELECT * FROM vendas', con=DATABASE_URL)

    # Verificar se o DataFrame não está vazio
    assert not df.empty, "O DataFrame está vazio."

    # Verificar o schema (colunas e tipos de dados)
    expected_dtype = {
        'email': 'object',  # object em Pandas corresponde a string em SQL
        'data': 'datetime64[ns]',
        'valor': 'float64',
        'quantidade': 'int64',
        'produto': 'object',
        'categoria': 'object'
    }

    assert df.dtypes.to_dict() == expected_dtype, "O schema do DataFrame não corresponde ao esperado."