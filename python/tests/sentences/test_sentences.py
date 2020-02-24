#  Copyright 2020 Regents of the University of Minnesota.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from argparse import Namespace
from pathlib import Path

import pytest
from mtap import Document, GenericLabel

from biomedicus.config import load_config
from biomedicus.deployment.deploy_biomedicus import check_data
from biomedicus.sentences.bi_lstm import create_processor


@pytest.fixture(name='bi_lstm_model')
def fixture_bi_lstm_model():
    check_data()
    config = load_config()
    conf = Namespace(
        embeddings=Path(config['sentences.wordEmbeddings']),
        chars_file=Path(config['sentences.charsFile']),
        hparams_file=Path(config['sentences.hparamsFile']),
        model_file=Path(config['sentences.modelFile'])
    )
    proc = create_processor(conf)
    yield proc
    proc.close()


def test_sentences_unknown_character(bi_lstm_model):
    document = Document('plaintext', text='• Sentence which contains unknown character.')
    bi_lstm_model.process_document(document, {})
    assert document.get_label_index('sentences') == [GenericLabel(2, 44)]
