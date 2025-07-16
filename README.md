
# Projeto Prático – Sistema de Recomendação para Hospedagens no Airbnb

## Universidade Federal de São Carlos


**Grupo:** 2

**Integrantes:**  
- Felipe Bonadia Bravo - 813908
- Laura Rieko Marçal Imai - 813451
- Ryan De Melo Andrade - 812899


**Disciplina:** Processamento Massivo de Dados

**Professora:** Profa. Dra. Sahudy Montenegro González

---

## Resumo 
Este projeto apresenta o desenvolvimento de um sistema de recomendação de hospedagens na plataforma Airbnb, baseado em um modelo híbrido de banco de dados, que integra MongoDB (documentos) e Neo4j (grafos). O objetivo principal é sugerir acomodações personalizadas aos usuários com base em seu histórico de reservas, considerando atributos como número de quartos, faixa de preço e comodidades presentes.

O MongoDB é usado para armazenar os dados dos hotéis, enquanto o Neo4j modela os relacionamentos entre usuários, acomodações, localização e avaliações. A integração entre os dois bancos é feita por meio da biblioteca APOC, permitindo a transformação dos dados em grafos.

A arquitetura proposta permite identificar padrões de preferência do usuário e realizar recomendações eficientes com base em similaridade. O sistema prioriza acomodações que compartilham características frequentes no histórico do usuário, como número de quartos e comodidades mais recorrentes, tudo isso, com base na localização que o usuário insere para a sua próxima hospedagem.

Este trabalho evidencia a aplicabilidade de tecnologias NoSQL em soluções práticas e escaláveis, demonstrando como a combinação de documentos e grafos pode potencializar sistemas de recomendação inteligentes.

## Definição do tema
O tema que iremos explorar no desenvolvimento do trabalho é o “Sistema de Recomendação para Hospedagens Airbnb”, feito com base em um banco de dados híbrido - de Documentos e Grafos. Nessa senda, visa-se modelar e analisar dados sobre hotéis, suas comodidades, localizações, preços, dentre outros atributos, com objetivo de fornecer recomendações personalizadas baseado nas preferências demonstradas pelo histórico do usuário.

---

## Introdução ao tema
Com a popularização das plataformas de hospedagem como o Airbnb, a possibilidade de oferecer recomendações “personalizadas” aos usuários é um diferencial, que melhora a experiência deste. Nesse contexto, um sistema de recomendação desempenha um papel fundamental para auxiliar na seleção de acomodações que atendem aos requisitos e necessidades específicas com base em um histórico.

Para o projeto em específico, propomos um modelo híbrido de banco de dados, que integra dois paradigmas: Documentos e Grafos. As informações estruturadas e descritivas acerca dos hotéis, como nome, descrição, número de quartos e preços serão armazenadas em Documentos, à medida que relacionamentos entre as hospedagens, suas comodidades oferecidas, localizações e avaliações de usuário serão representadas em Grafo, facilitando, assim, uma análise mais eficiente dessas conexões complexas. Desse modo, os dados armazenados em documentos possibilitam consultas detalhadas sobre atributos específicos dos hotéis, ao passo que os dados em grafos permitem identificar, de forma mais rápida, hospedagens que, por exemplo, possuem características semelhantes de comodidade ou localização, visto que, no banco de grafos, as relações entre os dados são parte central da estrutura, e podem ser consultadas e navegadas eficientemente.
Com isso em mente, a proposta do sistema de recomendação está pautada em dois principais requisitos de negócio: sugerir hotéis com comodidades similares àquelas dos hotéis que o usuário já alugou anteriormente; e sugerir hotéis com quantidades de quartos e faixa de preço semelhantes às adotadas pelo histórico de usuário.

Para isso, utilizaremos o conjunto de dados obtido pelo próprio site do MongoDB, sendo esses a amostra do conjunto de dados de listagens AirBnB, que possui detalhes sobre cerca de 5.500 anúncios da rede de hotéis do AirBnB.
Desse modo, o projeto propõe uma aplicação prática de tecnologias NoSQL, ao mesmo tempo em que evidencia como a análise de dados pode contribuir para a personalização e aprimoramento de serviços de hospedagem.

---

## Objetivos

