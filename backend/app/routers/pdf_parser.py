from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from app.services.pdf_parser import parse_order_pdf

router = APIRouter()

@router.post("/parse-order")
async def parse_order(pdf_file: UploadFile = File(...)):
    """
    Parse uploaded PDF and return structured order data
    """
    if not pdf_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await pdf_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Parse PDF
        order_data = parse_order_pdf(tmp_path)
        
        # Clean up
        os.unlink(tmp_path)
        
        return JSONResponse(content=order_data)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")

