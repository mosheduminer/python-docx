# encoding: utf-8

"""Unit test suite for the docx.parts.story module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.image.image import Image
from docx.package import Package
from docx.parts.document import DocumentPart
from docx.parts.story import BaseStoryPart
from docx.styles.style import BaseStyle

from ..unitutil.file import snippet_text
from ..unitutil.mock import instance_mock, method_mock, property_mock


class DescribeBaseStoryPart(object):

    def it_can_get_a_style_by_id_and_type(
        self, _document_part_prop_, document_part_, style_
    ):
        style_id = "BodyText"
        style_type = WD_STYLE_TYPE.PARAGRAPH
        _document_part_prop_.return_value = document_part_
        document_part_.get_style.return_value = style_
        story_part = BaseStoryPart(None, None, None, None)

        style = story_part.get_style(style_id, style_type)

        document_part_.get_style.assert_called_once_with(style_id, style_type)
        assert style is style_

    def it_can_get_a_style_id_by_style_or_name_and_type(
        self, _document_part_prop_, document_part_, style_
    ):
        style_type = WD_STYLE_TYPE.PARAGRAPH
        _document_part_prop_.return_value = document_part_
        document_part_.get_style_id.return_value = "BodyText"
        story_part = BaseStoryPart(None, None, None, None)

        style_id = story_part.get_style_id(style_, style_type)

        document_part_.get_style_id.assert_called_once_with(style_, style_type)
        assert style_id == "BodyText"

    def it_can_create_a_new_pic_inline(self, get_or_add_image_, image_, next_id_prop_):
        get_or_add_image_.return_value = "rId42", image_
        image_.scaled_dimensions.return_value = 444, 888
        image_.filename = "bar.png"
        next_id_prop_.return_value = 24
        expected_xml = snippet_text("inline")
        story_part = BaseStoryPart(None, None, None, None)

        inline = story_part.new_pic_inline("foo/bar.png", width=100, height=200)

        get_or_add_image_.assert_called_once_with(story_part, "foo/bar.png")
        image_.scaled_dimensions.assert_called_once_with(100, 200)
        assert inline.xml == expected_xml

    def it_knows_the_main_document_part_to_help(self, package_, document_part_):
        package_.main_document_part = document_part_
        story_part = BaseStoryPart(None, None, None, package_)

        document_part = story_part._document_part

        assert document_part is document_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _document_part_prop_(self, request):
        return property_mock(request, BaseStoryPart, "_document_part")

    @pytest.fixture
    def get_or_add_image_(self, request):
        return method_mock(request, BaseStoryPart, "get_or_add_image")

    @pytest.fixture
    def image_(self, request):
        return instance_mock(request, Image)

    @pytest.fixture
    def next_id_prop_(self, request):
        return property_mock(request, BaseStoryPart, "next_id")

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)