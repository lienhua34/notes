import tensorflow.contrib.learn as learn
from sklearn import datasets, metrics

iris = datasets.load_iris()
feature_columns = learn.infer_real_valued_columns_from_input(iris.data)
classifier = learn.LinearClassifier(n_classes=3, feature_columns=feature_columns)
classifier.fit(iris.data, iris.target, steps=200, batch_size=32)
iris_predictions = list(classifier.predict(iris.data, as_iterable=True))
score = metrics.accuracy_score(iris.target, iris_predictions)
print("Accuracy: {0:f}".format(score))
