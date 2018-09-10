from src.operators import Operator


class DictOperator(Operator, cls_keywords=('dict', '{}')):
    def __init__(self, used_keyword):
        super().__init__(used_keyword)
        self.last_atom_subject = ' '

    def _handle_multiple_atoms(self):
        """last_atom_subject = ''
        if len(atoms) % 2 != 0:
            last_atom_subject = atoms[-1].subject
            atoms = atoms[:-1]"""
        if len(self.atoms) % 2 != 0:
            self.last_atom_subject += self.atoms[-1].subject
            self.atoms = self.atoms[:-1]

        self._parenthesize_stringify()

        return self._convert()

    def _handle_single_atom(self):
        """:rtype: str"""
        self._parenthesize_stringify(condition=lambda a: a.is_dotted)

        return f'dict({self.atoms[0].result})'

    def _convert(self):
        r_side = ''

        extend_with = lambda target, ex: f'{target}{ex} '
        for idx, atom in enumerate(self.atoms):
            r_side += extend_with(target=atom.result,
                                  ex=':' if idx % 2 == 0 else ',')

        converted = extend_with(target=f'{{{r_side.strip()[:-1]}}}', ex=self.last_atom_subject)

        return converted.strip()