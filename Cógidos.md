# 1. Transferência de dados para as recomendações do MongoDB ao Neo4j

O seguinte comando foi utilizado para transferir dados relevantes para a execução das consultas de recomendação do MongoDB para o Neo4j

```cypher

CALL apoc.periodic.iterate(
'CALL apoc.mongo.find(
  "mongodb+srv://ryanandrade:12345678ryan@cluster0.jtjptts.mongodb.net/sample_airbnb.listingsAndReviews",
  {},
  {objectIdAsMap: false, compatibleValues: true,  bsonToJson: true, 
  project: {_id: 1, amenities: 1, address: {country: 1}, reviews: {_id: 1}, 
  bedroomds: 1, price: 1}}
) YIELD value return value',

```

## O que faz?

A primeira parte do comando estabelece uma conexão com o banco do MongoDB, obtendo os documentos com os dados que serão escritos no Neo4j, sendo eles:
- Os ids dos hoteis, junto de seu preço e número de quartos
- As comodidades
- Os paises 
- Os usuários

```cypher
'
WITH value
MERGE (h:Hotel {id: value._id})
SET h.price = value.price,
    h.bedrooms = value.bedrooms

// Comodidades
WITH h, value
UNWIND value.amenities AS amenity
MERGE (a:Amenity {name: amenity})
MERGE (h)-[:HAS_AMENITY]->(a)

// País
WITH DISTINCT h, value
MERGE (c:Country {name: value.address.country})
MERGE (h)-[:IS_LOCATED]->(c)

// Reviews
WITH DISTINCT h, value
UNWIND value.reviews AS review
MERGE (u:User {id: review._id})
MERGE (u)-[:HAS_RENTED]->(h)
',
{batchSize: 100, parallel: false}
)

```

## O que faz?

O restante do comando pega os documentos obtidos pela conexão, e para cada documento, que possui os dados de um hotel, é feito o seguinte:


## Criação de nós

- Se o nó já não existe, é criado um nó com o id do hotel, seu preço e número de quartos
- Para cada comodidade que esse hotel possui, se o nó já não existe, é criado um nó com o nome da comodidade
- Se o nó já não existe, é criado um nó com o nome do país que o hotel está
- Para cada usuário que alugou esse hotel, se o nó já não existe, é criado um nó com o id do usuário


## Criação de conexões

- O nó com o id do hotel é ligado aos nós das comodidades que ele possui pela conexão `HAS_AMENITY`
- O nó com o id do hotel é ligado ao nó do país que ele está pela conexão `IS_LOCATED`
- O nó com o id do hotel é ligado aos nós dos usuários que o alugaram pela conexão `HAS_RENTED`


# 2. Criar Conexões entre Usuários e Hotéis

Este script Cypher usa `apoc.periodic.iterate` para criar novas conexões entre usuários (`User`) e hotéis (`Hotel`) no Neo4j, simulando aluguéis.

## Motivação

No banco de dados original, cada usuário tinha alugado apenas um Airbnb, o que dificultaria a criação de um sistema de recomandação.

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
