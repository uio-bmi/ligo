from inspect import signature
from pathlib import Path

from ligo.IO.dataset_import.DataImport import DataImport
from ligo.dsl.DefaultParamsLoader import DefaultParamsLoader
from ligo.dsl.definition_parsers.DefinitionParserOutput import DefinitionParserOutput
from ligo.dsl.definition_parsers.EncodingParser import EncodingParser
from ligo.dsl.definition_parsers.MLParser import MLParser
from ligo.dsl.definition_parsers.MotifParser import MotifParser
from ligo.dsl.definition_parsers.PreprocessingParser import PreprocessingParser
from ligo.dsl.definition_parsers.ReportParser import ReportParser
from ligo.dsl.definition_parsers.SignalParser import SignalParser
from ligo.dsl.definition_parsers.SimulationParser import SimulationParser
from ligo.dsl.import_parsers.ImportParser import ImportParser
from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.encodings.DatasetEncoder import DatasetEncoder
from ligo.ml_methods.MLMethod import MLMethod
from ligo.preprocessing.Preprocessor import Preprocessor
from ligo.reports.data_reports.DataReport import DataReport
from ligo.reports.encoding_reports.EncodingReport import EncodingReport
from ligo.reports.ml_reports.MLReport import MLReport
from ligo.reports.multi_dataset_reports.MultiDatasetReport import MultiDatasetReport
from ligo.reports.train_ml_model_reports.TrainMLModelReport import TrainMLModelReport
from ligo.simulation.implants.Motif import Motif
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.motif_instantiation_strategy.MotifInstantiationStrategy import MotifInstantiationStrategy
from ligo.util.PathBuilder import PathBuilder
from ligo.util.ReflectionHandler import ReflectionHandler
from scripts.DocumentatonFormat import DocumentationFormat
from scripts.specification_util import write_class_docs, make_docs


class DefinitionParser:

    @staticmethod
    def parse(workflow_specification: dict, symbol_table: SymbolTable, result_path: Path):

        specs = workflow_specification["definitions"]

        specs_defs = {}

        for parser in [MotifParser, SignalParser, SimulationParser, PreprocessingParser, EncodingParser, MLParser, ReportParser, ImportParser]:
            symbol_table, new_specs = DefinitionParser._call_if_exists(parser.keyword, parser.parse, specs, symbol_table, result_path)
            specs_defs[parser.keyword] = new_specs

        return DefinitionParserOutput(symbol_table=symbol_table, specification=workflow_specification), specs_defs

    @staticmethod
    def _call_if_exists(key: str, method, specs: dict, symbol_table: SymbolTable, path=None):
        if key in specs:
            if "path" in signature(method).parameters:
                return method(specs[key], symbol_table, path)
            else:
                return method(specs[key], symbol_table)
        else:
            return symbol_table, {}

    @staticmethod
    def generate_docs(path: Path):
        def_path = PathBuilder.build(path / "definitions")
        DefinitionParser.make_dataset_docs(def_path)
        DefinitionParser.make_simulation_docs(def_path)
        DefinitionParser.make_encodings_docs(def_path)
        DefinitionParser.make_reports_docs(def_path)
        DefinitionParser.make_ml_methods_docs(def_path)
        DefinitionParser.make_preprocessing_docs(def_path)

    @staticmethod
    def make_simulation_docs(path: Path):
        instantiations = ReflectionHandler.all_nonabstract_subclasses(MotifInstantiationStrategy, "Instantiation", "motif_instantiation_strategy/")
        instantiations = [DocumentationFormat(inst, inst.__name__.replace('Instantiation', ""), DocumentationFormat.LEVELS[2])
                          for inst in instantiations]

        classes_to_document = [DocumentationFormat(Motif, Motif.__name__, DocumentationFormat.LEVELS[1])] + instantiations + \
                              [DocumentationFormat(Signal, Signal.__name__, DocumentationFormat.LEVELS[1])]

        file_path = path / "simulation.rst"
        with file_path.open("w") as file:
            for doc_format in classes_to_document:
                write_class_docs(doc_format, file)

    @staticmethod
    def make_dataset_docs(path: Path):
        import_classes = ReflectionHandler.all_nonabstract_subclasses(DataImport, "Import", "dataset_import/")
        make_docs(path, import_classes, "datasets.rst", "Import")

    @staticmethod
    def make_encodings_docs(path: Path):
        enc_classes = ReflectionHandler.all_direct_subclasses(DatasetEncoder, "Encoder", "encodings/")
        make_docs(path, enc_classes, "encodings.rst", "Encoder")

    @staticmethod
    def make_reports_docs(path: Path):
        filename = "reports.rst"
        file_path = path / filename

        with file_path.open("w") as file:
            pass

        for report_type_class in [DataReport, EncodingReport, MLReport, TrainMLModelReport, MultiDatasetReport]:
            with file_path.open("a") as file:
                doc_format = DocumentationFormat(cls=report_type_class,
                                                 cls_name=f"**{report_type_class.get_title()}**",
                                                 level_heading=DocumentationFormat.LEVELS[1])
                write_class_docs(doc_format, file)

            subdir = DefaultParamsLoader.convert_to_snake_case(report_type_class.__name__) + "s"

            classes = ReflectionHandler.all_nonabstract_subclasses(report_type_class, "", f"reports/{subdir}/")
            make_docs(path, classes, filename, "", "a")

    @staticmethod
    def make_ml_methods_docs(path: Path):
        classes = ReflectionHandler.all_nonabstract_subclasses(MLMethod, "", "ml_methods/")
        make_docs(path, classes, "ml_methods.rst", "")

    @staticmethod
    def make_preprocessing_docs(path: Path):
        classes = ReflectionHandler.all_nonabstract_subclasses(Preprocessor, "", "preprocessing/")
        make_docs(path, classes, "preprocessings.rst", "")
