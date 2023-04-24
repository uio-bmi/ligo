from dataclasses import dataclass

from ligo.data_model.dataset.Dataset import Dataset
from ligo.encodings.DatasetEncoder import DatasetEncoder
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.reports.Report import Report
from ligo.reports.ReportResult import ReportResult


@dataclass
class ExploratoryAnalysisUnit:
    dataset: Dataset
    report: Report
    preprocessing_sequence: list = None
    encoder: DatasetEncoder = None
    label_config: LabelConfiguration = None
    number_of_processes: int = 1
    report_result: ReportResult = None
