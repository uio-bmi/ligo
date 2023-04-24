from unittest import TestCase

from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.dsl.instruction_parsers.DatasetExportParser import DatasetExportParser
from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.dsl.symbol_table.SymbolType import SymbolType
from ligo.preprocessing.filters.ClonesPerRepertoireFilter import ClonesPerRepertoireFilter
from ligo.workflows.instructions.dataset_generation.DatasetExportInstruction import DatasetExportInstruction


class TestDatasetExportParser(TestCase):
    def test_parse_no_preproc(self):
        specs = {"type": "DatasetExport", "export_formats": ["ImmuneML", "AIRR"], "datasets": ["d1"]}

        symbol_table = SymbolTable()
        symbol_table.add("d1", SymbolType.DATASET, RepertoireDataset())

        instruction = DatasetExportParser().parse("instr1", specs, symbol_table)

        self.assertTrue(isinstance(instruction, DatasetExportInstruction))
        self.assertEqual(2, len(instruction.exporters))
        self.assertEqual(1, len(instruction.datasets))
        self.assertIsNone(instruction.preprocessing_sequence)

    def test_parse_preproc(self):
        specs = {"type": "DatasetExport", "export_formats": ["ImmuneML", "AIRR"], "datasets": ["d1"], "preprocessing_sequence": "p1"}

        symbol_table = SymbolTable()
        symbol_table.add("d1", SymbolType.DATASET, RepertoireDataset())
        symbol_table.add("p1", SymbolType.PREPROCESSING, [ClonesPerRepertoireFilter(lower_limit=-1, upper_limit=-1)])

        instruction = DatasetExportParser().parse("instr1", specs, symbol_table)

        self.assertTrue(isinstance(instruction, DatasetExportInstruction))
        self.assertEqual(2, len(instruction.exporters))
        self.assertEqual(1, len(instruction.datasets))
        self.assertEqual(1, len(instruction.preprocessing_sequence))
        self.assertIsInstance(instruction.preprocessing_sequence[0], ClonesPerRepertoireFilter)

