"""
test script for wdp_api_helper functions.
"""
from pathlib import Path
from convenience.wdp_api_helper import write_wdp_api_xml,read_wdp_api_xml

username = "testusername"
password = "testpassword"
xml_file_name = "test.xml"


def test_write_wdp_api_xml():
    """Test write wdp api xml"""
    write_wdp_api_xml(xml_file_name, username,password)
    xml_file = Path('text.xml')

    assert xml_file.exists() is True
    assert username,password == read_wdp_api_xml(xml_file_name)

def test_read_wdp_api_xml():
    """Test write wdp api xml"""
    assert username,password == read_wdp_api_xml(xml_file_name)
