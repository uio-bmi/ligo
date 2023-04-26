from ligo.presentation.PresentationFormat import PresentationFormat
from ligo.presentation.html.FeasibilitySummaryHTMLBuilder import FeasibilitySummaryHTMLBuilder
from ligo.presentation.html.LIgOSimulationHTMLBuilder import LIgOSimulationHTMLBuilder
from ligo.simulation.LigoSimState import LigoSimState
from ligo.workflows.instructions.ligo_sim_feasibility.FeasibilitySummaryInstruction import FeasibilitySummaryState


class PresentationFactory:

    @staticmethod
    def make_presentation_builder(state, presentation_format: PresentationFormat):
        if isinstance(state, LigoSimState) and presentation_format == PresentationFormat.HTML:
            return LIgOSimulationHTMLBuilder
        elif isinstance(state, FeasibilitySummaryState) and presentation_format == PresentationFormat.HTML:
            return FeasibilitySummaryHTMLBuilder
        else:
            raise ValueError(f"PresentationFactory: state and format combination ({type(state).__name__}, {presentation_format.name}) "
                             f"is not supported.")
