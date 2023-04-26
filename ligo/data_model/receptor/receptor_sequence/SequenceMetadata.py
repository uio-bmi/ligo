# quality: gold
from ligo.data_model.receptor.RegionType import RegionType
from ligo.data_model.receptor.receptor_sequence.Chain import Chain
from ligo.data_model.receptor.receptor_sequence.SequenceFrameType import SequenceFrameType


class SequenceMetadata:

    def __init__(self, v_call: str = None, j_call: str = None, chain=None, duplicate_count: int = None, frame_type: str = SequenceFrameType.IN.name,
                 region_type: str = None, cell_id: str = None, custom_params: dict = None):
        self.v_call = v_call
        self.j_call = j_call
        self.chain = Chain.get_chain(chain) if chain and isinstance(chain, str) else chain if isinstance(chain, Chain) else None
        self.duplicate_count = int(float(duplicate_count)) if isinstance(duplicate_count, str) else duplicate_count
        self.frame_type = SequenceFrameType(frame_type) if frame_type and isinstance(frame_type, str) and frame_type != 'nan' else frame_type if isinstance(frame_type, SequenceFrameType) else None
        self.region_type = RegionType(region_type) if region_type and isinstance(region_type, str) and region_type != 'nan' else region_type if isinstance(region_type, RegionType) else None
        self.cell_id = cell_id
        self.custom_params = custom_params if custom_params is not None else {}

    @property
    def v_gene(self):
        return self.v_call.split("\*")[0]

    @property
    def j_gene(self):
        return self.j_call.split("\*")[0]

    def get_attribute(self, name: str):
        """Returns the attribute value if attribute is present either directly or in custom_params, otherwise returns None"""
        if hasattr(self, name):
            return getattr(self, name)
        elif name in self.custom_params:
            return self.custom_params[name]
        else:
            return None
