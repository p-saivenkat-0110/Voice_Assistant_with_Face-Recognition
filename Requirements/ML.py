import numpy as np

def distance(v1,v2):
    minlen = min(len(v1), len(v2))
    v1 = v1[:minlen]
    v2 = v2[:minlen]
    return np.sqrt(((v1 - v2) ** 2).sum())


def knn(train, test, k=15):
    dist = []
    for i in range(train.shape[0]):
        # Get the vector and label
        ix = train[i, :-1]
        iy = train[i, -1]
        # Compute the distance from test point
        # print("Train : ",train)
        # print("\n\nTest : \n",test)
        # print("\n\nIX : \n",ix)
        # print("\n\nIY : \n",iy)
        # print("\n\n\n",len(train),len(test),len(ix))

        d = distance(test, ix)
        dist.append([d, iy])
    # Sort based on distance and get top k
    dk = sorted(dist, key=lambda x: x[0])[:k]
    # Retrieve only the labels
    # print(dist)

    labels = np.array(dk)[:, -1]
    # Get frequencies of each label
    output = np.unique(labels, return_counts=True)
    # Find max frequency and corresponding label
    index = np.argmax(output[1])
    return output[0][index]