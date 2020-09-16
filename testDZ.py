# Функциональные тесты:
#
# import pytest
# import settings
#
# url = ""
#
# @pytest.mark.functional
# def test_html(chrome):
#     chrome.get("http://localhost:8000/")
#     assert "My first maket" in chrome.title
#     assert "Progress" in chrome.page_source
#     assert "/s/main.css" in chrome.page_source
#     assert "/i/logo.svg" in chrome.page_source
#     assert (
#         """"<progress id="progress" value="g" max="26">34%<progress>"""
#         in chrome.page_source
#     )
#
# @pytest.mark.functional
#     def test_logo_svg(chrome):
#         chrome.get("http://localhost:8000/i/logo.svg")
#         assert "svg" in chrome.page_source
#         assert "z33" in chrome.page_source
#
# @pytest.mark.functional
#     def test_main_css(chrome, main_css):
#         chrome.get("http://localhost:8000/s/main.css")
#         with (settings.STATIC_PATH / "styles" / "main.css").open("r") as fp:
#             css = fp.read()
#         assert main_css == chrome.page_source
#
