import torch
import copy
import torch.nn as nn
from torch.autograd import Variable

import utils.io as io
import utils.pytorch_layers as pytorch_layers


class VerbGivenBoxesAndObjectLabelConstants(io.JsonSerializableClass):
    def __init__(self):
        super(VerbGivenBoxesAndObjectLabelConstants,self).__init__()
        self.box_feat_size = 21
        self.num_objects = 80
        self.num_verbs = 117

    @property
    def mlp_const(self):
        in_dim = 2*self.box_feat_size + self.num_objects
        layer_units = [in_dim]*2
        factor_const = {
            'in_dim': in_dim,
            'out_dim': self.num_verbs,
            'out_activation': 'Identity',
            'layer_units': layer_units,
            'activation': 'ReLU',
            'use_out_bn': False,
            'use_bn': True
        }
        return factor_const
    
    
class VerbGivenBoxesAndObjectLabel(nn.Module,io.WritableToFile):
    def __init__(self,const):
        super(VerbGivenBoxesAndObjectLabel,self).__init__()
        self.const = copy.deepcopy(const)
        self.mlp = pytorch_layers.create_mlp(self.const.mlp_const)

    def transform_feat(self,feat):
        log_feat = torch.log(feat+1e-6)
        transformed_feat = torch.cat((feat,log_feat),1) 
        return transformed_feat

    def forward(self,feats):
        transformed_box_feats = self.transform_feat(feats['box'])
        in_feat = torch.cat((transformed_box_feats,feats['object_one_hot']),1)
        factor_scores = self.mlp(in_feat)
        return factor_scores