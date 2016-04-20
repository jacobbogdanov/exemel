"""Unit tests for the dict2xml module"""

import unittest

import xmlunittest

import dict2xml


class RootElementTestCase(xmlunittest.XmlTestCase):

    def test_default_root(self):
        actual_xml = dict2xml.build({})

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_custom_root(self):
        actual_xml = dict2xml.build({}, root='custom')

        expected_xml = '<custom/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class DictTestCase(xmlunittest.XmlTestCase):

    def test_root_is_empty_dict(self):
        actual_xml = dict2xml.build({})

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_keys_become_sub_elements(self):
        actual_xml = dict2xml.build({
            'alpha': 'a',
            'bravo': 'b'
        })

        expected_xml = """
            <root>
                <alpha>a</alpha>
                <bravo>b</bravo>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_sub_element_is_empty_dict(self):
        actual_xml = dict2xml.build({
            'alpha': {}
        })

        expected_xml = """
            <root>
                <alpha/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class TypesTestCase(xmlunittest.XmlTestCase):

    def test_none_value(self):
        actual_xml = dict2xml.build({
            'alpha': None,
        })

        expected_xml = """
            <root>
                <alpha/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_int_value(self):
        actual_xml = dict2xml.build({
            'alpha': 0,
        })

        expected_xml = """
            <root>
                <alpha>0</alpha>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_float_value(self):
        actual_xml = dict2xml.build({
            'alpha': 1.1,
        })

        expected_xml = """
            <root>
                <alpha>1.1</alpha>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_boolean_values(self):
        actual_xml = dict2xml.build({
            'alpha': True,
            'bravo': False
        })

        expected_xml = """
            <root>
                <alpha>true</alpha>
                <bravo>false</bravo>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class ListTestCase(xmlunittest.XmlTestCase):

    def test_empty_list(self):
        actual_xml = dict2xml.build({
            'myList': []
        })

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_value_items(self):
        actual_xml = dict2xml.build({
            'myList': ['foo', 0, 1.1, True, False, None]
        })

        expected_xml = """
            <root>
                <myList>foo</myList>
                <myList>0</myList>
                <myList>1.1</myList>
                <myList>true</myList>
                <myList>false</myList>
                <myList/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_dict_items(self):
        actual_xml = dict2xml.build({
            'myList': [
                {
                    'alpha': 0,
                    'bravo': 1
                },
                {
                    'alpha': 2,
                    'bravo': 3
                }
            ]
        })

        expected_xml = """
            <root>
                <myList>
                    <alpha>0</alpha>
                    <bravo>1</bravo>
                </myList>
                <myList>
                    <alpha>2</alpha>
                    <bravo>3</bravo>
                </myList>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class AttributeTestCase(xmlunittest.XmlTestCase):

    def test_on_root(self):
        actual_xml = dict2xml.build({
            '@alpha': 'a',
            '@bravo': 'b'
        })

        expected_xml = '<root alpha="a" bravo="b"/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_on_sub_element(self):
        actual_xml = dict2xml.build({
            'child': {
                '@alpha': 'a',
                '@bravo': 'b'
            }
        })

        expected_xml = """
            <root>
                <child alpha="a" bravo="b"/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class NamespaceTestCase(xmlunittest.XmlTestCase):

    def test_on_root(self):
        actual_xml = dict2xml.build({
            '#ns': 'fake:ns'
        })

        expected_xml = '<root xmlns="fake:ns"/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_on_sub_element(self):
        actual_xml = dict2xml.build({
            'child': {
                '#ns': 'fake:ns'
            }
        })

        expected_xml = """
            <root>
                <child xmlns="fake:ns"/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_inherited(self):
        actual_xml = dict2xml.build({
            '#ns': 'fake:ns',
            'child': None
        })

        expected_xml = """
            <f:root xmlns:f="fake:ns">
                <f:child/>
            </f:root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_not_inherited(self):
        actual_xml = dict2xml.build({
            '#ns': 'fake:ns',
            'child': {
                '#ns': None
            }
        })

        expected_xml = """
            <f:root xmlns:f="fake:ns">
                <child/>
            </f:root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_list_items_different_namespaces(self):
        actual_xml = dict2xml.build({
            'myList': [
                {
                    '#ns': 'first:ns'
                },
                {
                    '#ns': 'second:ns'
                }
            ]
        })

        expected_xml = """
            <root>
                <myList xmlns="first:ns"/>
                <myList xmlns="second:ns"/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class TextTestCase(xmlunittest.XmlTestCase):

    def test_on_root(self):
        actual_xml = dict2xml.build({
            '#text': 'foo'
        })

        expected_xml = '<root>foo</root>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_on_sub_element(self):
        actual_xml = dict2xml.build({
            'child': {
                '#text': 'foo'
            }
        })

        expected_xml = """
            <root>
                <child>foo</child>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_int_value(self):
        actual_xml = dict2xml.build({
            '#text': 0
        })

        expected_xml = '<root>0</root>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_float_value(self):
        actual_xml = dict2xml.build({
            '#text': 1.1
        })

        expected_xml = '<root>1.1</root>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_boolean_values(self):
        actual_xml = dict2xml.build({
            'child': [
                {
                    '#text': True
                },
                {
                    '#text': False
                }
            ]
        })

        expected_xml = """
            <root>
                <child>true</child>
                <child>false</child>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_none_value(self):
        actual_xml = dict2xml.build({
            '#text': None
        })

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_text_and_sub_elements(self):
        actual_xml = dict2xml.build({
            'alpha': None,
            '#text': 'foo',
            'bravo': None
        })

        expected_xml = """
            <root>
                foo
                <alpha/>
                <bravo/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


if __name__ == '__main__':
    unittest.main()
