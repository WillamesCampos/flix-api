# Formato do CSV para Importação de Filmes

## Estrutura do Arquivo CSV

O arquivo CSV deve ter as seguintes colunas no cabeçalho:

```csv
title,genre,release_date,actors,resume
```

## Descrição das Colunas

### 1. `title` (OBRIGATÓRIO)
- **Tipo**: String
- **Descrição**: Título do filme
- **Tamanho máximo**: 500 caracteres
- **Exemplo**: `"O Poderoso Chefão"`

### 2. `genre` (OBRIGATÓRIO)
- **Tipo**: String (nome do gênero)
- **Descrição**: Nome do gênero do filme. O gênero **deve existir** no banco de dados antes da importação
- **Exemplo**: `"Drama"`, `"Ação"`, `"Comédia"`, `"Crime"`, `"Ficção Científica"`
- **Importante**: O gênero será buscado pelo nome exato. Se não existir, o filme será ignorado.

### 3. `release_date` (OPCIONAL)
- **Tipo**: Data no formato `YYYY-MM-DD`
- **Descrição**: Data de lançamento do filme
- **Formato**: `YYYY-MM-DD` (ex: `1972-03-24`)
- **Validação**: Ano deve ser >= 1900
- **Exemplo**: `1972-03-24`, `2023-12-15`
- **Pode ser deixado vazio**: Sim

### 4. `actors` (OPCIONAL)
- **Tipo**: String (nomes separados por vírgula)
- **Descrição**: Lista de nomes dos atores separados por vírgula
- **Formato**: `"Nome1, Nome2, Nome3"`
- **Importante**: Os atores **devem existir** no banco de dados antes da importação. Atores não encontrados serão ignorados (mas o filme será criado)
- **Exemplo**: `"Marlon Brando, Al Pacino, James Caan"`
- **Pode ser deixado vazio**: Sim

### 5. `resume` (OPCIONAL)
- **Tipo**: String (texto)
- **Descrição**: Sinopse/resumo do filme
- **Tamanho máximo**: 500 caracteres
- **Exemplo**: `"A história da família Corleone, uma das mais poderosas famílias do crime organizado."`
- **Pode ser deixado vazio**: Sim

## Exemplo Completo de CSV

```csv
title,genre,release_date,actors,resume
O Poderoso Chefão,Crime,1972-03-24,"Marlon Brando, Al Pacino, James Caan","A história da família Corleone, uma das mais poderosas famílias do crime organizado."
Pulp Fiction,Crime,1994-10-14,"John Travolta, Samuel L. Jackson, Uma Thurman","A vida de dois assassinos, um boxeador e outros personagens se entrelaça em Los Angeles."
Matrix,Ficção Científica,1999-03-31,"Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss","Um programador descobre que a realidade é uma simulação."
Cidade de Deus,Crime,2002-08-30,"Alexandre Rodrigues, Leandro Firmino, Phellipe Haagensen","A história de dois jovens que crescem na favela da Cidade de Deus no Rio de Janeiro."
Tropa de Elite,Ação,2007-10-05,"Wagner Moura, Caio Junqueira, André Ramiro","A rotina de um capitão da BOPE durante a preparação para a Copa do Mundo."
```

## Exemplo com Campos Opcionais Vazios

```csv
title,genre,release_date,actors,resume
Filme Sem Data,Drama,,,
Filme Sem Atores,Ação,2020-01-01,,
Filme Completo,Comédia,2015-06-15,"Will Smith, Martin Lawrence","Dois policiais se infiltram em uma escola."
```

## Comando para Importar

```bash
# Localmente
python manage.py import_movies arquivo.csv

# Com Docker
docker compose exec flix_web python manage.py import_movies arquivo.csv
```

## Validações Aplicadas

1. **Título**: Obrigatório, não pode estar vazio
2. **Gênero**:
   - Obrigatório
   - Deve existir no banco de dados (busca pelo nome exato)
3. **Data de lançamento**:
   - Formato: `YYYY-MM-DD`
   - Ano mínimo: 1900
4. **Resumo**: Máximo de 500 caracteres
5. **Atores**: Devem existir no banco de dados (nomes exatos). Atores não encontrados são ignorados, mas o filme é criado.

## Ordem Recomendada de Importação

1. **Primeiro**: Importar gêneros (se ainda não foram importados)
2. **Segundo**: Importar atores (se ainda não foram importados)
3. **Terceiro**: Importar filmes

## Observações Importantes

- O arquivo deve estar codificado em **UTF-8**
- A primeira linha deve conter os cabeçalhos: `title,genre,release_date,actors,resume`
- Use aspas duplas (`"`) para campos que contenham vírgulas (como lista de atores ou resumo)
- Certifique-se de que os nomes de gêneros e atores correspondem exatamente aos cadastrados no banco
- O comando mostra um resumo ao final com:
  - Quantidade de filmes criados
  - Quantidade de filmes ignorados
  - Lista de erros encontrados

## Exemplo de Uso

```bash
# Criar arquivo CSV
cat > movies.csv << EOF
title,genre,release_date,actors,resume
O Poderoso Chefão,Crime,1972-03-24,"Marlon Brando, Al Pacino, James Caan","A história da família Corleone."
Matrix,Ficção Científica,1999-03-31,"Keanu Reeves, Laurence Fishburne","Um programador descobre que a realidade é uma simulação."
EOF

# Importar
python manage.py import_movies movies.csv
```
