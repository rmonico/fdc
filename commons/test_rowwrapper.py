from unittest import TestCase
from . rowwrapper import RowWrapper


class RowWrapperTests(TestCase):

    def test_should_create_property_for_row_id_and_fields(self):
        class SingleClass(RowWrapper):
            pass

        SingleClass._create_field('nome')

        self.assertTrue(hasattr(SingleClass, 'rowid'))
        self.assertTrue(hasattr(SingleClass, 'nome'))

    def test_should_create_a_single_property(self):
        class SingleClass(RowWrapper):
            pass

        SingleClass._create_field('nome')

        instance = SingleClass((1, 'Instance name'))

        self.assertEqual(instance.rowid, 1)
        self.assertEqual(instance.nome, 'Instance name')

    def test_class_with_reference(self):
        class ReferedClass(RowWrapper):
            pass

        ReferedClass._create_field('nome')
        ReferedClass._create_field('observacoes')

        class ClassWithReference(RowWrapper):
            pass

        ClassWithReference._create_field('nome')
        ClassWithReference._create_field('reference', ReferedClass)

        self.assertTrue(hasattr(ClassWithReference, 'rowid'))
        self.assertTrue(hasattr(ClassWithReference, 'nome'))
        self.assertTrue(hasattr(ClassWithReference, 'reference'))
        self.assertTrue(hasattr(ReferedClass, 'rowid'))
        self.assertTrue(hasattr(ReferedClass, 'nome'))
        self.assertTrue(hasattr(ReferedClass, 'observacoes'))

        instance = ClassWithReference((1, 'Instance name', 2, 'Reference name', 'Reference observações'))

        self.assertEqual(instance.rowid, 1)
        self.assertEqual(instance.nome, 'Instance name')
        self.assertEqual(instance.reference.rowid, 2)
        self.assertEqual(instance.reference.nome, 'Reference name')
        self.assertEqual(instance.reference.observacoes, 'Reference observações')
