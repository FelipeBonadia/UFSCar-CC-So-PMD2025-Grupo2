from pymongo import MongoClient
from neo4j import GraphDatabase

from neo4j.exceptions import ServiceUnavailable
from pymongo.errors import ConnectionFailure

from flask import Flask, render_template

try:
    mongo = 'mongodb+srv://ryanandrade:12345678ryan@cluster0.jtjptts.mongodb.net/'
    client = MongoClient(mongo, serverSelectionTimeoutMS=3000)
    mongodb = client["hoteis"]
    mongocollection = mongodb["testeEscrita"]

    mongodb2 = client["sample_airbnb"]
    mongocollection2 = mongodb2["listingsAndReviews"]

    client.admin.command('ping')
    print("✅ Conexão com MongoDB bem-sucedida!")

except ConnectionFailure as e:
    print(f"Erro ao conectar no MongoDB: {e}")

try:
    neo = "neo4j://127.0.0.1:7687"
    usuario = "neo4j"
    senha = "12345678ryan"
    driver = GraphDatabase.driver(neo, auth=(usuario, senha))

    with driver.session() as session:
        result = session.run("RETURN 1 AS resultado")
        if result.single()["resultado"] == 1:
            print("✅ Conexão com Neo4j bem-sucedida!")

except ServiceUnavailable as e:
    print(f"❌ Erro ao conectar no Neo4j: {e}")





userConsulta = input("Digite o id do usuário ")

countries = [
    "Australia",
    "Brazil",
    "Canada",
    "China",
    "Hong Kong",
    "Portugal",
    "Spain",
    "Turkey",
    "United States"
]

print("Digite o número do pais que deseja ter as recomendações")

for i, country in enumerate(countries, 1):
    print(f"{i}. {country}")

pais = int(input())

queryAntiga = f"""
CALL {{
  MATCH (u:User {{id: "{str(userConsulta)}" }})-[:HAS_RENTED]->(rentedHotel:Hotel)-[:HAS_AMENITY]->(amenity:Amenity)
  WITH u, COLLECT(DISTINCT amenity) as userPreferredAmenities

  MATCH (u)-[:HAS_RENTED]->(rentedHotel:Hotel)
  WITH u, userPreferredAmenities, 
       COLLECT(rentedHotel.bedrooms) as bedroomHistory,
       AVG(rentedHotel.price) as avgPrice,
       MIN(rentedHotel.price) as minPrice,
       MAX(rentedHotel.price) as maxPrice

  UNWIND bedroomHistory as bedroom
  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice,
       bedroom, COUNT(bedroom) as frequency
  ORDER BY frequency DESC
  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice,
       COLLECT(bedroom)[0] as preferredBedrooms

  MATCH (country:Country {{name: "{countries[pais-1]}"}})<-[:IS_LOCATED]-(hotel:Hotel)
  WHERE NOT EXISTS((u)-[:HAS_RENTED]->(hotel))

  OPTIONAL MATCH (hotel)-[:HAS_AMENITY]->(amenity:Amenity)
  WHERE amenity IN userPreferredAmenities
  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice, preferredBedrooms,
       hotel, COLLECT(DISTINCT amenity) as commonAmenities

  OPTIONAL MATCH (hotel)-[:HAS_AMENITY]->(hotelAmenity:Amenity)
  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice, preferredBedrooms,
       hotel, commonAmenities, COLLECT(DISTINCT hotelAmenity) as hotelAmenities

  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice, preferredBedrooms,
       hotel, commonAmenities, hotelAmenities,
       SIZE(commonAmenities) as commonCount,
       SIZE(userPreferredAmenities) as userCount,
       SIZE(hotelAmenities) as hotelCount
  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice, preferredBedrooms,
       hotel, commonAmenities, commonCount, userCount, hotelCount,
       userCount + hotelCount - commonCount as unionSize,
       CASE 
         WHEN SIZE(userPreferredAmenities) = 0 THEN 0.0
         WHEN userCount + hotelCount - commonCount > 0 THEN toFloat(commonCount) / toFloat(userCount + hotelCount - commonCount)
         ELSE 0.0
       END as amenityScore

  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice, preferredBedrooms,
       hotel, commonAmenities, amenityScore, commonCount,
       CASE 
         WHEN hotel.bedrooms = preferredBedrooms THEN 1.0
         WHEN ABS(hotel.bedrooms - preferredBedrooms) = 1 THEN 0.7
         WHEN ABS(hotel.bedrooms - preferredBedrooms) = 2 THEN 0.4
         ELSE 0.2
       END as bedroomScore

  WITH u, userPreferredAmenities, avgPrice, minPrice, maxPrice, preferredBedrooms,
       hotel, commonAmenities, amenityScore, bedroomScore, commonCount,
       ABS(hotel.price - avgPrice) as priceDiff,
       CASE 
         WHEN maxPrice = minPrice THEN 1.0
         ELSE 1 - (ABS(hotel.price - avgPrice) / (maxPrice - minPrice))
       END as priceScore

  WITH hotel, amenityScore, bedroomScore, priceScore,
       (amenityScore * 0.4 + bedroomScore * 0.35 + priceScore * 0.25) as finalScore

  RETURN hotel.id as hotelId,
         ROUND(finalScore * 100, 2) as finalRecommendationScore
  ORDER BY finalScore DESC
  LIMIT 10
}}

WITH COLLECT({{
  hotelId: hotelId,
  score: finalRecommendationScore
}}) as recommendations

CALL apoc.mongo.insert(
  "mongodb+srv://ryanandrade:12345678ryan@cluster0.jtjptts.mongodb.net/hoteis.testeEscrita", 
  [{{
    userId: "{userConsulta}",
    country: "{countries[pais-1]}",
    timestamp: datetime(),
    recommendations: recommendations
  }}]
)

RETURN 
  "{userConsulta}" as userId,
  datetime() as timestamp,
  SIZE(recommendations) as totalRecommendations,
  recommendations as insertedData;
"""

