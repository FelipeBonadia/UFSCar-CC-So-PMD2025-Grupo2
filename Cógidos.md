# Criar Conexões entre Usuários e Hotéis

Este script Cypher usa `apoc.periodic.iterate` para criar novas conexões entre usuários (`User`) e hotéis (`Hotel`) no Neo4j, simulando aluguéis.

## Motivações

No banco de dados original, cada usuário tinha alugado apenas um aribnb, o que dificultaria a criação de um sistema de recomandação.

## O que ele faz

Para cada usuário:
- Encontra hotéis que ele ainda não alugou.
- Sorteia 2 hotéis aleatórios dessa lista.
- Cria a relação `HAS_RENTED` com esses hotéis.

## Script

```cypher
CALL apoc.periodic.iterate(
  "
    MATCH (u:User)
    RETURN u
  ",
  "
    MATCH (h:Hotel)
    WHERE NOT (u)-[:HAS_RENTED]->(h)
    WITH u, collect(h) AS hoteisDisponiveis
    WITH u, apoc.coll.randomItems(hoteisDisponiveis, 2, false) AS hoteisSorteados
    UNWIND hoteisSorteados AS hotel
    MERGE (u)-[:HAS_RENTED]->(hotel)
  ",
  {batchSize: 100, parallel: false}
)
```