O programa tem como objetivo oferecer um sistema de recomendação de hotéis Airbnb baseado nas preferências demonstradas pelo histórico do usuário. Para ser mais específico, baseado nas avaliações anteriores do usuário, será identificado os hotéis que ele alugou no passado. A partir disso, serão analisadas as características desses hotéis, como seu número de quartos e comodidades oferecidas, o que oferecerá um padrão de preferências desse usuário, que servirá como base para a recomendação de novos hotéis após designada uma localização. Desse modo, será possível implementar um sistema baseado nas preferências de usuários, com apoio de tecnologias NoSQL para representar, de modo eficiente tanto os dados descritivos, quanto os seus relacionamentos.

Em primeira análise, destaca-se como eixo a ser explorado pela aplicação a análise de preferências do usuário, sendo esta composta pela identificação, por meio do histórico de reservas do usuários, dos atributos mais comuns das hospedagens escolhidas - como número de quartos e faixa de preço -, além da detecção de comodidades mais recorrentes nessas hospedagens anteriores.
 
Em segunda análise, deve-se compreender o eixo de recomendações baseadas em similaridade, ou seja, sugerir hospedagens com perfil similar, no que diz respeito a atributos e comodidades, às preferências passadas, possibilitando, em consonância a isso, uma filtragem por localização para refinar os resultados.

---

## Modelagem

### Tecnologias escolhidas

Para o desenvolvimento do trabalho, serão usados os modelos noSQL MongoDB e Neo4j, com a integração entre eles sendo realizada por meio dos procedimentos da biblioteca apoc.

Adentrando mais na escolha de tecnologias, considerou-se os requisitos de desempenho, flexibilidade, estrutura de dados e facilidade de integração entre estas. Nesse cenário, tem-se que o MongoDB foi escolhido, tendo em vista a facilidade em utilizá-lo para consultas rápidas, sobre hospedagens específicas, além da possibilidade de encapsulamento das informações em um único registro - um documento JSON. Com relação à decisão de uso do Neo4j, como modelo orientado a grafos, tem-se a modelagem natural de conexões, no caso relacionamentos, que é interessante para o projeto e será melhor abordada no tópico de decisões de projeto.
 
Em consonância com as tecnologias escolhidas, optou-se pela integração feita por meio da biblioteca APOC (Awesome Procedures On Cypher), que será utilizada para importar os dados do MongoDB diretamente para o Neo4j, fato que facilitará a migração e transformação “automática” dos dados em formato de documento, para grafos.

---
### Decisões de projeto

A escolha do uso de um banco de dados orientado a grafos, para armazenar as informações relevantes para a recomendação de hotéis, deve-se ao fato dele ser substancialmente mais eficiente para essa funcionalidade, quando comparado a outros modelos de banco de dados, pois:
As relações são o foco, o que é o caso para o sistema de recomendação proposto, que considera as relações que os hotéis possuem com as suas comodidades, localizações e avaliações; 

Possui menos custos com junções, uma vez que - no SQL, por exemplo - seriam necessários múltiplos joins de diferentes tabelas (no caso, usuário, avaliação, hotel, comodidades), o que degradaria a performance, enquanto em grafos, a mesma lógica se resume a percorrer arestas, tendo, desse modo, custo constante;
Lida naturalmente com dados conectados, sem duplicação, nem agregações complexas, já que no cenário abordado pelo projeto, caso o conjunto de dados fosse mantido integralmente no MongoDB, onde se origina a priori, seriam necessárias diversas agregações para realizar um sistema de recomendação, e cada comodidade, que é padronizada, poderia estar duplicada em diferentes arquivos de hotéis. 

Acerca de como os dados presentes no grafo vão ser organizados, que são as comodidades dos hotéis, as reviews dos usuários, os próprios hotéis e os países que estão disponíveis, todos eles se tornarão nós, dos quais haverão ligações (arestas) que indicam:
- Que um hotel possui uma comodidade, quando um hotel é ligado a uma comodidade;
- Que um hotel está em um determinado país, quando um hotel é ligado a um país;
- Que um usuário avaliou e se hospedou em um hotel, quando um hotel é ligado a uma avaliação.

---

### Arquitetura e fluxo de dados

![Exemplo de Imagem](Fluxograma.png)

A arquitetura do sistema de recomendação segue uma estrutura modular, com etapas bem definidas para ingestão, transformação, armazenamento e análise dos dados.

