import shutil
from pathlib import Path

from transformers.models.roberta import RobertaForMaskedLM
from transformers import AutoTokenizer, AutoModelForMaskedLM
from tokenizers import Tokenizer
from tokenizers.processors import TemplateProcessing

from fairseq.models.roberta import RobertaModel

from mlm_scoring.scoring import score_model_on_paradigm

from babyberta import configs
from babyberta.utils import load_tokenizer

model_names = [p.name for p in (configs.Dirs.root / 'saved_models').glob('*')]
model_names.append('RoBERTa-base_10M')  # trained by Warstadt et al., 2020
# model_names.append('RoBERTa-base_AO-CHILDES')  # trained by us using fairseq  # TODO not implemented

path_out = Path('output')

for model_name in model_names:

    path_model_out = (path_out / model_name)
    if path_model_out.exists():
        if len(list(path_model_out.glob('*.txt'))) == 67:
            print(f'Output already exists. Skipping evaluation of {model_name}.')
            continue
        else:
            shutil.rmtree(path_model_out)
    else:
        path_model_out.mkdir(parents=True)

    # BabyBERTa
    if model_name.startswith('BabyBERTa'):
        model = RobertaForMaskedLM.from_pretrained(f'../saved_models/{model_name}')
        path_tokenizer_config = configs.Dirs.tokenizers / 'a-a-w-w-w-8192.json'
        tokenizer = load_tokenizer(path_tokenizer_config, max_num_tokens_in_sequence=128)
        vocab = tokenizer.get_vocab()

    # pre-trained RoBERTa-base by Warstadt et al., 2020
    elif model_name == 'RoBERTa-base_10M':
        model = AutoModelForMaskedLM.from_pretrained("nyu-mll/roberta-base-10M-2")
        model.cuda(0)
        tokenizer = AutoTokenizer.from_pretrained("nyu-mll/roberta-base-10M-2")
        vocab = tokenizer.get_vocab()

    # pre-trained by us using fairseq
    elif model_name == 'RoBERTa-base_AO-CHILDES':
        path_model_data = configs.Dirs.root / 'fairseq_models' / 'fairseq_Roberta-base_5M'
        model = RobertaModel.from_pretrained(model_name_or_path=str(path_model_data / '0'),
                                             checkpoint_file=str(path_model_data / '0' / 'checkpoint_best.pt'),
                                             data_name_or_path=str(path_model_data / 'aochildes-data-bin'),
                                             )
        print(f'Num parameters={sum(p.numel() for p in model.parameters() if p.requires_grad):,}')
        model.eval()
        model.cuda(0)
        vocab = None
        tokenizer = None  # tokenizer in fairseq is part of the model class

    else:
        raise AttributeError('Invalid arg to name')

    for path_paradigm in (configs.Dirs.blimp / 'data').glob('*.txt'):

        print(f"Scoring pairs in {path_paradigm} with {model_name}...")

        path_out_file = configs.Dirs.blimp / 'output' / model_name / path_paradigm.name
        score_model_on_paradigm(model, vocab, tokenizer, path_paradigm, path_out_file)
