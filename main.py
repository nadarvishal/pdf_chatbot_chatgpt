from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from utils import extract_text_from_pdf, index_pdf_content, generate_response

app = FastAPI()

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = extract_text_from_pdf(file.file)
    index_pdf_content(content)
    return {"message": "PDF content indexed successfully."}

@app.post("/query_pdf")
async def query_pdf(query: str = Form(...)):
    response = generate_response(query)
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