Com relação ao fluxo de dados, pode-se inferir que o processo se inicia com a coleta de dados de hospedagem, que estão armazenados no MongoDB, contendo várias informações, como nome, quartos, preços, comodidades e avaliações. Posteriormente, será realizada a importação e o pré-processamento dos dados, garantindo que os atributos desejados sejam considerados na análise. Com essa etapa concluída, extraímos os atributos principais, como as comodidades, países, dentre outros.

Em seguida, deve-se realizar o envio dos dados processados para o Neo4j, aproveitado-se da biblioteca APOC, permitindo que a criação dos grafos seja concluída com sucesso, sendo que nele estarão presentes nós dos tipos: Hotel, Comodidade, Localização, Avaliações/usuários - e arestas dos tipo: POSSUI, ESTA, AVALIOU. Após isso, o usuário entra com o ID para receber as recomendações personalizadas, o sistema realiza uma consulta para identificar as hospedagens que já foram alugadas pelo usuário, analisando, desse modo, os padrões de preferência do usuário, no que diz respeito à prioridade de comodidades, preços e quartos por exemplo. 

Esses padrões são usados para gerar um perfil do usuário baseado em seu histórico, com o perfil gerado, o sistema consulta o grafo por hospedagens que possuem similaridade com as preferências. Por fim, é apresentada ao usuário uma lista personalizada de hotéis recomendados, com base nas similaridades encontradas. 

---

### Sobre o uso do programa

Para ilustrar o funcionamento do sistema de recomendações proposto, considere o caso de um usuário que já alugou três acomodações no Airbnb. Todas elas possuíam dois quartos. As comodidades oferecidas por cada uma foram as seguintes:
- Acomodação 1: Wi-Fi, ar-condicionado, cozinha, extintor de incêndio, geladeira e micro-ondas.
- Acomodação 2: Wi-Fi, cozinha, cafeteira, máquina de lavar, TV e geladeira.
- Acomodação 3: Wi-Fi, garagem, cozinha, aquecedor, geladeira e forno.

Com base nesse histórico, o sistema identifica padrões de preferência do usuário. Neste exemplo, destaca-se a recorrência de acomodações com dois quartos, além das comodidades Wi-Fi, cozinha e geladeira, presentes em todas as estadias anteriores. Assim, ao recomendar novas opções, o programa prioriza aquelas que compartilham essas características, oferecendo sugestões mais alinhadas ao perfil e às preferências do usuário.



# Desenvolvimento

## Descrição

Aplicação Flask que recomenda hotéis com base em preferências anteriores do usuário, utilizando MongoDB e Neo4j.


## Transferência de dados para as recomendações do MongoDB ao Neo4j

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

**O que faz?**

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

**O que faz?**

O restante do comando pega os documentos obtidos pela conexão, e para cada documento, que possui os dados de um hotel, é feito o seguinte:


**Criação de nós**

- Se o nó já não existe, é criado um nó com o id do hotel, seu preço e número de quartos
- Para cada comodidade que esse hotel possui, se o nó já não existe, é criado um nó com o nome da comodidade
- Se o nó já não existe, é criado um nó com o nome do país que o hotel está
- Para cada usuário que alugou esse hotel, se o nó já não existe, é criado um nó com o id do usuário


**Criação de conexões**

- O nó com o id do hotel é ligado aos nós das comodidades que ele possui pela conexão `HAS_AMENITY`
- O nó com o id do hotel é ligado ao nó do país que ele está pela conexão `IS_LOCATED`
- O nó com o id do hotel é ligado aos nós dos usuários que o alugaram pela conexão `HAS_RENTED`



## Criação de Conexões entre Usuários e Hotéis

A fim do desenvolvimento do trabalho, este script Cypher cria novas conexões entre usuários (`User`) e hotéis (`Hotel`) no Neo4j, simulando aluguéis.

**Motivação**

No banco de dados original, cada usuário tinha alugado apenas um Airbnb, o que dificultaria a criação de um sistema de recomendação. 

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

**O que ele faz**

Para cada usuário:
- Encontra hotéis que ele ainda não alugou.
- Sorteia hotéis aleatórios dessa lista.
- Cria a relação `HAS_RENTED` com esses hotéis.


## Como Executar

```bash
pip install flask pymongo neo4j
python app.py
```

## Conexões com Banco de Dados

