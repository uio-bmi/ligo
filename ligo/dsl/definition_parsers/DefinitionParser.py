from inspect import signature
from pathlib import Path

from ligo.IO.dataset_import.DataImport import DataImport
from ligo.dsl.definition_parsers.DefinitionParserOutput import DefinitionParserOutput
from ligo.dsl.definition_parsers.MotifParser import MotifParser
from ligo.dsl.definition_parsers.SignalParser import SignalParser
from ligo.dsl.definition_parsers.SimulationParser import SimulationParser
from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.simulation.SimConfig import SimConfig
from ligo.simulation.SimConfigItem import SimConfigItem
from ligo.simulation.generative_models.GenerativeModel import GenerativeModel
from ligo.simulation.implants.LigoPWM import LigoPWM
from ligo.simulation.implants.SeedMotif import SeedMotif
from ligo.simulation.implants.Signal import Signal
from ligo.util.PathBuilder import PathBuilder
from ligo.util.ReflectionHandler import ReflectionHandler
from scripts.DocumentatonFormat import DocumentationFormat
from scripts.specification_util import write_class_docs, make_docs


class DefinitionParser:

    @staticmethod
    def parse(workflow_specification: dict, symbol_table: SymbolTable, result_path: Path):

        specs = workflow_specification["definitions"]

        specs_defs = {}

        for parser in [MotifParser, SignalParser, SimulationParser]:
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
        DefinitionParser.make_gen_model_docs(def_path)

    @staticmethod
    def make_simulation_docs(path: Path):

        classes_to_document = [DocumentationFormat(SeedMotif, SeedMotif.__name__, DocumentationFormat.LEVELS[1]),
                               DocumentationFormat(LigoPWM, "PWM", DocumentationFormat.LEVELS[1]),
                               DocumentationFormat(Signal, Signal.__name__, DocumentationFormat.LEVELS[1]),
                               DocumentationFormat(SimConfig, "Simulation config", DocumentationFormat.LEVELS[1]),
                               DocumentationFormat(SimConfigItem, "Simulation config item", DocumentationFormat.LEVELS[1])]

        file_path = path / "simulation.rst"
        with file_path.open("w") as file:
            for doc_format in classes_to_document:
                write_class_docs(doc_format, file)

    @staticmethod
    def make_dataset_docs(path: Path):
        import_classes = ReflectionHandler.all_nonabstract_subclasses(DataImport, "Import", "dataset_import/")
        make_docs(path, import_classes, "datasets.rst", "Import")

    @staticmethod
    def make_gen_model_docs(path: Path):
        gen_models = ReflectionHandler.all_nonabstract_subclasses(GenerativeModel, "", "simulation/generative_models/")
        make_docs(path, gen_models, "gen_models.rst", "")

