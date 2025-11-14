# Generated manually to fix ManyToMany intermediate table
# This migration fixes the intermediate table for Movie.actors ManyToManyField
# by converting movie_id and actor_id columns from bigint to uuid
#
# Strategy (for development):
# 1. Remove old constraints
# 2. Clear the intermediate table (development data can be recreated)
# 3. Remove old bigint columns
# 4. Add new uuid columns
# 5. Recreate constraints
#
# NOTE: For production, you would need to:
# 1. Create a backup of the intermediate table
# 2. Create a manual mapping table (old_bigint_id -> new_uuid)
# 3. Populate the new uuid columns using the mapping
# 4. Then execute this structural migration

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_movie_id_movie_created_at_movie_created_by_and_more'),
        ('actors', '0002_remove_actor_id_actor_created_at_actor_created_by_and_more'),
    ]

    operations = [
        # Passo 1: Remover constraints antigas
        migrations.RunSQL(
            sql="""
                ALTER TABLE movies_movie_actors
                DROP CONSTRAINT IF EXISTS movies_movie_actors_movie_id_fkey,
                DROP CONSTRAINT IF EXISTS movies_movie_actors_actor_id_fkey,
                DROP CONSTRAINT IF EXISTS movies_movie_actors_movie_id_actor_id_uniq,
                DROP CONSTRAINT IF EXISTS movies_movie_actors_pkey;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Passo 2: Limpar a tabela intermediária (dados de desenvolvimento podem ser recriados)
        migrations.RunSQL(
            sql="DELETE FROM movies_movie_actors;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Passo 3: Remover as colunas antigas (bigint)
        migrations.RunSQL(
            sql="""
                ALTER TABLE movies_movie_actors
                DROP COLUMN IF EXISTS movie_id,
                DROP COLUMN IF EXISTS actor_id;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Passo 4: Adicionar as colunas novas com tipo uuid
        migrations.RunSQL(
            sql="""
                ALTER TABLE movies_movie_actors
                ADD COLUMN movie_id uuid NOT NULL,
                ADD COLUMN actor_id uuid NOT NULL;
            """,
            reverse_sql="""
                ALTER TABLE movies_movie_actors
                DROP COLUMN IF EXISTS movie_id,
                DROP COLUMN IF EXISTS actor_id;
            """,
        ),
        # Passo 5: Recriar as constraints e índices
        migrations.RunSQL(
            sql="""
                -- Foreign Key para Movie
                ALTER TABLE movies_movie_actors
                ADD CONSTRAINT movies_movie_actors_movie_id_fkey
                FOREIGN KEY (movie_id) REFERENCES movies_movie(uuid)
                ON DELETE CASCADE;

                -- Foreign Key para Actor
                ALTER TABLE movies_movie_actors
                ADD CONSTRAINT movies_movie_actors_actor_id_fkey
                FOREIGN KEY (actor_id) REFERENCES actors_actor(uuid)
                ON DELETE CASCADE;

                -- Constraint de unicidade (evita duplicatas)
                ALTER TABLE movies_movie_actors
                ADD CONSTRAINT movies_movie_actors_movie_id_actor_id_uniq
                UNIQUE (movie_id, actor_id);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]


"""
[pt-BR]
Se o caso ocorresse com um banco de dados de produção, seria necessário:
1. Criar um backup da tabela intermediária
2. Criar uma tabela de mapeamento (old_bigint_id -> new_uuid)
3. Popular a tabela de mapeamento usando os IDs antigos
4. Executar esta migração estrutural

E esse processo seria necessário, devido a todos os models herdarem de BaseModel,
que possui o campo uuid como primary key, sendo que as tabelas já possuem o campo id como bigint e estão
populadas com dados.

Uma abordagem mais segura ao implantar o BaseModel seria:
1 - criar a coluna uuid, não como primary key, mas como unique
2 - referenciar as entidades de dados sempre com o uuid no projeto,
evitando assim problemas de compatibilidade com o banco de dados.

Documentação para fins de aprendizagem.
"""

"""
[en-US]
If this occurred in a production database, it would be necessary to:
1. Create a backup of the intermediate table
2. Create a mapping table (old_bigint_id -> new_uuid)
3. Populate the mapping table using the old IDs
4. Then execute this structural migration

And this process would be necessary, due to all models inheriting from BaseModel,
which has the uuid field as primary key, and the tables already have the id field as bigint and are populated with data.

An approach to a more secure implementation of the BaseModel would be:
1 - create the uuid column, not as primary key, but as unique
2 - reference the data entities always with the uuid in the project,
avoiding compatibility problems with the database.

Documentation for learning purposes.
"""
