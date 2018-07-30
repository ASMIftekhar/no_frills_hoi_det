import os

import utils.io as io
from utils.argparse_utils import manage_required_args, str_to_bool
from data.hico.hico_constants import HicoConstants
from utils.constants import Constants, ExpConstants
from exp.experimenter import *
from exp.hoi_classifier.data.features_dataset import FeatureConstants
import exp.embeddings_from_classifiers.train as train
import exp.embeddings_from_classifiers.train_w_aes as \
    train_w_aes
from exp.embeddings_from_classifiers.models.one_to_all_model import \
    OneToAllConstants
from exp.embeddings_from_classifiers.models.feat_autoencoders import \
    FeatAutoencodersConstants
import exp.embeddings_from_classifiers.update_hoi_classifier as \
    update_hoi_classifier
import exp.embeddings_from_classifiers.update_hoi_classifier_aes as \
    update_hoi_classifier_aes
import exp.embeddings_from_classifiers.eval as evaluate


parser.add_argument(
    '--num_train_verbs',
    type=int,
    default=100,
    help='Number of training verbs')
parser.add_argument(
    '--word_vec',
    type=str,
    choices=['random','glove'],
    help='Use glove or random as pretrained word vectors')
parser.add_argument(
    '--make_identity',
    type=str_to_bool,
    default=False,
    help='Whether to use glove as global space')
parser.add_argument(
    '--coupling',
    type=str_to_bool,
    default=True,
    help='Whether to use coupling variable')
parser.add_argument(
    '--exp_name',
    type=str,
    help='Name of the experiment for eval')
parser.add_argument(
    '--ae_code_dim',
    type=int,
    default=100,
    help='feat_ae code dim')
parser.add_argument(
    '--ae_hidden_layers',
    type=int,
    default=2,
    help='Number of hidden layers in feat_ae encoders and decoders')
parser.add_argument(
    '--ae_drop_prob',
    type=float,
    default=0.2,
    help='Dropout used in feat_ae')
parser.add_argument(
    '--concept_hidden_layers',
    type=int,
    default=0,
    help='Number of hidden layers in the concept space')
parser.add_argument(
    '--concept_dim',
    type=int,
    default=100,
    help='Dimension of concept space')
parser.add_argument(
    '--concept_loss_weight',
    type=float,
    default=1.0,
    help='Dropout used in feat_ae')


def exp_train():
    exp_name = 'first_try'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.log_dir = os.path.join(exp_const.exp_dir,'log')
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')
    exp_const.num_steps = 40000
    exp_const.lr = 1e-2
    exp_const.num_train_verbs = 100
    exp_const.num_test_verbs = 17

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    model_const.one_to_all = OneToAllConstants()
    train.main(exp_const,data_const,model_const)


def exp_ablation_num_train_verbs():
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=['num_train_verbs'])
    if len(not_specified_args) > 0:
        return

    exp_name = f'num_train_verbs_{args.num_train_verbs}'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/ablation_num_train_verbs')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.log_dir = os.path.join(exp_const.exp_dir,'log')
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')
    exp_const.num_steps = 40000
    exp_const.lr = 1e-2
    exp_const.num_train_verbs = args.num_train_verbs
    exp_const.num_test_verbs = 17
    exp_const.word_vec = 'glove'
    exp_const.make_identity = False

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    model_const.one_to_all = OneToAllConstants()
    train.main(exp_const,data_const,model_const)


def exp_ablation_glove_vs_random():
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=['word_vec'])
    if len(not_specified_args) > 0:
        return

    exp_name = f'word_vec_{args.word_vec}'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/ablation_word_vec')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.log_dir = os.path.join(exp_const.exp_dir,'log')
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')
    exp_const.num_steps = 40000
    exp_const.lr = 1e-2
    exp_const.num_train_verbs = 100
    exp_const.num_test_verbs = 17
    exp_const.word_vec = args.word_vec

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    model_const.one_to_all = OneToAllConstants()
    train.main(exp_const,data_const,model_const)


