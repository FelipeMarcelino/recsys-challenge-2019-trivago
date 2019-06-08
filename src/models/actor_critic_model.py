import torch
import torch.nn as nn #pylint:disable=useless-import-alias
import torch.nn.functional as F#pylint:disable=useless-import-alias



#Tasks of the Actor:
# 1) Setting an initial preference at the beginning of a new recommendation session
# - This is make by training the hidden state of GRU using the last items that user interact
# -- The items will be a embedding vector representation. The article create embedding of items using word vec.
#    In that case a words of items will be a sequence.
# 2) Learning the real-time preferences in the current session of the user, which should capture the interactions of
# the users with system and create a relavant ordered list of recommendations
# - Using CNN to capture local features, the most relevant items for the user will be in the top of the list
# TODO: Use attention with linear transformation (size = 2*hidden or 0.5 Hidden),
# TODO: Add softmax function after output attention layer
# TODO: Test differents size of transpose layer 
# TODO: Verify the output and modify the channels, stride, kernel size of the cnn
class Actor(nn.Module):
    def __init__(self,batch_size, vocab_item, vocab_inter, vocab_times, embedding_output, hidden_size, out_channel):
        super(Actor, self).__init__()
        embedding_layer_item = nn.Embedding(vocab_item, embedding_output, padding_idx=0)
        embedding_layer_inter = nn.Embedding(vocab_inter, embedding_output,  padding_idx=0)
        embedding_layer_times= nn.Embedding(vocab_times, embedding_output, padding_idx=0)
        gru_layer = nn.GRU(embedding_output, hidden_size, batch_first=True)
        ##conv_layer = nn.Conv2d()
        ##deconv_layer = nn.ConvTranspose2d() # Desconvolution Layer - But is not real deconv(https://discuss.pytorch.org/t/true-deconvolution-layer-not-transposed-convolution/27776/9)


    def forward(self, input_state):
        pass
