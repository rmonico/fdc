from unittest import TestCase

from commons.rowwrapper import RowWrapper


class RowWrapperTests(TestCase):

    def test_should_create_property_for_row_id_and_fields(self):
        class SingleClass(RowWrapper):
            pass

        SingleClass.create_field('nome')

        self.assertTrue(hasattr(SingleClass, 'rowid'))
        self.assertTrue(hasattr(SingleClass, 'nome'))

    def test_should_create_a_single_property(self):
        class SingleClass(RowWrapper):
            pass

        SingleClass.create_field('nome')

        instance = SingleClass((1, 'Instance name'))

        self.assertEqual(instance.rowid, 1)
        self.assertEqual(instance.nome, 'Instance name')

    def test_class_with_reference(self):
        class ReferedClass(RowWrapper):
            pass

        ReferedClass.create_field('nome')
        ReferedClass.create_field('observacoes')

        class ClassWithReference(RowWrapper):
            pass

        ClassWithReference.create_field('nome')
        ClassWithReference.create_field('reference', ReferedClass)

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

    def test_should_build_reference_with_callable(self):
        class AnotherClass(object):
            def __init__(self, id, value):
                self.id = id
                self.value = value

        def another_class_builder(row, offset):
            return AnotherClass(row[offset], row[offset + 1])

        class ClassWithReference(RowWrapper):
            pass

        ClassWithReference.create_field('nome')
        ClassWithReference.create_field('reference', another_class_builder, 2)
        ClassWithReference.create_field('ref', another_class_builder, 2)

        instance = ClassWithReference((1, 'Instance name', 2, 'Reference value', 4, 'Another reference value'))

        self.assertEqual(instance.rowid, 1)
        self.assertEqual(instance.nome, 'Instance name')
        self.assertEqual(instance.reference.id, 2)
        self.assertEqual(instance.reference.value, 'Reference value')
        self.assertEqual(instance.ref.id, 4)
        self.assertEqual(instance.ref.value, 'Another reference value')