def exp_ablation_identity_vs_mlp():
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=['make_identity'])
    if len(not_specified_args) > 0:
        return

    exp_name = f'make_identity_{args.make_identity}_2_hidden_layers_adam'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/' + \
        'ablation_identity_vs_mlp_verb_vec_dim_5')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.log_dir = os.path.join(exp_const.exp_dir,'log')
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')
    exp_const.num_steps = 40000
    exp_const.lr = 1e-3
    exp_const.weight_decay = 0
    exp_const.num_train_verbs = 100
    exp_const.num_test_verbs = 17
    exp_const.word_vec = 'glove'

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    model_const.one_to_all = OneToAllConstants()
    model_const.one_to_all.use_coupling_variable = False
    model_const.one_to_all.make_identity = args.make_identity
    train.main(exp_const,data_const,model_const)


def exp_ablation_coupling():
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=['coupling'])
    if len(not_specified_args) > 0:
        return

    exp_name = f'coupling_{args.coupling}'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/ablation_coupling')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.log_dir = os.path.join(exp_const.exp_dir,'log')
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')
    exp_const.num_steps = 40000
    exp_const.lr = 1e-2
    exp_const.num_train_verbs = 100
    exp_const.num_test_verbs = 17
    exp_const.word_vec = 'glove'
    exp_const.make_identity = False

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    model_const.one_to_all = OneToAllConstants()
    model_const.one_to_all.use_coupling_variable = args.coupling
    train.main(exp_const,data_const,model_const)


def exp_update_hoi_classifier():
    make_identity = False
    exp_name = f'make_identity_{make_identity}_sgd'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/ablation_identity_vs_mlp')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    # one_to_all model constants
    model_const.one_to_all = OneToAllConstants()
    model_const.one_to_all.use_coupling_variable = False
    model_const.one_to_all.make_identity = make_identity
    model_const.one_to_all.model_num = 10000
    model_const.one_to_all.model_path = os.path.join(
        exp_const.model_dir,
        f'one_to_all_{model_const.one_to_all.model_num}')
    # hoi_classifier constants have been prespecified in load_classifiers.py

    update_hoi_classifier.main(exp_const,data_const,model_const)


def exp_train_aes_and_concept():
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=[
            'ae_code_dim',
            'ae_hidden_layers',
            'ae_drop_prob',
            'concept_hidden_layers',
            'concept_dim',
            'concept_loss_weight'])
    if len(not_specified_args) > 0:
        return

    exp_name = \
        f'loss_l1_' + \
        f'ae_' + \
        f'code_dim_{args.ae_code_dim}_' + \
        f'hidden_layers_{args.ae_hidden_layers}_' + \
        f'drop_prob_{args.ae_drop_prob}_' + \
        f'concept_' + \
        f'dim_{args.concept_dim}_' + \
        f'hidden_layers_{args.concept_hidden_layers}_' + \
        f'concept_loss_weight_{args.concept_loss_weight}_trial'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/' + \
        'aes_and_concept_space')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.log_dir = os.path.join(exp_const.exp_dir,'log')
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')
    exp_const.num_steps = 40000
    exp_const.lr = 1e-3
    exp_const.weight_decay = 0
    exp_const.num_train_verbs = 100
    exp_const.num_test_verbs = 17
    exp_const.word_vec = 'glove'
    exp_const.concept_loss_weight = args.concept_loss_weight

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const = Constants()
    model_const.feat_ae = FeatAutoencodersConstants()
    model_const.feat_ae.drop_prob = args.ae_drop_prob
    for factor_name in model_const.feat_ae.code_dims.keys():
        model_const.feat_ae.code_dims[factor_name] = args.ae_code_dim
    for factor_name in model_const.feat_ae.num_hidden_layers.keys():
        model_const.feat_ae.num_hidden_layers[factor_name] = \
            args.ae_hidden_layers
    model_const.one_to_all = OneToAllConstants()
    model_const.one_to_all.use_coupling_variable = False
    model_const.one_to_all.make_identity = True
    model_const.one_to_all.num_hidden_layers = args.concept_hidden_layers
    model_const.one_to_all.verb_vec_dim = args.concept_dim
    model_const.one_to_all.feat_dims = model_const.feat_ae.code_dims
    train_w_aes.main(exp_const,data_const,model_const)


