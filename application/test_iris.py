import httplib
import json
from INFaaS import settings
from dbman import DBManangerMongoDB

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'


# Initialize db
dbman = DBManangerMongoDB()
dbman.drop_collections()
dbman.init_collections()

# Prepare connection to INFaaS
conn = httplib.HTTPConnection(settings.SERVER_HOST, settings.SERVER_PORT)

# Register domain
domain = {}
domain["id"] = "net.infidea.infaas.domain.iris"
domain["name"] = "IRIS Example"
domain["description"] = "IRIS Example"
domain["situations"] = ["setosa", "versicolor", "virginica"]
conn.request("POST", "/api/domain", json.dumps(domain), headers={"Content-Type": "application/json"})
response = conn.getresponse()

# Prepare iris training set
baseset = {}
baseset["setosa"] = [
    [5.1, 3.5, 1.4, 0.2],
    [4.9, 3., 1.4, 0.2],
    [4.7, 3.2, 1.3, 0.2],
    [4.6, 3.1, 1.5, 0.2],
    [5., 3.6, 1.4, 0.2],
    [5.4, 3.9, 1.7, 0.4],
    [4.6, 3.4, 1.4, 0.3],
    [5., 3.4, 1.5, 0.2],
    [4.4, 2.9, 1.4, 0.2],
    [4.9, 3.1, 1.5, 0.1],
    [5.4, 3.7, 1.5, 0.2],
    [4.8, 3.4, 1.6, 0.2],
    [4.8, 3., 1.4, 0.1],
    [4.3, 3., 1.1, 0.1],
    [5.8, 4., 1.2, 0.2],
    [5.7, 4.4, 1.5, 0.4],
    [5.4, 3.9, 1.3, 0.4],
    [5.1, 3.5, 1.4, 0.3],
    [5.7, 3.8, 1.7, 0.3],
    [5.1, 3.8, 1.5, 0.3],
    [5.4, 3.4, 1.7, 0.2],
    [5.1, 3.7, 1.5, 0.4],
    [4.6, 3.6, 1., 0.2],
    [5.1, 3.3, 1.7, 0.5],
    [4.8, 3.4, 1.9, 0.2],
    [5., 3., 1.6, 0.2],
    [5., 3.4, 1.6, 0.4],
    [5.2, 3.5, 1.5, 0.2],
    [5.2, 3.4, 1.4, 0.2],
    [4.7, 3.2, 1.6, 0.2],
    [4.8, 3.1, 1.6, 0.2],
    [5.4, 3.4, 1.5, 0.4],
    [5.2, 4.1, 1.5, 0.1],
    [5.5, 4.2, 1.4, 0.2],
    [4.9, 3.1, 1.5, 0.1],
    [5., 3.2, 1.2, 0.2],
    [5.5, 3.5, 1.3, 0.2],
    [4.9, 3.1, 1.5, 0.1],
    [4.4, 3., 1.3, 0.2],
    [5.1, 3.4, 1.5, 0.2],
    [5., 3.5, 1.3, 0.3],
    [4.5, 2.3, 1.3, 0.3],
    [4.4, 3.2, 1.3, 0.2],
    [5., 3.5, 1.6, 0.6],
    [5.1, 3.8, 1.9, 0.4],
    [4.8, 3., 1.4, 0.3],
    [5.1, 3.8, 1.6, 0.2],
    [4.6, 3.2, 1.4, 0.2],
    [5.3, 3.7, 1.5, 0.2],
    [5., 3.3, 1.4, 0.2]
]
baseset["versicolor"] = [
    [7., 3.2, 4.7, 1.4],
    [6.4, 3.2, 4.5, 1.5],
    [6.9, 3.1, 4.9, 1.5],
    [5.5, 2.3, 4., 1.3],
    [6.5, 2.8, 4.6, 1.5],
    [5.7, 2.8, 4.5, 1.3],
    [6.3, 3.3, 4.7, 1.6],
    [4.9, 2.4, 3.3, 1.],
    [6.6, 2.9, 4.6, 1.3],
    [5.2, 2.7, 3.9, 1.4],
    [5., 2., 3.5, 1.],
    [5.9, 3., 4.2, 1.5],
    [6., 2.2, 4., 1.],
    [6.1, 2.9, 4.7, 1.4],
    [5.6, 2.9, 3.6, 1.3],
    [6.7, 3.1, 4.4, 1.4],
    [5.6, 3., 4.5, 1.5],
    [5.8, 2.7, 4.1, 1.],
    [6.2, 2.2, 4.5, 1.5],
    [5.6, 2.5, 3.9, 1.1],
    [5.9, 3.2, 4.8, 1.8],
    [6.1, 2.8, 4., 1.3],
    [6.3, 2.5, 4.9, 1.5],
    [6.1, 2.8, 4.7, 1.2],
    [6.4, 2.9, 4.3, 1.3],
    [6.6, 3., 4.4, 1.4],
    [6.8, 2.8, 4.8, 1.4],
    [6.7, 3., 5., 1.7],
    [6., 2.9, 4.5, 1.5],
    [5.7, 2.6, 3.5, 1.],
    [5.5, 2.4, 3.8, 1.1],
    [5.5, 2.4, 3.7, 1.],
    [5.8, 2.7, 3.9, 1.2],
    [6., 2.7, 5.1, 1.6],
    [5.4, 3., 4.5, 1.5],
    [6., 3.4, 4.5, 1.6],
    [6.7, 3.1, 4.7, 1.5],
    [6.3, 2.3, 4.4, 1.3],
    [5.6, 3., 4.1, 1.3],
    [5.5, 2.5, 4., 1.3],
    [5.5, 2.6, 4.4, 1.2],
    [6.1, 3., 4.6, 1.4],
    [5.8, 2.6, 4., 1.2],
    [5., 2.3, 3.3, 1.],
    [5.6, 2.7, 4.2, 1.3],
    [5.7, 3., 4.2, 1.2],
    [5.7, 2.9, 4.2, 1.3],
    [6.2, 2.9, 4.3, 1.3],
    [5.1, 2.5, 3., 1.1],
    [5.7, 2.8, 4.1, 1.3]
]
baseset["virginica"] = [
    [6.3, 3.3, 6., 2.5],
    [5.8, 2.7, 5.1, 1.9],
    [7.1, 3., 5.9, 2.1],
    [6.3, 2.9, 5.6, 1.8],
    [6.5, 3., 5.8, 2.2],
    [7.6, 3., 6.6, 2.1],
    [4.9, 2.5, 4.5, 1.7],
    [7.3, 2.9, 6.3, 1.8],
    [6.7, 2.5, 5.8, 1.8],
    [7.2, 3.6, 6.1, 2.5],
    [6.5, 3.2, 5.1, 2.],
    [6.4, 2.7, 5.3, 1.9],
    [6.8, 3., 5.5, 2.1],
    [5.7, 2.5, 5., 2.],
    [5.8, 2.8, 5.1, 2.4],
    [6.4, 3.2, 5.3, 2.3],
    [6.5, 3., 5.5, 1.8],
    [7.7, 3.8, 6.7, 2.2],
    [7.7, 2.6, 6.9, 2.3],
    [6., 2.2, 5., 1.5],
    [6.9, 3.2, 5.7, 2.3],
    [5.6, 2.8, 4.9, 2.],
    [7.7, 2.8, 6.7, 2.],
    [6.3, 2.7, 4.9, 1.8],
    [6.7, 3.3, 5.7, 2.1],
    [7.2, 3.2, 6., 1.8],
    [6.2, 2.8, 4.8, 1.8],
    [6.1, 3., 4.9, 1.8],
    [6.4, 2.8, 5.6, 2.1],
    [7.2, 3., 5.8, 1.6],
    [7.4, 2.8, 6.1, 1.9],
    [7.9, 3.8, 6.4, 2.],
    [6.4, 2.8, 5.6, 2.2],
    [6.3, 2.8, 5.1, 1.5],
    [6.1, 2.6, 5.6, 1.4],
    [7.7, 3., 6.1, 2.3],
    [6.3, 3.4, 5.6, 2.4],
    [6.4, 3.1, 5.5, 1.8],
    [6., 3., 4.8, 1.8],
    [6.9, 3.1, 5.4, 2.1],
    [6.7, 3.1, 5.6, 2.4],
    [6.9, 3.1, 5.1, 2.3],
    [5.8, 2.7, 5.1, 1.9],
    [6.8, 3.2, 5.9, 2.3],
    [6.7, 3.3, 5.7, 2.5],
    [6.7, 3., 5.2, 2.3],
    [6.3, 2.5, 5., 1.9],
    [6.5, 3., 5.2, 2.],
    [6.2, 3.4, 5.4, 2.3],
    [5.9, 3., 5.1, 1.8]
]

# Prepare solution
solution = {}
solution["id"] = "net.infidea.infaas.solution.iris"
solution["domain"] = "net.infidea.infaas.domain.iris"
solution["alg"] = "kmeans" # one of the algorithms: c4.5, gnb, svm, knn, kmeans
solution["baseset"] = baseset
solution["visibility"] = "public"
solution["features"] = ["sepal length in cm", "sepal width in cm", "petal length in cm", "petal width in cm"]
solution["conf"] = {"num_clusters":4}

# Register solution
conn.request("POST", "/api/solution", json.dumps(solution), headers={"Content-Type": "application/json"})
response = conn.getresponse()

# Prepare application to request
application = {}
application["user"] = "mkdmkk@gmail.com"
application["solution"] = "net.infidea.infaas.solution.iris"
application["observation"] = [6.3, 3.3, 6., 2.5] # virginica

# Request situation inference
conn.request("POST", "/api/infer", json.dumps(application), headers={"Content-Type": "application/json"})
response = conn.getresponse()
print(response.read())