O sistema conecta-se a dois bancos:
- **MongoDB**: onde armazena e consulta as recomendações geradas;
- **Neo4j**: responsável por processar recomendações com base em similaridade de preferências de usuários e hotéis.

As conexões são feitas no início do script. Caso falhem, são capturadas e informadas no terminal.

## Entrada do Usuário

O usuário fornece:
1. Seu ID (`userId`);
2. O número do país desejado para receber recomendações.

Essas entradas personalizam a consulta Cypher executada no Neo4j.

## Geração ou Recuperação de Recomendação

- O sistema verifica se já existem recomendações salvas para esse usuário + país no MongoDB.
- Se **existirem**, os dados são recuperados do banco.
- Caso contrário, é executada uma **consulta Cypher elaborada** no Neo4j, baseada em:
  - comodidades preferidas,
  - número de quartos,
  - preço médio histórico,
  - similaridade entre hotéis não visitados.

Os resultados são salvos no MongoDB para reutilização.

## Exibição via Flask

O Flask exibe as recomendações no navegador, carregando:
- Nome do hotel,
- Preço,
- Número de quartos,
- Nota média,
- Nome do host,
- Imagem.

Tudo é renderizado usando o template `index2.html`.

## Sobre a Consulta de Recomendação

### Análise das Comodidades do Usuário no Cypher

```cypher
MATCH (u:User {id: "xxxxxx" })-[:HAS_RENTED]->(rentedHotel:Hotel)-[:HAS_AMENITY]->(amenity:Amenity)
WITH u, amenity, COUNT(amenity) as amenityFrequency
WITH u, COLLECT({amenity: amenity, frequency: amenityFrequency}) as userAmenityFrequencies,
     SUM(amenityFrequency) as totalAmenityCount
```
<sub>Exemplo de id válido: 221244427</sub>

**O que faz?**
  - Encontrar todos os hotéis alugados pelo usuário e suas respectivas comodidades.
  - Contar quantas vezes cada comodidade aparece.
  - Calcular a frequência de cada comodidade para o usuário, criando uma lista.
  - Calcular o total de comodidades para o usuário.
  
**Exemplo**: Se o usuário alugou 3 hotéis, 3 vezes com Wi-Fi e 1 vez com piscina, a lista será:
  - `userAmenityFrequencies = [{amenity: "Wi-Fi", frequency: 3}, {amenity: "Pool", frequency: 1}]` 
  - `totalAmenityCount = 4`

### Determinação do Número de Quartos Preferido do Usuário

```cypher
MATCH (u)-[:HAS_RENTED]->(rentedHotel:Hotel)
WITH u, userAmenityFrequencies, totalAmenityCount,
     COLLECT(rentedHotel.bedrooms) as bedroomHistory
UNWIND bedroomHistory as bedroom
WITH u, userAmenityFrequencies, totalAmenityCount,
     bedroom, COUNT(bedroom) as frequency
ORDER BY frequency DESC
WITH u, userAmenityFrequencies, totalAmenityCount,
     COLLECT(bedroom)[0] as preferredBedrooms
```
**O que faz?**
  - Conta quantas vezes cada número de quartos aparece no histórico.
  - Ordena de forma descendente pela frequência de número de quartos.
  - Seleciona a moda (número de quartos mais frequente) como a preferência do usuário.
  
**Exemplo**: Se o usuário alugou 5 hotéis, 3 deles com 1 quarto e 1 com 7 quartos e 1 com 3 quartos, a a preferência será por hotéis com apenas 1 quarto.

### Histórico de Preços Baseado nos Quartos Preferidos

```cypher
MATCH (u)-[:HAS_RENTED]->(rentedHotel:Hotel)
WHERE rentedHotel.bedrooms = preferredBedrooms
WITH u, userAmenityFrequencies, totalAmenityCount, preferredBedrooms,
     AVG(rentedHotel.price) as avgPrice,
     MIN(rentedHotel.price) as minPrice,
     MAX(rentedHotel.price) as maxPrice
```
**O que faz?**
  - Calcula estatísticas de preço **apenas** dos hotéis que têm a quantidade de quartos preferida pelo usuário.
  - Calcula o preço médio, mínimo e máximo dos hotéis com o número de quartos preferido.

  
