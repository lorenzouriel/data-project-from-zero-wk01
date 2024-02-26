import pandas as pd
from contrato import Vendas
from dotenv import load_dotenv

load_dotenv(".env")

POSTGRES_USER='dbnameworkshop_hlyr_user'
POSTGRES_PASSWORD='BeYZh0z3NPo6mvI9IONBfXFAi9pHyxYd'
POSTGRES_HOST='dpg-cncvv9acn0vc73f4dp7g-a.oregon-postgres.render.com'
POSTGRES_PORT=5432
POSTGRES_DB='dbnameworkshop_hlyr'

# Cria a URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def process_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        errors = []

        # Verificar se há colunas extras no DataFrame
        extra_cols = set(df.columns) - set(Vendas.model_fields.keys())
        if extra_cols:
            return False, f"Colunas extras detectadas no Excell: {', '.join(extra_cols)}"
        
        # Validar cada linha com o schema escolhido
        for index, row in df.iterrows():
            try:
                _ = Vendas(**row.to_dict())
            except Exception as e:
                errors.append(f"Erro na linha {index + 2}: {e}")
            
        return df, True, errors
    
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def excel_to_sql(df):
    df.to_sql('vendas', con=DATABASE_URL, if_exists='replace', index=False)