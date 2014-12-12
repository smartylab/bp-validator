import json
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy
from pymongo import MongoClient
from sklearn.cluster.k_means_ import KMeans

from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.svm.classes import SVC
from sklearn.tree.tree import DecisionTreeClassifier

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

@csrf_exempt
def infer(request):
    # Prepare db
    client = MongoClient()
    db = client.sis

    # Load application
    application = json.loads(request.body)

    # Load solution
    print("Loading solution... (%s)" % application["solution"])
    solution = db.solutions.find({"id": application["solution"]})[0]
    domain = db.domains.find({"id": solution["domain"]})[0]

    # Check algorithm and prepare model
    # The following algorithm types are considered: classification, clustering
    # The following algorithms are supported:
    # Decision Tree (c.4.5), Gaussian Naive Bayes (gnb), Support Vector Machine (svm),
    # K-Nearest Neighbors (knn), K-Means Clustering (kmeans)
    if solution["alg"] == "c4.5":
        model = DecisionTreeClassifier()
        alg_type = "classification"
    elif solution["alg"] == "gnb":
        model = GaussianNB()
        alg_type = "classification"
    elif solution["alg"] == "svm":
        model = SVC()
        alg_type = "classification"
    elif solution["alg"] == "knn":
        model = KNeighborsClassifier(1)
        alg_type = "classification"
    elif solution["alg"] == "kmeans":
        # Check configuration
        if "conf" in application and "num_clusters" in application["conf"]:
            num_clusters = application["conf"]["num_clusters"]
        elif "conf" in solution and "num_clusters" in solution["conf"]:
            num_clusters = solution["conf"]["num_clusters"]
        else:
            num_clusters = len(domain["situations"])
        print("The decided number of clusters is %s." % num_clusters)
        model = KMeans(n_clusters=num_clusters)
        alg_type = "clustering"
    else:
        return HttpResponse("The specified algorithm, %s, is not supported yet." % solution["alg"], content_type="application/json")

    print("The model is prepared: %s" % model)

    # Check solution
    print("Checking solution...")
    sit_list = []
    sit_base_list = []
    for sit, sit_base in solution["baseset"].iteritems():
        print("The situation loaded. %s: %s" % (sit, sit_base))
        sit_list += [sit] * len(sit_base)
        sit_base_list += sit_base

    # Train model
    X = numpy.array(sit_base_list)
    y = numpy.array(sit_list)
    model.fit(X, y)

    # Infer situation
    if alg_type == "classification":
        results = model.predict(numpy.array(application["observation"]))
        print("The situation is inferred: %s" % results)
        return HttpResponse(results, content_type="application/json")
    elif alg_type == "clustering":
        if "observation" in application:
            results = model.predict(numpy.array(application["observation"]))
            print("Result of inference: %s" % results.tolist()[0])
        print("Result of clustering: %s" % model.labels_.tolist())
        return HttpResponse(json.dumps({"baseset":model.labels_.tolist(),"observation":results.tolist()[0]}), content_type="application/json")
    else:
        return HttpResponse("No result.", content_type="application/json")
