import json
import os
import pytest
from csv2json import convert_csv_to_json

def test_successful_csv_conversion(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age,city\nAlice,30,Lagos\nBob,25,London", encoding="utf-8")
    
    output = convert_csv_to_json(str(csv_file))
    data = json.loads(output)
    
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["city"] == "London"

def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError, match="does not exist"):
        convert_csv_to_json("non_existent_file.csv")

def test_empty_file_raises_error(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("", encoding="utf-8")
    
    with pytest.raises(ValueError, match="completely empty"):
        convert_csv_to_json(str(empty_csv))

def test_custom_output_file_creation(tmp_path):
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "output.json"
    csv_file.write_text("product,price\nLaptop,1000", encoding="utf-8")
    
    res = convert_csv_to_json(str(csv_file), str(json_file))
    assert json_file.exists()
    assert "Successfully converted" in res

def test_bom_header_handling(tmp_path):
    csv_file = tmp_path / "bom.csv"
    # Write UTF-8 with BOM
    csv_file.write_bytes("\xef\xbb\xbfid,val\n1,test".encode("utf-8"))
    
    output = convert_csv_to_json(str(csv_file))
    data = json.loads(output)
    assert "id" in data[0]

def test_semicolon_delimited_csv(tmp_path):
    csv_file = tmp_path / "tsv_data.csv"
    csv_file.write_text("id;name;role\n1;John;Dev", encoding="utf-8")
    
    output = convert_csv_to_json(str(csv_file))
    data = json.loads(output)
    assert data[0]["name"] == "John"
