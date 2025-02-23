import torchvision as torch
from torchvision.models.detection import ssd300_vgg16

# 加载预训练的 SSD 模型
model = ssd300_vgg16(pretrained=True)

# 保存模型
torch.save(model.state_dict(), "ssd300_vgg16.pth")