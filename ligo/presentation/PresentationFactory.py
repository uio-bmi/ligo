from ligo.hyperparameter_optimization.states.TrainMLModelState import TrainMLModelState
from ligo.presentation.PresentationFormat import PresentationFormat
from ligo.presentation.html.DatasetExportHTMLBuilder import DatasetExportHTMLBuilder
from ligo.presentation.html.ExploratoryAnalysisHTMLBuilder import ExploratoryAnalysisHTMLBuilder
from ligo.presentation.html.FeasibilitySummaryHTMLBuilder import FeasibilitySummaryHTMLBuilder
from ligo.presentation.html.HPHTMLBuilder import HPHTMLBuilder
from ligo.presentation.html.LIgOSimulationHTMLBuilder import LIgOSimulationHTMLBuilder
from ligo.presentation.html.MLApplicationHTMLBuilder import MLApplicationHTMLBuilder
from ligo.presentation.html.SubsamplingHTMLBuilder import SubsamplingHTMLBuilder
from ligo.simulation.LigoSimState import LigoSimState
from ligo.workflows.instructions.dataset_generation.DatasetExportState import DatasetExportState
from ligo.workflows.instructions.exploratory_analysis.ExploratoryAnalysisState import ExploratoryAnalysisState
from ligo.workflows.instructions.ligo_sim_feasibility.FeasibilitySummaryInstruction import FeasibilitySummaryState
from ligo.workflows.instructions.ml_model_application.MLApplicationState import MLApplicationState
from ligo.workflows.instructions.subsampling.SubsamplingState import SubsamplingState


class PresentationFactory:

    @staticmethod
    def make_presentation_builder(state, presentation_format: PresentationFormat):
        if isinstance(state, TrainMLModelState) and presentation_format == PresentationFormat.HTML:
            return HPHTMLBuilder
        elif isinstance(state, ExploratoryAnalysisState) and presentation_format == PresentationFormat.HTML:
            return ExploratoryAnalysisHTMLBuilder
        elif isinstance(state, DatasetExportState) and presentation_format == PresentationFormat.HTML:
            return DatasetExportHTMLBuilder
        elif isinstance(state, MLApplicationState) and presentation_format == PresentationFormat.HTML:
            return MLApplicationHTMLBuilder
        elif isinstance(state, SubsamplingState) and presentation_format == PresentationFormat.HTML:
            return SubsamplingHTMLBuilder
        elif isinstance(state, LigoSimState) and presentation_format == PresentationFormat.HTML:
            return LIgOSimulationHTMLBuilder
        elif isinstance(state, FeasibilitySummaryState) and presentation_format == PresentationFormat.HTML:
            return FeasibilitySummaryHTMLBuilder
        else:
            raise ValueError(f"PresentationFactory: state and format combination ({type(state).__name__}, {presentation_format.name}) "
                             f"is not supported.")
