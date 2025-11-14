# Formato do CSV para Importação de Atores

## Estrutura do Arquivo CSV

O arquivo CSV deve ter as seguintes colunas no cabeçalho:

```csv
name,birthday,nationality
```

## Descrição das Colunas

### 1. `name` (OBRIGATÓRIO)
- **Tipo**: String
- **Descrição**: Nome completo do ator
- **Tamanho máximo**: 200 caracteres
- **Exemplo**: `"Leonardo DiCaprio"`

### 2. `birthday` (OBRIGATÓRIO)
- **Tipo**: Data no formato `YYYY-MM-DD`
- **Descrição**: Data de nascimento do ator
- **Formato**: `YYYY-MM-DD` (ex: `1974-11-11`)
- **Exemplo**: `1974-11-11`, `1929-10-16`

### 3. `nationality` (OBRIGATÓRIO)
- **Tipo**: String (código de nacionalidade)
- **Descrição**: Nacionalidade do ator
- **Valores aceitos**:
  - `USA` - United States of America
  - `BRA` - Brazil
- **Exemplo**: `USA`, `BRA`
- **Importante**: O valor deve corresponder exatamente às opções disponíveis (maiúsculas)

## Exemplo Completo de CSV

```csv
name,birthday,nationality
Leonardo DiCaprio,1974-11-11,USA
Fernanda Montenegro,1929-10-16,BRA
Tom Hanks,1956-07-09,USA
Wagner Moura,1976-06-27,BRA
Meryl Streep,1949-06-22,USA
Robert De Niro,1943-08-17,USA
Al Pacino,1940-04-25,USA
Denzel Washington,1954-12-28,USA
Morgan Freeman,1937-06-01,USA
Samuel L. Jackson,1948-12-21,USA
```

## Comando para Importar

```bash
# Localmente
python manage.py import_actors arquivo.csv

# Com Docker
docker compose exec flix_web python manage.py import_actors arquivo.csv
```

## Validações Aplicadas

1. **Nome**: Obrigatório, não pode estar vazio
2. **Data de nascimento**:
   - Formato obrigatório: `YYYY-MM-DD`
   - Deve ser uma data válida
3. **Nacionalidade**:
   - Obrigatória
   - Deve ser exatamente `USA` ou `BRA` (maiúsculas)

## Observações Importantes

- O arquivo deve estar codificado em **UTF-8**
- A primeira linha deve conter os cabeçalhos: `name,birthday,nationality`
- A data deve estar no formato `YYYY-MM-DD` (ano-mês-dia)
- A nacionalidade deve ser exatamente `USA` ou `BRA` (maiúsculas)
- Use aspas duplas (`"`) se o nome contiver vírgulas

## Exemplo de Uso

```bash
# Criar arquivo CSV
cat > actors.csv << EOF
name,birthday,nationality
Leonardo DiCaprio,1974-11-11,USA
Fernanda Montenegro,1929-10-16,BRA
Tom Hanks,1956-07-09,USA
EOF

# Importar
python manage.py import_actors actors.csv
```
