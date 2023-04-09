import torch
from torch import nn
from torch.nn import Module, Conv2d, Parameter, Softmax

# OPM适用于obj pair; OPAM适用于attention
__all__ = ['COPM_Module', "OPAM_Module", "msra",
           "Attn_Module", "Norm_Attn_Module", "Attn_Conv_Module", "Attn_Compress_Module",
           "Attn_ConvNorm_Module",
           "OPAM_Small_Cat_Double_Module", "OPAM_Small_NormAttnCat_Double_Module",
           "OPAM_Small_CatPool_Module", "OPAM_Small_CatPool_Double_Module",
           "OPAM_Small_AttnConvCat_Double_Module", "OPAM_Small_AttnCompressCat_Double_Module",
           "OPAM_Small_Cat_Heavy_Module", "OPAM_Small_AttnConvNormCat_Double_Module",
           "OPAM_Norm_Module", "OPAM_Small_CatHeavy_Module",
           "OPAM_Small_Module", "OPAM_Small_Classifier",
           "OPAM_Small_Cat_Module", "OPAM_Small_Cat_Classifier",
           "OPAM_Small_CatAttnNorm_Module",
           "OPAM_Small_CatNorm_Module", "OPAM_Small_CatNorm_Double_Module",
           "OPAM_Small_Cat_PointDepth_Module", "OPAM_Small_Cat_Double_LightCompress_Module",
           "OPAM_Small_Cat_Double_LightCompress_Module",
           "OPAM_Small_Cat_One_Heavy_Module", "OPAM_Small_Cat_Double_Heavy_Module",
           "OPAM_DualAttn_Module", "OPAM_Small_128_Module", "Classifier_Small_Single",
           'Classifier_Mix', 'Classifier_Single', "Classifier_1024", "Classifier_512"]


def msra(module: nn.Module) -> None:
    nn.init.kaiming_normal_(module.weight, mode="fan_out", nonlinearity="relu")
    if module.bias is not None:  # pyre-ignore
        nn.init.constant_(module.bias, 0)


class Attn_Module(Module):
    def __init__(self, in_dim, compress):
        super(Attn_Module, self).__init__()
        channel_in = in_dim//compress
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        for layer in [self.value_conv, self.query_conv, self.key_conv]:
            msra(layer)

    def forward(self, x):
        # B, V, L, 1  256, 1024, 150, 1
        # x = x.permute(0, 2, 1, 3)
        m_batchsize, C, length,  _ = x.size()
        # B X V X L
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        # B X V X L
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = torch.cat((self.gamma*x, proj_value), dim=1).view(m_batchsize, -1, length, 1)
        return x


class Norm_Attn_Module(Module):  # in_channel = out_channel
    def __init__(self, in_dim, compress):
        super(Norm_Attn_Module, self).__init__()
        channel_in = in_dim//8
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=in_dim, kernel_size=1)
        self.query_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)
        self.conv = Conv2d(in_channels=in_dim, out_channels=in_dim, kernel_size=1)

        for layer in [self.value_conv, self.query_conv, self.key_conv, self.conv]:
            msra(layer)

    def forward(self, x):
        m_batchsize, C, length,  _ = x.size()
        v = self.value_conv(x).view(m_batchsize, -1, length)
        q = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        k = self.key_conv(x).view(m_batchsize, -1, length)
        energy = torch.bmm(q, k)
        attn = self.softmax(energy)
        attn = torch.bmm(v, attn.permute(0, 2, 1)).view(m_batchsize, -1, length, 1)
        attn = self.conv(attn)
        x = x + self.gamma*attn
        return x


