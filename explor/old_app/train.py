from gensim import models

training_data = []
with open("./all_training_data.txt", "r") as input_file:
    for line in input_file:
        training_data.append(line.split())

model = models.Word2Vec(training_data, min_count=1, size=50,workers=3,window=40,sg=1)
print(model.most_similar('01NX020')[:5])
print(model.most_similar('01FR024')[:5])