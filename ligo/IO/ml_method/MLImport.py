import pickle
from pathlib import Path
from typing import List, Tuple

from ligo.IO.ml_method.MLMethodConfiguration import MLMethodConfiguration
from ligo.environment.Label import Label
from ligo.hyperparameter_optimization.HPSetting import HPSetting
from ligo.preprocessing.Preprocessor import Preprocessor
from ligo.util.ReflectionHandler import ReflectionHandler


class MLImport:

    @staticmethod
    def import_encoder(config: MLMethodConfiguration, config_dir: Path):
        encoder_class = ReflectionHandler.get_class_by_name(config.encoding_class)
        encoder = encoder_class.load_encoder(config_dir / config.encoding_file)
        return encoder

    @staticmethod
    def import_preprocessing_sequence(config: MLMethodConfiguration, config_dir) -> List[Preprocessor]:
        file_path = config_dir / config.preprocessing_file

        if file_path.is_file():
            with file_path.open("rb") as file:
                preprocessing_sequence = pickle.load(file)
        else:
            preprocessing_sequence = []
        return preprocessing_sequence

    @staticmethod
    def import_label(config: MLMethodConfiguration) -> Label:
        return Label(name=config.label_name, values=config.label_values, positive_class=config.label_positive_class)

    @staticmethod
    def import_hp_setting(config_dir: Path) -> Tuple[HPSetting, Label]:

        config = MLMethodConfiguration()
        config.load(config_dir / 'ml_config.yaml')

        ml_method = ReflectionHandler.get_class_by_name(config.ml_method, 'ml_methods/')()
        ml_method.load(config_dir)

        encoder = MLImport.import_encoder(config, config_dir)
        preprocessing_sequence = MLImport.import_preprocessing_sequence(config, config_dir)

        label = MLImport.import_label(config)

        return HPSetting(encoder=encoder, encoder_params=config.encoding_parameters, encoder_name=config.encoding_name,
                         ml_method=ml_method, ml_method_name=config.ml_method_name, ml_params={},
                         preproc_sequence=preprocessing_sequence, preproc_sequence_name=config.preprocessing_sequence_name), label