class Attn_Conv_Module(Module):
    def __init__(self, in_dim, compress):
        super(Attn_Conv_Module, self).__init__()
        channel_in = in_dim//compress
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)
        self.conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)

        for layer in [self.value_conv, self.query_conv, self.key_conv, self.conv]:
            msra(layer)

    def forward(self, x):
        m_batchsize, C, length,  _ = x.size()
        v = self.value_conv(x).view(m_batchsize, -1, length)
        v_f = v.view(m_batchsize, -1, length, 1)
        q = self.query_conv(v_f).view(m_batchsize, -1, length).permute(0, 2, 1)
        k = self.key_conv(v_f).view(m_batchsize, -1, length)
        energy = torch.bmm(q, k)
        attn = self.softmax(energy)
        attn = torch.bmm(v, attn.permute(0, 2, 1)).view(m_batchsize, -1, length, 1)
        attn = self.conv(attn)
        x = torch.cat((v_f, self.gamma*attn), dim=1)
        return x


class Attn_ConvNorm_Module(Module):
    def __init__(self, in_dim, compress):
        super(Attn_ConvNorm_Module, self).__init__()
        channel_in = in_dim//compress
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)
        self.conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.bn1 = nn.Sequential(nn.BatchNorm2d(channel_in*2), nn.ReLU(inplace=True))

        for layer in [self.value_conv, self.query_conv, self.key_conv, self.conv]:
            msra(layer)

    def forward(self, x):
        m_batchsize, C, length,  _ = x.size()
        v = self.value_conv(x).view(m_batchsize, -1, length)
        v_f = v.view(m_batchsize, -1, length, 1)
        q = self.query_conv(v_f).view(m_batchsize, -1, length).permute(0, 2, 1)
        k = self.key_conv(v_f).view(m_batchsize, -1, length)
        energy = torch.bmm(q, k)
        attn = self.softmax(energy)
        attn = torch.bmm(v, attn.permute(0, 2, 1)).view(m_batchsize, -1, length, 1)
        attn = self.conv(attn)
        x = torch.cat((v_f, self.gamma*attn), dim=1)
        x = self.bn1(x)
        return x


class Attn_Compress_Module(Module):
    def __init__(self, in_dim, compress):
        super(Attn_Compress_Module, self).__init__()
        channel_in = in_dim//compress
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in//2, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in//2, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        for layer in [self.value_conv, self.query_conv, self.key_conv]:
            msra(layer)

    def forward(self, x):
        m_batchsize, C, length,  _ = x.size()
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = torch.cat((self.gamma*x, proj_value), dim=1).view(m_batchsize, -1, length, 1)
        return x


