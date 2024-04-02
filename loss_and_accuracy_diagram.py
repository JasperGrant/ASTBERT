import matplotlib.pyplot as plt

models = [
    "JasperGrant/ASTBERT-cb-25k-methods",
    "JasperGrant/ASTBERT-cb-5k-methods",
    "JasperGrant/ASTBERT-cb-5k-methods-multipath",
    "JasperGrant/ASTBERT-gb-25k-methods",
    "JasperGrant/ASTBERT-gb-5k-methods",
    "JasperGrant/ASTBERT-gb-5k-methods-multipath",
]

data_file = open("results/loss_and_accuracy.txt", "r")

# For each model read 11 lines of file
# First line is model name
# Next 10 lines are loss, accuracy and epoch values
for model in models:
    model_data = []
    for i in range(11):
        model_data.append(data_file.readline().strip())
    model_data = [data.split("\t") for data in model_data[1:]]
    epochs = [i[2] for i in model_data]
    loss = [float(i[0]) for i in model_data]
    accuracy = [float(i[1]) for i in model_data]
    plt.plot(epochs, accuracy, label=model + " Accuracy")
    plt.title(model)
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()


plt.title("Accuracy vs Epoch")
plt.show()
print(model_data)
