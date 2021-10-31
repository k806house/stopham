import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

ru_lm = torch.hub.load('pytorch/fairseq',
                       'transformer_lm.wmt19.ru',
                       tokenizer='moses',
                       bpe='fastbpe')