**Exemplo**: Se o usuário prefere hotéis de 2 quartos e alugou:
  - Hotel A: 1 quarto, $100 → **Ignorado no cálculo**
  - Hotel B: 2 quartos, $200 → **Incluído**
  - Hotel C: 2 quartos, $300 → **Incluído**
  - Hotel D: 3 quartos, $400 → **Ignorado no cálculo**
  
**avgPrice** = $250 (média apenas dos hotéis de 2 quartos)

### Seleção de Hotéis Candidatos

```cypher
MATCH (country:Country {name: "xxxxxx"})<-[:IS_LOCATED]-(hotel:Hotel)
// WHERE NOT EXISTS((u)-[:HAS_RENTED]->(hotel))
OPTIONAL MATCH (hotel)-[:HAS_AMENITY]->(hotelAmenity:Amenity)
WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
     hotel, COLLECT(DISTINCT hotelAmenity) as hotelAmenities
```

<sub>Exemplo de país válido: Brazil</sub>


**O que faz?**
  - Encontra hotéis na localização escolhida.
  - Coleta as comodidades presentes nessas hospedagens.
  
### Score das Comodidades

```cypher
WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
     hotel, hotelAmenities,
     [amenityFreq IN userAmenityFrequencies 
      WHERE amenityFreq.amenity IN hotelAmenities | 
      toFloat(amenityFreq.frequency) / toFloat(totalAmenityCount)] as matchingWeights
WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
     hotel, hotelAmenities, matchingWeights,
     CASE 
       WHEN SIZE(matchingWeights) = 0 THEN 0.0
       ELSE REDUCE(sum = 0.0, weight IN matchingWeights | sum + weight)
     END as weightedAmenityScore
```
**O que faz?**
  - Analisa quais são as comodidades do hotel que coincidem com as do histórico do usuário, calculando o peso normalizado dela.
  - Soma todos os pesos das comodidades comuns.
  - Caso a comodidade não esteja entre as comuns, atribui-se peso 0.


**Exemplo**: O usuário alugou hotéis com as seguintes comodidades:
  - Piscina: 1 vezes
  - Wi-Fi: 3 vezes
  - Total de ocorrências: 4

&nbsp;&nbsp;&nbsp;&nbsp; Aqui, temos então os pesos normalizados dessas comodidades:
  - Piscina: 1/4 = 0.25 = 25%
  - Wi-Fi: 3/4 = 0.75 = 75%

&nbsp;&nbsp;&nbsp;&nbsp;Caso a hospedagem tenha comodidas "extras", como "Academia" e "Café da manhã", além das citadas acima, temos o seguinte cálculo:
  - Comodidades Comuns: Piscina, Wi-Fi: 100% (25% + 75%)
  - Comodidades Extras: Academia, Café da manhã: 0% (0% + 0%)
  - Score: 100%

&nbsp;&nbsp;&nbsp;&nbsp;Caso a hospedagem tenha comodidas "extras", como "Academia" e "Café da manhã", juntamente com a "Wi-Fi", temos o seguinte cálculo:
  - Comodidades Comuns: Wi-Fi: 75%
  - Comodidades Extras: Academia, Café da manhã: 0% (0% + 0%)
  - Score: 75%


### Score dos Quartos

```cypher
WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
     hotel, weightedAmenityScore,
     CASE 
       WHEN hotel.bedrooms = preferredBedrooms THEN 1.0
       WHEN ABS(hotel.bedrooms - preferredBedrooms) = 1 THEN 0.7
       WHEN ABS(hotel.bedrooms - preferredBedrooms) = 2 THEN 0.4
       ELSE 0.2
     END as bedroomScore
```
**O que faz?**
  - Score máximo (1) caso o número de quartos seja igual ao da preferência.
  - Score 0.7 para uma diferença modular de 1; bem como score de 0.4 para diferença modular de 2 quartos.
  - Demais casos, com diferença absoluta superior, atribui-se Score mínimo (0.2).

> ❗ **Nota:** Os pesos podem ser redefinidos, basta alterá-los no código, também é possível acrescentar pesos específicos para mais diferenças, de modo a penalizar menos a variação (distância) entre a quantidade de quartos preferida e a disponível na hospedagem.

### Score do Preço

