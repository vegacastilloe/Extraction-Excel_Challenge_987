# 🧠 Data Extraction -

![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Last Updated](https://img.shields.io/github/last-commit/vegacastilloe/Extraction-Excel_Challenge_987)
![Language](https://img.shields.io/badge/language-español-darkred)

#
---
- 🌟 --- CAN YOU SOLVE THIS - EXCEL CHALLENGE 987 --- 🌟
- 🌟 **Author**: Excel (Vijay A. Verma) BI




  - 🔰 Explicación del Script Línea por Línea

🔰 Este script tiene como objetivo extraer información específica de una columna de texto (`Data`) de un archivo Excel, utilizando expresiones regulares, y luego combinar la información extraída en un formato estandarizado para su comparación.

 🔗 Link to Excel file:
 👉 https://lnkd.in/gxJ-B29y

**My code in Python** 🐍 **for this challenge**

 🔗 https://github.com/vegacastilloe/Extraction-Excel_Challenge_987/blob/main/extraction-excel_challenge_987.py

---
---



### 1. Importación de Librerías

```python
import pandas as pd
import re
```
*   `import pandas as pd`: Importa la librería `pandas`, que es fundamental para el manejo y análisis de datos en DataFrames. Se le asigna el alias `pd` para facilitar su uso.
*   `import re`: Importa el módulo `re` (regular expression), necesario para trabajar con expresiones regulares para la extracción de patrones de texto.

### 2. Carga y Preparación Inicial de los Datos

```python
df_raw = pd.read_excel(input_table, header=0, sheet_name= 'Sheet1')
df_input = df_raw['Data'].dropna(how='all').copy()
```
*   `df_raw = pd.read_excel(input_table, header=0, sheet_name= 'Sheet1')`: Lee el archivo Excel desde la URL especificada en `input_table`. `header=0` indica que la primera fila es el encabezado y `sheet_name='Sheet1'` especifica la hoja a leer. Los datos se cargan en un DataFrame llamado `df_raw`.
*   `df_input = df_raw['Data'].dropna(how='all').copy()`: Selecciona la columna 'Data' de `df_raw`. `.dropna(how='all')` elimina cualquier fila donde *todos* los valores de la columna 'Data' sean nulos. `.copy()` crea una copia explícita para evitar advertencias de SettingWithCopyWarning en operaciones futuras.

### 3. Configuración de la Extracción con Expresiones Regulares

```python
extraction_config = {
    'Code': {
        'pattern': re.compile(r'(?:INV-|ORD:|SHIP:|INV=|ORD=|SHIP=|TRX:INV-)([A-Z0-9-]+)(?:[#/|$@])'),
        'converter': lambda m: m.group(1) if m else None
    },
    'Quantity': {
        'pattern': re.compile(r'[Q#](\d+(?:\.\d+)?)'),
        'converter': lambda m: float(m.group(1)) if m else None
    },
    'Value': {
        'pattern': re.compile(r'[$V](\d+\.?\d*)'),
        'converter': lambda m: float(m.group(1)) if m else None
    },
    'Status': { # MODIFIED REGEX to be more specific (after @)
        'pattern': re.compile(r'@(ACT|PEND|CMP)'),
        'converter': lambda m: m.group(1) if m else None
    },
    'Priority': { # MODIFIED REGEX to be more specific (after #P)
        'pattern': re.compile(r'#P(\d)'),
        'converter': lambda m: int(m.group(1)) if m else None
    }
}
```
*   `extraction_config`: Es un diccionario que define cómo extraer diferentes tipos de información (`Code`, `Quantity`, `Value`, `Status`, `Priority`) de la columna 'OriginalData'.
    *   Cada clave (por ejemplo, `'Code'`) tiene un diccionario anidado con:
        *   `'pattern'`: Una expresión regular compilada (`re.compile`) para buscar un patrón específico. Compilar las expresiones regulares mejora el rendimiento si se van a usar varias veces.
        *   `'converter'`: Una función `lambda` que toma el objeto `match` (resultado de `pattern.search()`) y devuelve el valor extraído (o `None` si no hay coincidencia).
    *   Las expresiones regulares están diseñadas para capturar diferentes formatos de datos (por ejemplo, `INV-`, `ORD:`, `$`, `Q#`, `@`, `#P`).

### 4. Creación del DataFrame de Resultados y Aplicación de Extracción

```python
# Create a new DataFrame from df_input to store the extracted features
df_result = pd.DataFrame(df_input).rename(columns={'Data': 'OriginalData'})

# Apply the extraction configurations
for col_name, config in extraction_config.items():
    pattern = config['pattern']
    converter = config['converter']
    df_result[col_name] = df_result['OriginalData'].apply(lambda x: converter(pattern.search(x)))
```
*   `df_result = pd.DataFrame(df_input).rename(columns={'Data': 'OriginalData'})`: Crea un nuevo DataFrame `df_result` a partir de `df_input` (que es una Serie). La columna 'Data' se renombra a 'OriginalData' para mantener el dato original y añadir las columnas extraídas.
*   El bucle `for` itera sobre cada configuración en `extraction_config`:
    *   `pattern = config['pattern']`: Obtiene la expresión regular compilada.
    *   `converter = config['converter']`: Obtiene la función de conversión.
    *   `df_result[col_name] = df_result['OriginalData'].apply(lambda x: converter(pattern.search(x)))`: Aplica la función `lambda` a cada elemento de la columna 'OriginalData'. Por cada elemento, busca el patrón definido y luego usa el `converter` para obtener el valor, que se guarda en una nueva columna (`col_name`) en `df_result`.

### 5. Funciones Auxiliares para Formateo y Combinación

```python
def format_numeric_for_join(value):
    if pd.isna(value):
        return ''
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

# MODIFIED LOGIC: Combine Status and Priority directly without a hyphen between them
def combine_row_data(row):
    code = format_numeric_for_join(row['Code'])
    quantity = format_numeric_for_join(row['Quantity'])
    value = format_numeric_for_join(row['Value'])
    status = format_numeric_for_join(row['Status'])
    priority = format_numeric_for_join(row['Priority'])

    # Combine Status and Priority directly (e.g., ACT2)
    status_priority = f"{status}{priority}"

    parts = [code, quantity, value, status_priority]
    return '-'.join(parts)
```
*   `format_numeric_for_join(value)`: Esta función auxiliar se encarga de formatear valores numéricos para que sean adecuados para la unión.
    *   Si el valor es `NaN` (no es un número), devuelve una cadena vacía.
    *   Si es un `float` que representa un número entero (por ejemplo, `72.0`), lo convierte a `int` para eliminar el `.0` antes de convertirlo a `str`.
    *   Para cualquier otro caso, lo convierte directamente a `str`.
*   `combine_row_data(row)`: Esta función toma una fila completa del DataFrame `df_result` y combina los valores extraídos en una sola cadena, utilizando el formato `Code-Quantity-Value-StatusPriority`.
    *   Usa `format_numeric_for_join` para preparar cada componente (`Code`, `Quantity`, `Value`, `Status`, `Priority`).
    *   `status_priority = f"{status}{priority}"`: Combina directamente el `Status` y `Priority` sin un guion intermedio (ejemplo: `ACT2`).
    *   `parts = [code, quantity, value, status_priority]`: Crea una lista con los componentes formateados.
    *   `return '-'.join(parts)`: Une los componentes con un guion (`-`) como separador y devuelve la cadena resultante.

### 6. Aplicación de la Combinación y Verificación

```python
df_result['CombinedExtracted'] = df_result.apply(combine_row_data, axis=1)

expected = df_raw['AnswerExpected'].dropna(how='all').copy()
print(f'Match expected: 🐍✅ #{df_result['CombinedExtracted'].equals(expected)}') #True si todo coincide ...
```
*   `df_result['CombinedExtracted'] = df_result.apply(combine_row_data, axis=1)`: Aplica la función `combine_row_data` a cada fila (`axis=1`) de `df_result` y guarda el resultado en una nueva columna llamada 'CombinedExtracted'.
*   `expected = df_raw['AnswerExpected'].dropna(how='all').copy()`: Carga la columna 'AnswerExpected' del DataFrame original `df_raw`, elimina los nulos y crea una copia. Esta columna se asume que contiene los resultados esperados.
*   `print(f'Match expected: 🐍✅ #{df_result['CombinedExtracted'].equals(expected)}')`: Compara la columna 'CombinedExtracted' generada por el script con la columna 'AnswerExpected' (los resultados esperados). `.equals()` verifica si las Series son idénticas en valores e índices. Imprime `True` si todas las filas coinciden, `False` en caso contrario, indicando si la extracción y combinación fueron exitosas.


## 📦 Requisitos

- Python 3.9+
- Paquetes:
- pandas openpyxl (para leer .xlsx)
- Archivo Excel con al menos:
    - La columna: `Data`.
    - En la columna `AnswerExpected` : resultados esperados para comparación

---

## 🚀 Cómo funciona

- Lee un archivo Excel desde una URL o ruta local.
- Limpia columnas vacías y espacios en los encabezados.
- Aplica una transformación regex.
- Compara el resultado con una columna de respuestas.

---

## 📤 Salida

El script imprime : # True si al comparar df_result contra expected.
---

## 🧹 Output:

`Match expected: 🐍✅ #True`

---

## 🛠️ Personalización

Puedes adaptar el script para:

- Aplicar reglas más complejas
- Exportar el resultado a Excel o CSV

---

## 🚀 Ejecución

```python
import pandas as pd
import re

df_raw = pd.read_excel(input_table, header=0, sheet_name= 'Sheet1')
df_input = df_raw['Data'].dropna(how='all').copy()

extraction_config = {
    'Code': {
        'pattern': re.compile(r'(?:INV-|ORD:|SHIP:|INV=|ORD=|SHIP=|TRX:INV-)([A-Z0-9-]+)(?:[#/|$@])'),
        'converter': lambda m: m.group(1) if m else None
    },
    'Quantity': {
        'pattern': re.compile(r'[Q#](\d+(?:\.\d+)?)'),
        'converter': lambda m: float(m.group(1)) if m else None
    },
    'Value': {
        'pattern': re.compile(r'[$V](\d+\.?\d*)'),
        'converter': lambda m: float(m.group(1)) if m else None
    },
    'Status': { # MODIFIED REGEX to be more specific (after @)
        'pattern': re.compile(r'@(ACT|PEND|CMP)'),
        'converter': lambda m: m.group(1) if m else None
    },
    'Priority': { # MODIFIED REGEX to be more specific (after #P)
        'pattern': re.compile(r'#P(\d)'),
        'converter': lambda m: int(m.group(1)) if m else None
    }
}

# Create a new DataFrame from df_input to store the extracted features
df_result = pd.DataFrame(df_input).rename(columns={'Data': 'OriginalData'})

# Apply the extraction configurations
for col_name, config in extraction_config.items():
    pattern = config['pattern']
    converter = config['converter']
    df_result[col_name] = df_result['OriginalData'].apply(lambda x: converter(pattern.search(x)))

def format_numeric_for_join(value):
    if pd.isna(value):
        return ''
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

# MODIFIED LOGIC: Combine Status and Priority directly without a hyphen between them
def combine_row_data(row):
    code = format_numeric_for_join(row['Code'])
    quantity = format_numeric_for_join(row['Quantity'])
    value = format_numeric_for_join(row['Value'])
    status = format_numeric_for_join(row['Status'])
    priority = format_numeric_for_join(row['Priority'])

    # Combine Status and Priority directly (e.g., ACT2)
    status_priority = f"{status}{priority}"

    parts = [code, quantity, value, status_priority]
    return '-'.join(parts)

df_result['CombinedExtracted'] = df_result.apply(combine_row_data, axis=1)

expected = df_raw['AnswerExpected'].dropna(how='all').copy()
print(f'Match expected: 🐍✅ #{df_result['CombinedExtracted'].equals(expected)}') #True si todo coincide ...
```

### 💾 Exportación opcional
```python
# # df_result.to_excel("extraction_output.xlsx", index=False)
```
---
### 📄 Licencia
---
Este proyecto está bajo ![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg). Puedes usarlo, modificarlo y distribuirlo libremente.

---

