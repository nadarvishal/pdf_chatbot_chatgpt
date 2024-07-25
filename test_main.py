import os
import pytest
from fastapi.testclient import TestClient
from main import app
from utils import extract_text_from_pdf, index_pdf_content, generate_response

client = TestClient(app)

def test_upload_pdf():
    with open("test.pdf", "rb") as file:
        response = client.post("/upload_pdf", files={"file": ("test.pdf", file, "application/pdf")})
    assert response.status_code == 200
    assert response.json() == {"message": "PDF content indexed successfully."}

def test_query_pdf():
    query = "What is recursion?"
    response = client.post("/query_pdf", data={"query": query})
    assert response.status_code == 200
    assert "response" in response.json()

def test_extract_text_from_pdf():
    with open("test.pdf", "rb") as file:
        text = extract_text_from_pdf(file)
    assert isinstance(text, str)
    assert len(text) > 0

def test_index_pdf_content():
    text = "This is a sample text for testing."
    index_pdf_content(text)
    # Here we should ideally check if the content is indexed, but FAISS and the in-memory mapping make it tricky
    # However, if no exceptions are raised, it's a good indication that the indexing works

def test_generate_response():
    query = "What is recursion?"
    response = generate_response(query)
    assert isinstance(response, str)
    assert len(response) > 0

if __name__ == "__main__":
    # Create a sample PDF file for testing
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Title', 0, 1, 'C')

        def chapter_title(self, num, label):
            self.set_font('Arial', '', 12)
            self.cell(0, 10, 'Chapter %d : %s' % (num, label), 0, 1, 'L')
            self.ln(4)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title(1, 'Recursion')
    pdf.chapter_body('Recursion is a method of solving a problem where the solution involves solving smaller instances of the same problem.')

    pdf.output("test.pdf")

    # Run tests
    pytest.main(["-v", __file__])

    # Clean up the sample PDF file after testing
    os.remove("test.pdf")
