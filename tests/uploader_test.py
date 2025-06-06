import os
import shutil

TEST_UPLOAD_DIRECTORY = "uploaded_files"

def test_upload_single_file_success(client):
    file_content = b"Contenido de un archivo de prueba individual."
    file_name = "single_test_file.txt"

    files_to_upload = [("files", (file_name, file_content, "text/plain"))]

    response = client.post("/upload", files=files_to_upload)
    assert response.status_code == 200
    
    uploaded_file_path = os.path.join(TEST_UPLOAD_DIRECTORY, file_name)

    assert os.path.exists(uploaded_file_path)
    with open(uploaded_file_path, "rb") as f:
        assert f.read() == file_content

def test_upload_multiple_files_success(client):
    file1_content = b"Contenido del primer archivo."
    file1_name = "multi_file1.txt"
    file2_content = b"Contenido del segundo archivo."
    file2_name = "multi_file2.png"

    files_to_upload = [
        ("files", (file1_name, file1_content, "text/plain")),
        ("files", (file2_name, file2_content, "image/png"))
    ]

    response = client.post("/upload", files=files_to_upload)
    assert response.status_code == 200

    uploaded_file1_path = os.path.join(TEST_UPLOAD_DIRECTORY, file1_name)
    uploaded_file2_path = os.path.join(TEST_UPLOAD_DIRECTORY, file2_name)

    assert os.path.exists(uploaded_file1_path)
    assert os.path.exists(uploaded_file2_path)

    with open(uploaded_file1_path, "rb") as f:
        assert f.read() == file1_content
    with open(uploaded_file2_path, "rb") as f:
        assert f.read() == file2_content

def test_upload_file_not_provided(client):
    response = client.post("/upload")
    assert response.status_code == 422

def test_upload_file_empty_content(client):
    file_content = b"Contenido de un archivo de prueba individual."
    file_name = "single_test_file.txt"

    files_to_upload = [("files", (file_name, file_content, "text/plain"))]

    response = client.post("/upload", files=files_to_upload)
    assert response.status_code == 200

    uploaded_file_path = os.path.join(TEST_UPLOAD_DIRECTORY, file_name)
    assert os.path.exists(uploaded_file_path)

    with open(uploaded_file_path, "rb") as f:
     assert f.read() == b""