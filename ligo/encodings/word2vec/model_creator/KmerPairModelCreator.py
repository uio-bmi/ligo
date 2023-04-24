# quality: gold

from pathlib import Path

from gensim.models import Word2Vec

from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.encodings.word2vec.model_creator.ModelCreatorStrategy import ModelCreatorStrategy
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.SequenceType import SequenceType
from ligo.util.KmerHelper import KmerHelper


class KmerPairModelCreator(ModelCreatorStrategy):

    def create_model(self, dataset: RepertoireDataset, k: int, vector_size: int, batch_size: int, model_path: Path, sequence_type: SequenceType):

        model = Word2Vec(size=vector_size, min_count=1, window=self.window)  # creates an empty model
        all_kmers = KmerHelper.create_all_kmers(k=k, alphabet=EnvironmentSettings.get_sequence_alphabet())
        all_kmers = [[kmer] for kmer in all_kmers]
        model.build_vocab(all_kmers)

        for kmer in all_kmers:
            sentences = KmerHelper.create_kmers_within_HD(kmer=kmer[0],
                                                          alphabet=EnvironmentSettings.get_sequence_alphabet(),
                                                          distance=1)
            model.train(sentences=sentences, total_words=len(all_kmers), epochs=model.epochs)

        model.save(str(model_path))

        return model