```cypher
WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
     hotel, weightedAmenityScore, bedroomScore,
     CASE 
       WHEN maxPrice = minPrice THEN 1.0
       ELSE 1 - (ABS(hotel.price - avgPrice) / (maxPrice - minPrice))
     END as priceScore
```
**O que faz?**
  - Caso todos os hotéis tenham o mesmo preço, atribui-se Score máximo (1).
  - Senão, calcula-se o quão próximo o preço do hotel está, com relação à média de preços alugados do usuário.
  - **IMPORTANTE**: Agora usa a faixa de preços baseada **apenas nos hotéis com a quantidade de quartos preferida** para normalizar.

**Exemplo**: 

Histórico de Preços dos Hotéis com Quartos Preferidos (2 quartos):

| Hotel   | Quartos | Preço (\$) | Incluído no Cálculo |
| ------- | ------- | ---------- | ------------------- |
| Hotel A | 1       | 100        | ❌ Não               |
| Hotel B | 2       | 200        | ✅ Sim               |
| Hotel C | 2       | 150        | ✅ Sim               |
| Hotel D | 2       | 250        | ✅ Sim               |
| Hotel E | 3       | 400        | ❌ Não               |

Cálculos Baseados no Histórico (apenas hotéis de 2 quartos):

- **avgPrice** = (200 + 150 + 250) / 3 = **$200**
- **minPrice** = **$150**
- **maxPrice** = **$250**
- **Faixa de Preços** = 250 - 150 = **$100**

Cálculo do `priceScore`:

Fórmula:

```text
priceScore = 1 - (ABS(preço_candidato - avgPrice) / (maxPrice - minPrice))
```

Avaliação de Hotéis Candidatos (2 quartos):

| Hotel Candidato         | Preço ($) | Cálculo                                                                 | priceScore (%) |
|-------------------------|-----------|--------------------------------------------------------------------------|----------------|
| Médio Histórico         | 200       | 1 - (ABS(200 - 200) / 100) = 1 - (0 / 100) = 1 - 0 = **1.0**              | **100%**       |
| Ligeiramente Mais Caro | 225       | 1 - (ABS(225 - 200) / 100) = 1 - (25 / 100) = 1 - 0.25 = **0.75**         | **75%**        |
| Preço Mínimo            | 150       | 1 - (ABS(150 - 200) / 100) = 1 - (50 / 100) = 1 - 0.5 = **0.5**           | **50%**        |
| Preço Máximo            | 250       | 1 - (ABS(250 - 200) / 100) = 1 - (50 / 100) = 1 - 0.5 = **0.5**           | **50%**        |
| Muito Caro              | 300       | 1 - (ABS(300 - 200) / 100) = 1 - (100 / 100) = 1 - 1 = **0.0**            | **0%**         |
| Muito Barato            | 100       | 1 - (ABS(100 - 200) / 100) = 1 - (100 / 100) = 1 - 1 = **0.0**            | **0%**         |

### Score Final e Ranking de Recomendações

```cypher
WITH hotel, weightedAmenityScore, bedroomScore, priceScore,
     (weightedAmenityScore * 0.4 + bedroomScore * 0.35 + priceScore * 0.25) as finalScore
RETURN hotel.id as hotelId,
       ROUND(finalScore * 100, 2) as finalRecommendationScore
ORDER BY finalScore DESC
LIMIT 10
```
**O que faz?**
  - Combina os três scores calculados anteriormente, com pesos específicos:
    - Comodidades: 40% (0.4)
    - Quartos: 35% (0.35)
    - Preço: 25% (0.25)
  - Retorna o ID do hotel e o Score final, ordenado por ordem decrescente, limitando a 10 recomendações.
  
> ❗ **Nota:** Os pesos podem ser redefinidos, basta alterá-los no código.



## Bibliografia 

- SANTURBANO, Andrea. Transform MongoDB collections automagically into Graphs. Medium, Neo4j Developer Blog, 29 nov. 2019. Disponível em: https://medium.com/neo4j/transform-mongodb-collections-automagically-into-graphs-9ea085d6e3ef. Acesso em: 11 jun. 2025
- MONGODB. Atlas Sample Data – Sample Airbnb. MongoDB, [s.d.]. Disponível em: https://www.mongodb.com/pt-br/docs/atlas/sample-data/sample-airbnb/. Acesso em: 17 jun. 2025.
- NEO4J. APOC Library – Awesome Procedures On Cypher. Neo4j Labs, [s.d.]. Disponível em: https://neo4j.com/labs/apoc/. Acesso em: 17 jun. 2025.

