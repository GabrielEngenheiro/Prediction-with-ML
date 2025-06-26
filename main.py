# Upload do Excel (Colab)
#planilha disponivel em: https://drive.google.com/drive/u/1/folders/1ezyz7ApC5PnXDbfgmxavJw0A9Yh1NuUH
# Nome do arquivo da planilha "Prencher_Planilha_ML_Produtividade.xlsx" 
from google.colab import files
uploaded = files.upload()

# Instalar openpyxl (se necessário)
!pip install openpyxl --quiet

# Importar bibliotecas
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Ler o arquivo Excel
nome_arquivo = next(iter(uploaded))
df = pd.read_excel(io.BytesIO(uploaded[nome_arquivo]))

# Verificar colunas
print("Colunas encontradas:", df.columns.tolist())

# Filtrar apenas as linhas com médias (a cada 123ª linha)
intervalo = 123
linhas_medias = list(range(intervalo - 1, len(df), intervalo))
df_medias = df.iloc[linhas_medias].reset_index(drop=True)

# Remover a coluna 'data' se presente
if 'data' in df_medias.columns:
    df_medias = df_medias.drop(columns=['data'])

# Separar X (dados climáticos) e y (produtividade)
X = df_medias.drop(columns=['Produtividade_kg_ha'])
y = df_medias['Produtividade_kg_ha']

# Treinar o modelo Random Forest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

y_pred = modelo_rf.predict(X_test)
