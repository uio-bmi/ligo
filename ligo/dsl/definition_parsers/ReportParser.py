from ligo.dsl.ObjectParser import ObjectParser
from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.dsl.symbol_table.SymbolType import SymbolType
from ligo.reports.Report import Report
from ligo.util.Logger import log
from ligo.util.ReflectionHandler import ReflectionHandler


class ReportParser:

    keyword = "reports"

    @staticmethod
    def parse(reports: dict, symbol_table: SymbolTable):
        if reports is None or len(reports) == 0:
            reports = {}

        for rep_id in reports.keys():
            symbol_table, reports[rep_id] = ReportParser._parse_report(rep_id, reports[rep_id], symbol_table)

        return symbol_table, reports

    @staticmethod
    @log
    def _parse_report(key: str, params: dict, symbol_table: SymbolTable):
        valid_values = ReflectionHandler.all_nonabstract_subclass_basic_names(Report, "", "reports/")
        report_object, params = ObjectParser.parse_object(params, valid_values, "", "reports/", "ReportParser", key, builder=True,
                                                          return_params_dict=True)

        symbol_table.add(key, SymbolType.REPORT, report_object)

        return symbol_table, params
