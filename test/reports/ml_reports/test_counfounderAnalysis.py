import os
import shutil
from unittest import TestCase

from ligo.workflows.steps.SignalImplanter import SignalImplanter

from ligo.analysis.data_manipulation.NormalizationType import NormalizationType
from ligo.caching.CacheType import CacheType
from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.encodings.EncoderParams import EncoderParams
from ligo.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder
from ligo.encodings.kmer_frequency.sequence_encoding.SequenceEncodingType import SequenceEncodingType
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.Label import Label
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.environment.SequenceType import SequenceType
from ligo.ml_methods.LogisticRegression import LogisticRegression
from ligo.reports.ml_reports.ConfounderAnalysis import ConfounderAnalysis
from ligo.simulation.dataset_generation.RandomDatasetGenerator import RandomDatasetGenerator
from ligo.simulation.implants.Motif import Motif
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.motif_instantiation_strategy.GappedKmerInstantiation import GappedKmerInstantiation
from ligo.simulation.sequence_implanting.GappedMotifImplanting import GappedMotifImplanting
from ligo.simulation.signal_implanting.HealthySequenceImplanting import HealthySequenceImplanting
from ligo.simulation.signal_implanting.ImplantingComputation import ImplantingComputation
from ligo.util.PathBuilder import PathBuilder
from ligo.util.ReadsType import ReadsType


class TestConfounderAnalysis(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def _create_dummy_lr_model(self, path, encoded_data, label):
        # dummy logistic regression with 100 observations with 3 features belonging to 2 classes
        dummy_lr = LogisticRegression()
        dummy_lr.fit_by_cross_validation(encoded_data,
                                         number_of_splits=2, label=label)

        return dummy_lr

    def _make_dataset(self, path, size) -> RepertoireDataset:

        random_dataset = RandomDatasetGenerator.generate_repertoire_dataset(repertoire_count=size, sequence_count_probabilities={100: 1.},
                                                                            sequence_length_probabilities={5: 1.}, labels={}, path=path)

        signals = [Signal(id="disease", motifs=[Motif(identifier="m1", instantiation=GappedKmerInstantiation(), seed="AAA")],
                          implanting_strategy=HealthySequenceImplanting(implanting_computation=ImplantingComputation.ROUND,
                                                                        implanting=GappedMotifImplanting())),
                   Signal(id="HLA", motifs=[Motif(identifier="m2", instantiation=GappedKmerInstantiation(), seed="CCC")],
                          implanting_strategy=HealthySequenceImplanting(implanting_computation=ImplantingComputation.ROUND,
                                                                        implanting=GappedMotifImplanting())),
                   Signal(id="age", motifs=[Motif(identifier="m3", instantiation=GappedKmerInstantiation(), seed="GGG")],
                          implanting_strategy=HealthySequenceImplanting(implanting_computation=ImplantingComputation.ROUND,
                                                                        implanting=GappedMotifImplanting()))]

        simulation = Simulation([Implanting(dataset_implanting_rate=0.2, signals=signals, name='i1', repertoire_implanting_rate=0.25),
                                 Implanting(dataset_implanting_rate=0.2, signals=[signals[0], signals[1]], name='i2', repertoire_implanting_rate=0.25),
                                 Implanting(dataset_implanting_rate=0.1, signals=[signals[0]], name='i3', repertoire_implanting_rate=0.25),
                                 Implanting(dataset_implanting_rate=0.2, signals=[signals[2]], name='i4', repertoire_implanting_rate=0.25),
                                 Implanting(dataset_implanting_rate=0.1, signals=[signals[1]], name='i5', repertoire_implanting_rate=0.25)
                                 ])

        dataset = SignalImplanter.run(SimulationState(signals=signals, dataset=random_dataset, formats=['ImmuneML'], result_path=path,
                                                      name='my_synthetic_dataset', simulation=simulation, store_signal_in_receptors=True))

        return dataset

    def _encode_dataset(self, encoder, dataset, path, learn_model: bool = True):
        # encodes the repertoire by frequency of 3-mers
        lc = LabelConfiguration()
        lc.add_label("disease", [True, False])
        encoded_dataset = encoder.encode(dataset, EncoderParams(
            result_path=path / "encoded",
            label_config=lc,
            learn_model=learn_model,
            model={}
        ))
        return encoded_dataset

    def _create_report(self, path):
        report = ConfounderAnalysis.build_object(metadata_labels=["age", "HLA"], name='test')

        report.ml_details_path = path / "ml_details.yaml"
        report.label = Label("disease", [True, False])
        report.result_path = path
        encoder = KmerFrequencyEncoder.build_object(RepertoireDataset(), **{
            "normalization_type": NormalizationType.RELATIVE_FREQUENCY.name,
            "reads": ReadsType.UNIQUE.name,
            "sequence_encoding": SequenceEncodingType.CONTINUOUS_KMER.name,
            "k": 3,
            'sequence_type': SequenceType.AMINO_ACID.name
        })
        report.train_dataset = self._encode_dataset(encoder, self._make_dataset(path / "train", size=100), path)
        report.test_dataset = self._encode_dataset(encoder, self._make_dataset(path / "test", size=40), path, learn_model=False)
        report.method = self._create_dummy_lr_model(path, report.train_dataset.encoded_data, Label("disease", [True, False]))

        return report

    def test_generate(self):
        path = EnvironmentSettings.tmp_test_path / "confounder_report/"
        PathBuilder.build(path)

        report = self._create_report(path)

        # Running the report
        result = report._generate()

        shutil.rmtree(path)
