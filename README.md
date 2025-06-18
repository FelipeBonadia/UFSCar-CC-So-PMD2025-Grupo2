# Projeto Prático – Sistema de Recomendação para Hospedagens no Airbnb

**Grupo:** 2

**Integrantes:**  
- Felipe Bonadia Bravo - 813908
- Laura Rieko Marçal Imai - 813451
- Ryan De Melo Andrade - 812899


**Disciplina:** Processamento Massivo de Dados

**Professora:** Profa. Dra. Sahudy Montenegro González

---

## Introdução
Este projeto propõe o desenvolvimento de um sistema de recomendação para hospedagens da plataforma **Airbnb**, com base no histórico de preferências do usuário. A proposta utiliza um modelo híbrido de bancos NoSQL:

- **MongoDB**: para armazenar dados estruturados sobre as hospedagens;
- **Neo4j**: para modelar e consultar relações entre hospedagens, comodidades e perfis de usuário.

A meta é sugerir acomodações similares às previamente alugadas, com base em atributos como número de quartos, comodidades oferecidas e faixa de preço.

---

## Objetivos

### Objetivo Geral
Implementar um sistema que recomende hospedagens personalizadas usando tecnologias NoSQL.

### Objetivos Específicos
- Identificar padrões de hospedagens preferidas (comodidades, faixa de preço, localização);
- Sugerir hospedagens semelhantes com base em perfil histórico;
- Utilizar grafos para analisar conexões e similaridades entre as hospedagens.

---

## Fonte de Dados
Utiliza-se o dataset público **Airbnb Listings** do **MongoDB Atlas**, contendo cerca de 5.500 registros com informações como:

- Nome, tipo de imóvel, número de quartos, preço;
- Lista de comodidades;
- Localização e avaliações.

[Dataset oficial](https://www.mongodb.com/pt-br/docs/atlas/sample-data/sample-airbnb/#std-label-sample-airbnb)


---

## Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| **MongoDB** | Armazenamento de hospedagens como documentos JSON |
| **Neo4j** | Modelagem e análise das relações via grafos |
| **APOC** | Integração entre MongoDB e Neo4j |