def exp_update_hoi_classifier_ae():
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=[
            'ae_code_dim',
            'ae_hidden_layers',
            'ae_drop_prob',
            'concept_hidden_layers',
            'concept_dim',
            'concept_loss_weight'])
    if len(not_specified_args) > 0:
        return

    exp_name = \
        f'loss_l1_' + \
        f'ae_' + \
        f'code_dim_{args.ae_code_dim}_' + \
        f'hidden_layers_{args.ae_hidden_layers}_' + \
        f'drop_prob_{args.ae_drop_prob}_' + \
        f'concept_' + \
        f'dim_{args.concept_dim}_' + \
        f'hidden_layers_{args.concept_hidden_layers}_' + \
        f'concept_loss_weight_{args.concept_loss_weight}'
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/' + \
        'aes_and_concept_space')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')

    data_const = HicoConstants()
    data_const.glove_verb_vecs_npy = os.path.join(
        data_const.proc_dir,
        'glove_verb_vecs.npy')

    model_const_json = os.path.join(exp_const.exp_dir,'model_constants.json')
    model_const_dict = io.load_json_object(model_const_json)
    model_const = Constants()
    model_const.model_num = 35000
    model_const.feat_ae = FeatAutoencodersConstants()
    model_const.feat_ae.from_dict(model_const_dict['feat_ae'])
    model_const.one_to_all = OneToAllConstants()
    model_const.one_to_all.from_dict(model_const_dict['one_to_all'])
    model_const.one_to_all.model_path = os.path.join(
        exp_const.model_dir,
        f'one_to_all_{model_const.model_num}')
    model_const.feat_ae.model_path = os.path.join(
        exp_const.model_dir,
        f'feat_ae_{model_const.model_num}')
    # hoi_classifier constants have been prespecified in load_classifiers.py

    update_hoi_classifier_aes.main(exp_const,data_const,model_const)


def exp_eval():
    # make_identity = False
    # exp_name = f'make_identity_{make_identity}_adam'
    args = parser.parse_args()
    not_specified_args = manage_required_args(
        args,
        parser,
        required_args=['exp_name'])
    if len(not_specified_args) > 0:
        return

    exp_name = args.exp_name
    out_base_dir=os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/embeddings_from_classifier/aes_and_concept_space')
    exp_const = ExpConstants(
        exp_name=exp_name,
        out_base_dir=out_base_dir)
    exp_const.model_dir = os.path.join(exp_const.exp_dir,'models')

    data_const = FeatureConstants()
    hoi_cand_dir = os.path.join(
        os.getcwd(),
        'data_symlinks/hico_exp/hoi_candidates')
    data_const.hoi_cands_hdf5 = os.path.join(
        hoi_cand_dir,
        'hoi_candidates_test.hdf5')
    data_const.box_feats_hdf5 = os.path.join(
        hoi_cand_dir,
        'hoi_candidates_box_feats_test.hdf5')
    data_const.hoi_cand_labels_hdf5 = os.path.join(
        hoi_cand_dir,
        'hoi_candidate_labels_test.hdf5')
    data_const.human_pose_feats_hdf5 = os.path.join(
        hoi_cand_dir,
        'human_pose_feats_test.hdf5')
    data_const.faster_rcnn_feats_hdf5 = os.path.join(
        data_const.proc_dir,
        'faster_rcnn_fc7.hdf5')
    data_const.balanced_sampling = False
    data_const.subset = 'test' 
    
    model_const = Constants()
    model_const.model_num = 35000
    model_const.hoi_classifier_path = os.path.join(
        exp_const.model_dir,
        f'hoi_classifier_pred_feats_{model_const.model_num}')
    evaluate.main(exp_const,data_const,model_const)


if __name__=='__main__':
    list_exps(globals())