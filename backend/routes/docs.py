import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List, Dict, Any

from ..config import settings
from ..db import list_frameworks, get_framework, save_doc_file, list_framework_docs, delete_doc_file, save_code_example
from ..agents.doc_parsing_agent import DocParsingAgent
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

router = APIRouter(prefix="/docs", tags=["docs"])

llm_service = LLMService()
rag_service = RAGService(llm_service)

def process_docs_background(doc_id: str, fw_id: str, file_path: str, filename: str, file_format: str):
    try:
        fw = get_framework(fw_id)
        if not fw:
            return
            
        # 1. Parse documentation text & code snippets
        parsed = DocParsingAgent.parse_documentation(file_path, file_format, fw["name"])
        
        # 2. Index raw sections in ChromaDB RAG
        meta = {
            "file_name": filename,
            "topic": "General"
        }
        rag_service.index_doc_file(doc_id, fw_id, parsed["full_text"], meta)
        
        # 3. Save documentation entry in SQLite
        doc_record = {
            "id": doc_id,
            "framework_id": fw_id,
            "file_name": filename,
            "file_path": file_path,
            "file_format": file_format
        }
        save_doc_file(doc_record)
        
        # 4. Save extracted code examples in SQLite
        for ex in parsed["code_examples"]:
            save_code_example(ex)
            
        print(f"Background parsing complete for framework doc {doc_id}")
    except Exception as e:
        print(f"Error processing framework document: {e}")

@router.get("/frameworks")
async def get_frameworks():
    return list_frameworks()

@router.post("/{fw_id}/upload")
async def upload_docs(fw_id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    fw = get_framework(fw_id)
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found.")
        
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["html", "md", "markdown", "pdf", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported documentation file extension.")
        
    doc_id = str(uuid.uuid4())
    safe_filename = f"{doc_id}.{ext}"
    dest_path = settings.UPLOAD_DIR / safe_filename
    
    # Save file
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Trigger background parsing
    background_tasks.add_task(
        process_docs_background,
        doc_id,
        fw_id,
        str(dest_path),
        file.filename,
        ext
    )
    
    return {
        "message": "Documentation uploaded successfully and is being parsed in the background.",
        "doc_id": doc_id
    }

@router.get("/{fw_id}")
async def get_docs(fw_id: str):
    return list_framework_docs(fw_id)

@router.delete("/{doc_id}")
async def remove_doc(doc_id: str):
    delete_doc_file(doc_id)
    rag_service.delete_doc_index(doc_id)
    return {"message": "Documentation deleted successfully."}
