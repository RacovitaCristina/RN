
# Functia de clasificare
def predict(x, weights, bias):
    z = 0

    for i in range(len(x)):
        z += weights[i] * x[i]

    z += bias

    if z >= 0:
        return 1
    else:
        return -1


# Antrenarea perceptronului
def train(X, Y, learning_rate, epochs):
    weights = [0.0, 0.0]
    bias = 0.0

    for epoch in range(epochs):
        total_errors = 0

        for x, y in zip(X, Y):
            prediction = predict(x, weights, bias)

            error = prediction - y

            if error != 0:
                total_errors += 1

            for i in range(len(weights)):
                weights[i] -= learning_rate * error * x[i]

            bias -= learning_rate * error

        print(f"Epoch {epoch + 1}: errors = {total_errors}")

    return weights, bias


# Datele de antrenare - functia AND
X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

Y = [-1, -1, -1, 1]

weights, bias = train(X, Y, 0.1, 10)

print("Weights:", weights)
print("Bias:", bias)

for x in X:
    print(x, "->", predict(x, weights, bias))