class OPAM_Small_Cat_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_Double_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4)
        self.attn2 = Attn_Module(in_dim//2, 1)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_NormAttnCat_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_NormAttnCat_Double_Module, self).__init__()
        self.attn1 = Norm_Attn_Module(in_dim, 1)
        #self.attn2 = Norm_Attn_Module(in_dim, 1)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        #x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_AttnConvCat_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_AttnConvCat_Double_Module, self).__init__()
        self.attn1 = Attn_Conv_Module(in_dim, 4)
        self.attn2 = Attn_Conv_Module(in_dim//2, 1)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_AttnConvNormCat_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_AttnConvNormCat_Double_Module, self).__init__()
        self.attn1 = Attn_ConvNorm_Module(in_dim, 4)
        self.attn2 = Attn_ConvNorm_Module(in_dim//2, 1)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_AttnCompressCat_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_AttnCompressCat_Double_Module, self).__init__()
        self.attn1 = Attn_Compress_Module(in_dim, 4)
        self.attn2 = Attn_Compress_Module(in_dim//2, 1)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_Cat_Heavy_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_Heavy_Module, self).__init__()
        self.attn1 = Attn_Compress_Module(in_dim, 2)
        self.conv1 = nn.Conv2d(in_channels=in_dim, out_channels=in_dim, kernel_size=1)
        self.bn1 = nn.Sequential(nn.BatchNorm2d(in_dim), nn.ReLU(inplace=True), nn.Dropout2d(0.1, False))
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.conv1, self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_CatPool_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_CatPool_Module, self).__init__()
        channel_in = in_dim//4
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)
        self.pool = nn.MaxPool2d(kernel_size=(150, 1))
        self.depth_conv = nn.Conv2d(in_channels=channel_in*2,
                                    out_channels=channel_in*2,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in*2)

        self.point_conv = Conv2d(in_channels=channel_in*2, out_channels=channel_in*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(channel_in*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.value_conv, self.query_conv, self.key_conv]:
            msra(layer)
        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        # B, V, L, 1  256, 1024, 150, 1
        m_batchsize, C, length,  _ = x.size()
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = torch.cat((self.gamma*x, proj_value), dim=1).view(m_batchsize, -1, length, 1)
        y = self.pool(x).view(m_batchsize, -1)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(m_batchsize, -1)
        return torch.cat((x, y), dim=1)


class OPAM_Small_CatPool_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_CatPool_Double_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4)
        self.attn2 = Attn_Module(in_dim//2, 1)
        self.pool = nn.MaxPool2d(kernel_size=(150, 1))
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        y = self.pool(x).view(x.size(0), -1)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return torch.cat((x, y), dim=1)








class OPAM_Small_Cat_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_Module, self).__init__()
        channel_in = in_dim//4
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        self.depth_conv = nn.Conv2d(in_channels=channel_in*2,
                                    out_channels=channel_in*2,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in*2)

        self.point_conv = Conv2d(in_channels=channel_in*2, out_channels=channel_in*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(channel_in*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.value_conv, self.query_conv, self.key_conv]:
            msra(layer)
        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        # B, V, L, 1  256, 1024, 150, 1
        m_batchsize, C, length,  _ = x.size()
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = torch.cat((self.gamma*x, proj_value), dim=1).view(m_batchsize, -1, length, 1)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_CatHeavy_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_CatHeavy_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 2)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

        for layer in [self.depth_conv, self.point_conv]:
            msra(layer)

    def forward(self, x):
        x = self.attn1(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class COPM_Module(nn.Module):
    def __init__(self, one_hot_cls_num, arch):
        super(COPM_Module, self).__init__()
        out_channels = 512 if arch == 'resnet18' else 2048

        if one_hot_cls_num == 80:
            self.fc1 = nn.Linear(3240, 2048)
            self.fc2 = nn.Linear(2048, out_channels)
            self.dropout = nn.Dropout(0.5)
        elif one_hot_cls_num == 150:
            self.fc1 = nn.Linear(22500, 8192)
            self.fc2 = nn.Linear(8192, out_channels)
            self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = x.view(x.size(0),-1)
        # batch * 11325
        out = self.fc1(x)
        out = self.dropout(out)
        out = self.fc2(out)
        return out


# attention matrix大模型
class OPAM_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Module, self).__init__()
        channel_in = in_dim//8
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        out_channels = 512 if arch == 'resnet18' else 2048
        if one_hot_cls_num == 80:
            self.fc1 = nn.Linear(one_hot_cls_num*channel_in, 2048)
            self.fc2 = nn.Linear(2048, out_channels)
            self.dropout = nn.Dropout(0.5)
        elif one_hot_cls_num == 150:
            self.fc1 = nn.Linear(one_hot_cls_num*channel_in, 8192)
            self.fc2 = nn.Linear(8192, out_channels)
            self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # B, V, L, 1 256, 1024, 150, 1
        # x = x.permute(0, 2, 1, 3)
        m_batchsize, C, length,  _ = x.size()
        # B X V X L
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        # proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        # B X V X L
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = self.gamma*x + proj_value
        # B X CH
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x


class OPAM_Small_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Module, self).__init__()
        channel_in = in_dim//4
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        self.depth_conv = nn.Conv2d(in_channels=channel_in,
                                    out_channels=channel_in,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in)

        self.point_conv = Conv2d(in_channels=channel_in, out_channels=channel_in*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(channel_in*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        # B, V, L, 1  256, 1024, 150, 1
        # x = x.permute(0, 2, 1, 3)
        m_batchsize, C, length,  _ = x.size()
        # B X V X L
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        # proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        # B X V X L
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = (self.gamma*x + proj_value).view(m_batchsize, -1, length, 1)

        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)

        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_CatAttnNorm_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_CatAttnNorm_Module, self).__init__()
        channel_in = in_dim//4
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.attn_norm = nn.BatchNorm2d(channel_in)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        self.depth_conv = nn.Conv2d(in_channels=channel_in*2,
                                    out_channels=channel_in*2,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in*2)

        self.point_conv = Conv2d(in_channels=channel_in*2, out_channels=channel_in*4, kernel_size=1)
        self.norm = nn.BatchNorm2d(channel_in*4)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        # B, V, L, 1  256, 1024, 150, 1
        m_batchsize, C, length,  _ = x.size()
        # B X V X L
        proj_value = self.value_conv(x)
        proj_value = self.attn_norm(proj_value).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        # B X V X L
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = torch.cat((self.gamma*x, proj_value), dim=1).view(m_batchsize, -1, length, 1)

        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)

        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_CatNorm_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_CatNorm_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4)
        channel_in = in_dim//2
        self.depth_conv = nn.Conv2d(in_channels=channel_in,
                                    out_channels=channel_in,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in)
        self.norm1 = nn.BatchNorm2d(channel_in)
        self.point_conv = Conv2d(in_channels=channel_in, out_channels=channel_in*2, kernel_size=1)
        self.norm2 = nn.BatchNorm2d(channel_in*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.depth_conv(x)
        x = self.norm1(x)
        x = self.relu(x)
        x = self.point_conv(x)
        x = self.norm2(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_CatNorm_Double_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_CatNorm_Double_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4)
        self.attn2 = Attn_Module(in_dim//2, 1)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.norm1 = nn.BatchNorm2d(in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm2 = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.norm1(x)
        x = self.relu(x)
        x = self.point_conv(x)
        x = self.norm2(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_Cat_One_Heavy_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_One_Heavy_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4) # 1024-512
        self.conv1 = nn.Sequential(nn.Conv2d(in_channels=in_dim//2, out_channels=in_dim//2, kernel_size=1),
                                   nn.BatchNorm2d(in_dim//2), nn.ReLU(inplace=True), nn.Dropout2d(0.1, False))
        in_dim = in_dim//2
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.conv1(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_Cat_Double_Heavy_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_Double_Heavy_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4) # 1024-512
        self.conv1 = nn.Sequential(nn.Conv2d(in_channels=in_dim//2, out_channels=in_dim//2, kernel_size=1),
                                   nn.BatchNorm2d(in_dim//2), nn.ReLU(inplace=True), nn.Dropout2d(0.1, False))
        self.attn2 = Attn_Module(in_dim//2, 1) # 512-1024
        self.conv2 = nn.Sequential(nn.Conv2d(in_channels=in_dim, out_channels=in_dim, kernel_size=1),
                                   nn.BatchNorm2d(in_dim), nn.ReLU(inplace=True))
        in_dim = in_dim
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.conv1(x)
        x = self.attn2(x)
        x = self.conv2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_Cat_Double_LightCompress_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_Double_LightCompress_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 2)
        self.attn2 = Attn_Module(in_dim, 2)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_Cat_Trible_LightCompress_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_Trible_LightCompress_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 2)
        self.attn2 = Attn_Module(in_dim, 2)
        self.attn3 = Attn_Module(in_dim, 2)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.attn2(x)
        x = self.attn3(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_Cat_PointDepth_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_Cat_PointDepth_Module, self).__init__()
        self.attn1 = Attn_Module(in_dim, 4)
        self.conv1 = Conv2d(in_channels=in_dim//2, out_channels=in_dim, kernel_size=1)
        self.norm1 = nn.BatchNorm2d(in_dim)
        self.depth_conv = nn.Conv2d(in_channels=in_dim,
                                    out_channels=in_dim,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=in_dim)
        self.point_conv = Conv2d(in_channels=in_dim, out_channels=in_dim*2, kernel_size=1)
        self.norm2 = nn.BatchNorm2d(in_dim*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.attn1(x)
        x = self.v(x)
        x = self.norm1(x)
        x = self.relu(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm2(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        return x


class OPAM_Small_128_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Small_128_Module, self).__init__()
        channel_in = in_dim//8
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        self.depth_conv = nn.Conv2d(in_channels=channel_in,
                                    out_channels=channel_in,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in)

        self.point_conv = Conv2d(in_channels=channel_in, out_channels=channel_in*2, kernel_size=1)
        self.norm = nn.BatchNorm2d(channel_in * 2)
        self.relu = nn.ReLU(inplace=True)
        self.point_conv1 = Conv2d(in_channels=channel_in*2, out_channels=channel_in*4, kernel_size=1)
        self.norm1 = nn.BatchNorm2d(channel_in * 4)

    def forward(self, x):
        # B, V, L, 1  256, 1024, 150, 1
        # x = x.permute(0, 2, 1, 3)
        m_batchsize, C, length,  _ = x.size()
        # B X V X L
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        # proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        # B X V X L
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = (self.gamma*x + proj_value).view(m_batchsize, -1, length, 1)

        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)
        x = self.point_conv1(x)
        x = self.norm1(x)
        x = self.relu(x)

        x = x.view(x.size(0), -1)
        return x


class OPAM_DualAttn_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_DualAttn_Module, self).__init__()
        channel_in = in_dim//4
        self.value_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)
        self.value_conv1 = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)

        self.depth_conv = nn.Conv2d(in_channels=channel_in,
                                    out_channels=channel_in,
                                    kernel_size=(one_hot_cls_num, 1),
                                    stride=1,
                                    padding=0,
                                    groups=channel_in)

        self.point_conv = Conv2d(in_channels=channel_in, out_channels=channel_in * 2, kernel_size=1)
        self.norm = nn.BatchNorm2d(channel_in*2)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        # B, V, L, 1 256, 1024, 150, 1
        # x = x.permute(0, 2, 1, 3)
        m_batchsize, C, length,  _ = x.size()
        # B X V X L
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)
        x = proj_value.view(m_batchsize, -1, length, 1)
        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        # proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)
        # B X V X L
        x = torch.bmm(proj_value, attention.permute(0, 2, 1))
        x = (self.gamma*x + proj_value).view(m_batchsize, -1, length, 1)

        # B X V X L
        proj_value1 = self.value_conv1(x).view(m_batchsize, -1, length)
        proj_query1 = proj_value1
        # B X L X V
        proj_key1 = proj_value1.permute(0, 2, 1)
        energy1 = torch.bmm(proj_query1, proj_key1)
        energy_new = torch.max(energy1, -1, keepdim=True)[0].expand_as(energy1) - energy1
        attention1 = self.softmax(energy_new)
        x = torch.bmm(attention1, proj_value1)
        x = (self.gamma*x + proj_value1).view(m_batchsize, -1, length, 1)

        x = self.depth_conv(x)
        x = self.point_conv(x)
        x = self.norm(x)
        x = self.relu(x)

        x = x.view(x.size(0), -1)
        return x


# normal attention
class OPAM_Norm_Module(Module):
    def __init__(self, in_dim, one_hot_cls_num, arch):
        super(OPAM_Norm_Module, self).__init__()
        channel_in = in_dim//8
        self.reduce_conv = Conv2d(in_channels=in_dim, out_channels=channel_in, kernel_size=1)
        self.query_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.key_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.value_conv = Conv2d(in_channels=channel_in, out_channels=channel_in, kernel_size=1)
        self.gamma = Parameter(torch.zeros(1), requires_grad=True)
        self.softmax = Softmax(dim=-1)

        out_channels = 512 if arch == 'resnet18' else 2048
        if one_hot_cls_num == 80:
            self.fc1 = nn.Linear(one_hot_cls_num*channel_in, 2048)
            self.fc2 = nn.Linear(2048, out_channels)
            self.dropout = nn.Dropout(0.5)
        elif one_hot_cls_num == 150:
            self.fc1 = nn.Linear(one_hot_cls_num*channel_in, 8192)
            self.fc2 = nn.Linear(8192, out_channels)
            self.dropout = nn.Dropout(0.5)
    def forward(self, x):
        # B, V, L, 1 
        x = x.permute(0, 2, 1, 3)
        x = self.reduce_conv(x)
        m_batchsize, C, length, one = x.size()

        # B X L X V
        proj_query = self.query_conv(x).view(m_batchsize, -1, length).permute(0, 2, 1)
        # B X V X L
        proj_key = self.key_conv(x).view(m_batchsize, -1, length)        
        # B X L X L
        energy = torch.bmm(proj_query, proj_key)
        attention = self.softmax(energy)

        # B X V X L
        proj_value = self.value_conv(x).view(m_batchsize, -1, length)    
        # B X V X L
        o = torch.bmm(proj_value, attention.permute(0, 2, 1))
        o = o.view(m_batchsize, C, length, one)
        x = self.gamma*o + x

        x = x.view(m_batchsize, -1)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x



class Classifier_Mix(nn.Module):
    # resnet 50 -- 2048v, resnet 18 --- 512v
    def __init__(self, num_classes, arch):
        super(Classifier_Mix, self).__init__()
        if arch == "resnet18":
            self.fc1 = nn.Linear(1024, 512)
            self.fc2 = nn.Linear(512, num_classes)
        elif arch == "resnet50":
            self.fc1 = nn.Linear(4096, 2048)  # originally 1024
            self.fc2 = nn.Linear(2048, num_classes)  # originally 1024
        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU(inplace=True)
        nn.init.normal_(self.fc1.weight, std=0.01)
        nn.init.normal_(self.fc2.weight, std=0.01)

    def forward(self, x, idt):
        out = torch.cat((x, idt), 1)
        out = self.fc1(out)
        out = self.dropout(out)
        out = self.relu(out)
        out_ood_feature = out # only used when extracting features for OOD test
        out = self.fc2(out)
        return out, out_ood_feature


class Classifier_Single(nn.Module):
    def __init__(self, num_classes, arch):
        super(Classifier_Single, self).__init__()
        if arch == "resnet18":
            self.fc = nn.Linear(512, num_classes)
        else:
            self.fc = nn.Linear(2048, num_classes)
        nn.init.normal_(self.fc.weight, std=0.01)

    def forward(self, x):
        out = self.fc(x)
        return out


class Classifier_Small_Single(nn.Module):
    def __init__(self, num_classes, arch):
        super(Classifier_Small_Single, self).__init__()
        self.fc = nn.Linear(512, num_classes)
        nn.init.normal_(self.fc.weight, std=0.01)

    def forward(self, x):
        out = self.fc(x)
        return out


class OPAM_Small_Classifier(nn.Module):
    def __init__(self, num_classes):
        super(OPAM_Small_Classifier, self).__init__()
        self.fc = nn.Linear(512, num_classes)
        nn.init.normal_(self.fc.weight, std=0.01)

    def forward(self, x):
        out = self.fc(x)
        return out


class OPAM_Small_Cat_Classifier(nn.Module):
    def __init__(self, num_classes):
        super(OPAM_Small_Cat_Classifier, self).__init__()
        self.fc = nn.Linear(1024, num_classes)

    def forward(self, x):
        out = self.fc(x)
        return out


class Classifier_1024(nn.Module):
    def __init__(self, num_classes):
        super(Classifier_1024, self).__init__()
        self.fc = nn.Linear(1024, num_classes)
        nn.init.normal_(self.fc.weight, std=0.01)

    def forward(self, x):
        out = self.fc(x)
        return out


class Classifier_512(nn.Module):
    def __init__(self, num_classes):
        super(Classifier_512, self).__init__()
        self.fc = nn.Linear(512, num_classes)
        nn.init.normal_(self.fc.weight, std=0.01)

    def forward(self, x):
        out = self.fc(x)
        return out
