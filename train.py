import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

def main():

    dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Usando dispositivo: {dispositivo}")
    print(f"PyTorch versión: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    print(torch.cuda.get_device_name(0))

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], 
                            std=[0.5, 0.5, 0.5]
                            )
    ])

    #Dataset
    dataset = datasets.ImageFolder(root="Reconocimiento-de-huesos---CNN/database/gender", transform=transform)

    print(f"Número total de imágenes: {len(dataset)}")
    print(f"Clases: {dataset.classes}")


    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True,
        num_workers=0,
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0,
        pin_memory=True
    )

    class CNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Sequential(
                nn.Conv2d(3,32,3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2,2),

                nn.Conv2d(32,64,3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2,2),

                nn.Conv2d(64,128,3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2)
            )

            self.fc = nn.Sequential(
                nn.Flatten(),

                nn.Linear(128*28*28, 256),
                nn.ReLU(),

                nn.Dropout(0.5),
                nn.Linear(256, 2)
            )

        def forward(self, x):
            x = self.conv(x)
            x = self.fc(x)
            return x

    modelo = CNN().to(dispositivo)

    criterio = nn.CrossEntropyLoss()

    optimizador = optim.Adam(modelo.parameters(), lr=0.001)
    num_epochs = 10

    losses = []
    accuracies = []

    for epoch in range(num_epochs):
        modelo.train()
        running_loss = 0.0

        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.to(dispositivo)
            labels = labels.to(dispositivo)
            optimizador.zero_grad()
            outputs = modelo(images)
            loss = criterio(outputs, labels)
            loss.backward()
            optimizador.step()
            running_loss += loss.item()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total

        losses.append(epoch_loss)
        accuracies.append(epoch_acc)

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%")

    # Evaluación en el conjunto de prueba
    modelo.eval()
    correct = 0 
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(dispositivo)
            labels = labels.to(dispositivo)
            outputs = modelo(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    test_acc = 100 * correct / total
    print(f"Test Accuracy: {test_acc:.2f}%")


    torch.save(modelo.state_dict(), "genderModelcnn.pth")

    print("Modelo guardado como genderModelcnn.pth")

if __name__ == "__main__":
    main()