query2 = f"""
CALL {{
    MATCH (u:User {{id: "{str(userConsulta)}" }})-[:HAS_RENTED]->(rentedHotel:Hotel)-[:HAS_AMENITY]->(amenity:Amenity)
    WITH u, amenity, COUNT(amenity) as amenityFrequency
    WITH u, COLLECT({{amenity: amenity, frequency: amenityFrequency}}) as userAmenityFrequencies,
         SUM(amenityFrequency) as totalAmenityCount
    MATCH (u)-[:HAS_RENTED]->(rentedHotel:Hotel)
    WITH u, userAmenityFrequencies, totalAmenityCount,
         COLLECT(rentedHotel.bedrooms) as bedroomHistory
    UNWIND bedroomHistory as bedroom
    WITH u, userAmenityFrequencies, totalAmenityCount,
         bedroom, COUNT(bedroom) as frequency
    ORDER BY frequency DESC
    WITH u, userAmenityFrequencies, totalAmenityCount,
         COLLECT(bedroom)[0] as preferredBedrooms
    MATCH (u)-[:HAS_RENTED]->(rentedHotel:Hotel)
    WHERE rentedHotel.bedrooms = preferredBedrooms
    WITH u, userAmenityFrequencies, totalAmenityCount, preferredBedrooms,
         AVG(rentedHotel.price) as avgPrice,
         MIN(rentedHotel.price) as minPrice,
         MAX(rentedHotel.price) as maxPrice
    MATCH (country:Country {{name: "{countries[pais-1]}"}})<-[:IS_LOCATED]-(hotel:Hotel)
    // WHERE NOT EXISTS((u)-[:HAS_RENTED]->(hotel))
    OPTIONAL MATCH (hotel)-[:HAS_AMENITY]->(hotelAmenity:Amenity)
    WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
         hotel, COLLECT(DISTINCT hotelAmenity) as hotelAmenities
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
    WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
         hotel, weightedAmenityScore,
         CASE 
           WHEN hotel.bedrooms = preferredBedrooms THEN 1.0
           WHEN ABS(hotel.bedrooms - preferredBedrooms) = 1 THEN 0.7
           WHEN ABS(hotel.bedrooms - preferredBedrooms) = 2 THEN 0.4
           ELSE 0.2
         END as bedroomScore
    WITH u, userAmenityFrequencies, totalAmenityCount, avgPrice, minPrice, maxPrice, preferredBedrooms,
         hotel, weightedAmenityScore, bedroomScore,
         CASE 
           WHEN maxPrice = minPrice THEN 1.0
           ELSE 1 - (ABS(hotel.price - avgPrice) / (maxPrice - minPrice))
         END as priceScore
    WITH hotel, weightedAmenityScore, bedroomScore, priceScore,
         (weightedAmenityScore * 0.4 + bedroomScore * 0.35 + priceScore * 0.25) as finalScore
    RETURN hotel.id as hotelId,
           ROUND(finalScore * 100, 2) as finalRecommendationScore
    ORDER BY finalScore DESC
    LIMIT 10
}}

WITH COLLECT({{
  hotelId: hotelId,
  score: finalRecommendationScore
}}) as recommendations

CALL apoc.mongo.insert(
  "mongodb+srv://ryanandrade:12345678ryan@cluster0.jtjptts.mongodb.net/hoteis.testeEscrita", 
  [{{
    userId: "{userConsulta}",
    country: "{countries[pais-1]}",
    timestamp: datetime(),
    recommendations: recommendations
  }}]
)

RETURN 
  "{userConsulta}" as userId,
  datetime() as timestamp,
  SIZE(recommendations) as totalRecommendations,
  recommendations as insertedData;
  
"""


resultado = mongocollection.find_one({"userId": userConsulta, "country": countries[pais-1]})


#verifica se já tem as recomendações salvas no mongo

ids = []

dadosNome = []
dadosQuarto = []
dadosPreco = []
dadosImagem = []
dadosNumAvl = []
dadosNota = []
dadosHost = []

if resultado is None:

    print("Criando Recomendações")

    with driver.session() as session:
        result = session.run(query2)
        for record in result:
            for item in record["insertedData"]:
                ids.append(item['hotelId'])

else:

    print("Recuperando Recomendações")

    for item in resultado["recommendations"]:
        ids.append(item['hotelId'])



for hotel in ids:

    dadosHotel = mongocollection2.find_one({"_id": hotel},
                                           {"name": 1, "bedrooms": 1, "price": 1, "images.picture_url": 1,
                                            "host.host_name": 1,
                                            "review_scores.review_scores_rating": 1})

    print(dadosHotel)

    dadosNome.append(dadosHotel["name"])
    dadosQuarto.append(dadosHotel["bedrooms"])
    dadosPreco.append(dadosHotel["price"])
    dadosImagem.append(dadosHotel["images"]["picture_url"])
    dadosHost.append(dadosHotel["host"]["host_name"])

    if not dadosHotel["review_scores"]:
        dadosNota.append('-')
    else:
        dadosNota.append(dadosHotel["review_scores"]["review_scores_rating"])

app = Flask(__name__)


@app.route('/')
def index():


    return render_template('index2.html',
                           dadosNome=dadosNome,
                           dadosImagem=dadosImagem,
                           dadosQuarto=dadosQuarto,
                           dadosPreco=dadosPreco,
                           dadosNota=dadosNota,
                           dadosHost=dadosHost)



app.run(debug=False)