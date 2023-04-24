from pathlib import Path

from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.dsl.symbol_table.SymbolType import SymbolType
from ligo.presentation.html.HTMLBuilder import HTMLBuilder
from ligo.util.ParameterValidator import ParameterValidator
from ligo.util.PathBuilder import PathBuilder


class OutputParser:

    @staticmethod
    def parse(specs: dict, symbol_table: SymbolTable) -> dict:
        if "output" in specs:
            ParameterValidator.assert_keys(specs["output"], ["format"], "OutputParser", "output")
            ParameterValidator.assert_in_valid_list(specs["output"]["format"], ["HTML"], "OutputParser", "format")
        else:
            specs["output"] = {"format": "HTML"}
        symbol_table.add("output", SymbolType.OUTPUT, specs["output"])

        return specs["output"]

    @staticmethod
    def generate_docs(path: Path):
        output_path = PathBuilder.build(path / "output")
        output_path = output_path / "outputs.rst"
        with output_path.open( "w") as file:
            file.writelines(HTMLBuilder.__doc__)
