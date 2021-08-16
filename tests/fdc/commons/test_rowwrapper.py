import unittest

from commons.rowwrapper import RowWrapper


class RowWrapperTests(unittest.TestCase):

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
        class ReferredClass(RowWrapper):
            pass

        ReferredClass.create_field('nome')
        ReferredClass.create_field('observacoes')

        class ClassWithReference(RowWrapper):
            pass

        ClassWithReference.create_field('nome')
        ClassWithReference.create_field('reference', ReferredClass)

        self.assertTrue(hasattr(ClassWithReference, 'rowid'))
        self.assertTrue(hasattr(ClassWithReference, 'nome'))
        self.assertTrue(hasattr(ClassWithReference, 'reference'))
        self.assertTrue(hasattr(ReferredClass, 'rowid'))
        self.assertTrue(hasattr(ReferredClass, 'nome'))
        self.assertTrue(hasattr(ReferredClass, 'observacoes'))

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

    def zip_with_range_for_greater(self, expected, actual):
        len_expected = len(expected)
        len_actual = len(actual)

        longest = len_expected if len_expected > len_actual else len_actual

        return zip(range(longest), expected, actual)

    def assertFieldListEqual(self, entity_class, expected_list):
        actual_list = entity_class.fields()

        for i, expected, actual in self.zip_with_range_for_greater(expected_list, actual_list):
            for j, expected_referrence, actual_referrence in self.zip_with_range_for_greater(expected[0], actual[0]):
                self.assertEqual(expected_referrence, actual_referrence, f'Item {i}, reference {j}, expected: {expected_referrence.__name__}, actual: {actual_referrence.__name__}')
            self.assertEqual(expected_referrence, actual_referrence, 'Item {i}, reference list size')

            self.assertEqual(expected[1], actual[1], f'Item {i}, field name')

        self.assertEqual(len(expected_list), len(actual_list), 'Lists size')

    # FIXME
    def test_should_return_fields_for_class_with_fields(self):
        class ClassWithFields(RowWrapper):
            pass

        ClassWithFields.create_field('name')
        ClassWithFields.create_field('age')
        ClassWithFields.create_field('address')

        expected_list = [([ClassWithFields], 'rowid'),
                         ([ClassWithFields], 'name'),
                         ([ClassWithFields], 'age'),
                         ([ClassWithFields], 'address'), ]

        # import ipdb; ipdb.set_trace()
        self.assertFieldListEqual(ClassWithFields, expected_list)

    # FIXME
    def test_should_return_fields_for_class_with_inheritance(self):
        class SuperClass(RowWrapper):
            pass

        SuperClass.create_field('name')

        class SubClass(SuperClass):
            pass

        SubClass.create_field('address')

        expected_list = [
            ([SubClass], 'rowid'),
            ([SubClass], 'name'),
            ([SubClass], 'address'),
        ]

        self.assertFieldListEqual(SubClass, expected_list)

    # FIXME
    def test_should_return_fields_for_class_with_reference_and_inheritance(self):
        class SuperClass(RowWrapper):
            pass

        SuperClass.create_field('superclassfield')

        class SubClass(SuperClass):
            pass

        SubClass.create_field('subclassfield')

        class ReferrencerClass(RowWrapper):
            pass

        ReferrencerClass.create_field('subclassid', SubClass)
        ReferrencerClass.create_field('referrencerfield')

        expected_list = [
            ([ReferrencerClass], 'rowid'),
            ([ReferrencerClass], 'subclassid'),
            ([ReferrencerClass, SubClass], 'rowid'),
            ([ReferrencerClass, SubClass], 'superclassfield'),
            ([ReferrencerClass, SubClass], 'subclassfield'),
            ([ReferrencerClass], 'referrencerfield'),
        ]

        self.assertFieldListEqual(ReferrencerClass, expected_list)
