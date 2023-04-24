import copy

import numpy as np

from ligo.data_model.receptor.RegionType import RegionType
from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.data_model.receptor.receptor_sequence.SequenceAnnotation import SequenceAnnotation
from ligo.environment.SequenceType import SequenceType
from ligo.simulation.implants.ImplantAnnotation import ImplantAnnotation
from ligo.simulation.implants.MotifInstance import MotifInstance
from ligo.simulation.sequence_implanting.SequenceImplantingStrategy import SequenceImplantingStrategy
from ligo.util.PositionHelper import PositionHelper


class GappedMotifImplanting(SequenceImplantingStrategy):

    def implant(self, sequence, signal: dict, sequence_position_weights=None, sequence_type: SequenceType = SequenceType.AMINO_ACID) -> ReceptorSequence:

        assert sequence.metadata.region_type in [RegionType.IMGT_CDR3.name, RegionType.IMGT_JUNCTION.name], \
            f"{GappedMotifImplanting.__name__}: sequence is of type {sequence.metadata.region_type}, but currently only {RegionType.IMGT_CDR3.name} and " \
            f"{RegionType.IMGT_JUNCTION.name} are supported."

        motif_instance = signal["motif_instance"]
        imgt_aa_positions = self._build_imgt_positions(sequence, motif_instance, sequence_type)

        limit = len(motif_instance)
        if sequence_type == SequenceType.NUCLEOTIDE:
            limit = limit * 3

        position_weights = PositionHelper.build_position_weights(sequence_position_weights, imgt_aa_positions, limit)
        implant_position = self._choose_implant_position(imgt_aa_positions, position_weights)
        new_sequence = self._build_new_sequence(sequence, implant_position, signal, sequence_type)
        return new_sequence

    def _build_imgt_positions(self, sequence, motif_instance: MotifInstance, sequence_type: SequenceType):
        sequence_length = len(str(getattr(sequence, "sequence" if sequence_type == SequenceType.NUCLEOTIDE else 'sequence_aa')))
        assert sequence_length >= len(motif_instance), \
            "The motif instance is longer than sequence length. Remove the receptor_sequence from the repertoire or reduce max gap length " \
            "to be able to proceed."

        if sequence.metadata.region_type == RegionType.IMGT_JUNCTION.name:
            return PositionHelper.gen_imgt_positions_from_junction_length(sequence_length)
        elif sequence.metadata.region_type == RegionType.IMGT_CDR3.name:
            return PositionHelper.gen_imgt_positions_from_cdr3_length(sequence_length)
        else:
            raise NotImplementedError(f"IMGT positions here are defined only for CDR3 and JUNCTION region types, got {sequence.metadata.region_type}")

    def _choose_implant_position(self, imgt_positions, position_weights):
        imgt_implant_position = np.random.choice(list(position_weights.keys()), size=1, p=list(position_weights.values()))
        position = np.where(imgt_positions == imgt_implant_position)[0][0]
        return position

    def _build_new_sequence(self, sequence, position, signal: dict, sequence_type: SequenceType = SequenceType.AMINO_ACID):

        gap_length = signal["motif_instance"].gap
        if "/" in signal["motif_instance"].instance:
            motif_left, motif_right = signal["motif_instance"].instance.split("/")
        else:
            motif_left = signal["motif_instance"].instance
            motif_right = ""

        if sequence_type == SequenceType.NUCLEOTIDE:
            position *= 3
            sequence_string = str(sequence.sequence)
        else:
            sequence_string = str(sequence.sequence_aa)

        gap_start = position+len(motif_left)
        gap_end = gap_start+gap_length
        part1 = sequence_string[:position]
        part2 = sequence_string[gap_start:gap_end]
        part3 = sequence_string[gap_end+len(motif_right):]

        new_sequence_string = part1 + motif_left + part2 + motif_right + part3

        annotation = SequenceAnnotation()
        implant = ImplantAnnotation(signal_id=signal["signal_id"],
                                    motif_id=signal["motif_id"],
                                    motif_instance=str(signal["motif_instance"]),
                                    position=position)
        annotation.add_implant(implant)
        annotation.add_implant(ImplantAnnotation(signal_id=signal["signal_id"], motif_id=signal["motif_id"], motif_instance=signal["motif_instance"],
                                                 position=position))

        new_sequence = ReceptorSequence(annotation=annotation, metadata=copy.deepcopy(sequence.metadata))
        new_sequence.metadata.custom_params[signal['signal_id']] = True
        new_sequence.set_sequence(new_sequence_string, sequence_type)

        return new_sequence
