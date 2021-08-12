class Bottleneck(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  stride : int
  conv1 : __torch__.torch.nn.modules.conv.___torch_mangle_7.Conv2d
  bn1 : __torch__.torch.nn.modules.batchnorm.___torch_mangle_8.BatchNorm2d
  conv2 : __torch__.torch.nn.modules.conv.___torch_mangle_9.Conv2d
  bn2 : __torch__.torch.nn.modules.batchnorm.___torch_mangle_8.BatchNorm2d
  conv3 : __torch__.torch.nn.modules.conv.___torch_mangle_10.Conv2d
  bn3 : __torch__.torch.nn.modules.batchnorm.___torch_mangle_11.BatchNorm2d
  relu : __torch__.torch.nn.modules.activation.ReLU
  downsample : __torch__.torch.nn.modules.container.___torch_mangle_13.Sequential
  def forward(self: __torch__.torchvision.models.resnet.___torch_mangle_14.Bottleneck,
    x: Tensor) -> Tensor:
    out = (self.conv1).forward(x, )
    out0 = (self.bn1).forward(out, )
    out1 = (self.relu).forward(out0, )
    out2 = (self.conv2).forward(out1, )
    out3 = (self.bn2).forward(out2, )
    out4 = (self.relu).forward(out3, )
    out5 = (self.conv3).forward(out4, )
    out6 = (self.bn3).forward(out5, )
    identity = (self.downsample).forward(x, )
    out7 = torch.add_(out6, identity, alpha=1)
    return (self.relu).forward(out7, )
