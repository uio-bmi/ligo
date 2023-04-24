import os
from unittest import TestCase

from ligo.caching.CacheType import CacheType
from ligo.dsl.definition_parsers.SimulationParser import SimulationParser
from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.dsl.symbol_table.SymbolType import SymbolType
from ligo.environment.Constants import Constants
from ligo.simulation.implants.Motif import Motif
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.motif_instantiation_strategy.GappedKmerInstantiation import GappedKmerInstantiation
from ligo.simulation.sequence_implanting.GappedMotifImplanting import GappedMotifImplanting
from ligo.simulation.signal_implanting.HealthySequenceImplanting import HealthySequenceImplanting
from ligo.simulation.signal_implanting.ImplantingComputation import ImplantingComputation


class TestSimulationParser(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test_parse_simulation(self):

        simulation = {
            "sim1": {
                "type": "Implanting",
                "sim_items": {
                    "var1": {
                        "type": "Implanting",
                        "signals": ["signal1"],
                        "dataset_implanting_rate": 0.5,
                        "repertoire_implanting_rate": 0.1
                    }
                }
            }
        }

        symbol_table = SymbolTable()
        symbol_table.add("motif1", SymbolType.MOTIF, Motif("motif1", GappedKmerInstantiation(position_weights={0: 1}), seed="CAS"))
        symbol_table.add("signal1", SymbolType.SIGNAL, Signal("signal1", [symbol_table.get("motif1")],
                                                              HealthySequenceImplanting(GappedMotifImplanting(), implanting_computation=ImplantingComputation.ROUND)))

        symbol_table, specs = SimulationParser.parse(simulation, symbol_table)

        self.assertTrue(symbol_table.contains("sim1"))
        sim1 = symbol_table.get("sim1")
        self.assertEqual(1, len(sim1.sim_items))
