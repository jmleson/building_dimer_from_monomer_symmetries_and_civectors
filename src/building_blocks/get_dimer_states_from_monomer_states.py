from src.symmetries.CI_ORDERING import CI_ORDERING
from src.building_blocks.DimerState import DimerState
from src.symmetries.Molecule import Molecule
from src.mathematics.Sign import SIGN


def get_dimer_states_from_monomer_states(molecule:Molecule, ordering:CI_ORDERING):
    monomer_states = molecule.get_ci_vectors_triplets()

    dimer_states = []
    for p in range(len(monomer_states)):
        for l in range(p, len(monomer_states)):
            if monomer_states[p].get_multiplicity() + monomer_states[l].get_multiplicity() != 6:
                continue

            if monomer_states[p].label == monomer_states[l].label:
                d = DimerState(monomer_states[p], monomer_states[l], combination=SIGN.PLUS, point_group=molecule.get_point_group(), ordering=ordering )
                dimer_states.append(d)
            else:
                d = DimerState(monomer_states[p], monomer_states[l], combination=SIGN.PLUS, point_group=molecule.get_point_group(), ordering=ordering )
                dimer_states.append(d)
                d = DimerState(monomer_states[p], monomer_states[l], combination=SIGN.MINUS, point_group=molecule.get_point_group(), ordering=ordering )
                dimer_states.append(d)

    return dimer_states








