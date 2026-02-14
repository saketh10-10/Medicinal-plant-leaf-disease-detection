from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import io
import os
import tempfile
import json
from PIL import Image
from predict import predict_image

app = FastAPI(title="Medicinal Plant Analysis API")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class MedicinalProperty(BaseModel):
    name: str
    description: str

class DiseaseInfo(BaseModel):
    name: str
    severity: str
    symptoms: List[str]
    remedies: List[str]

class AnalysisResponse(BaseModel):
    scientific_name: str
    common_name: str
    confidence: float
    medicinal_properties: List[MedicinalProperty]
    plant_health_status: str
    detected_diseases: Optional[List[DiseaseInfo]]
    care_recommendations: List[str]

class PredictionResponse(BaseModel):
    scientific_name: str
    common_name: str
    confidence: float
    medicinal_properties: List[str]
    plant_health_status: str
    detected_diseases: Optional[List[Dict[str, Any]]] = None
    care_recommendations: List[str]

@app.get("/")
async def root():
    return {"message": "Medicinal Plant Analysis API is running!", "version": "1.0.0"}

@app.post("/test-upload")
async def test_upload(file: UploadFile = File(...)):
    """
    Simple test endpoint to verify image upload is working.
    Returns a success message with image details.
    """
    try:
        # Read file contents
        contents = await file.read()
        
        # Get file size
        file_size_kb = len(contents) / 1024
        
        # Try to open as image to validate
        image = Image.open(io.BytesIO(contents))
        width, height = image.size
        
        return {
            "message": "Image received successfully",
            "filename": file.filename,
            "content_type": file.content_type,
            "size_kb": round(file_size_kb, 2),
            "dimensions": f"{width}x{height}",
            "format": image.format
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")


def load_plant_info():
    """Load plant information from JSON file."""
    try:
        with open("plant_info.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Plant information database not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid plant information database")

@app.post("/analyze", response_model=PredictionResponse)
async def analyze_plant(file: UploadFile = File(...)):
    """
    Analyze a plant leaf image to predict the plant disease class.

    Args:
        file: Image file of the plant leaf

    Returns:
        Prediction results with class name, confidence, and class index
    """

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    temp_file_path = None
    try:
        # Read file contents
        contents = await file.read()

        # Validate image can be opened and convert to RGB
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            width, height = image.size
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid or corrupted image: {str(e)}")

        if width < 50 or height < 50:
            raise HTTPException(status_code=400, detail="Image too small. Minimum size: 50x50 pixels")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Call prediction function
        try:
            prediction_result = predict_image(temp_file_path)
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=503, 
                detail=f"Model not found. Please ensure the model file exists: {str(e)}"
            )
        except RuntimeError as e:
            # RuntimeError includes model loading and prediction errors
            error_msg = str(e)
            if "Model file not found" in error_msg or "not found" in error_msg.lower():
                raise HTTPException(status_code=503, detail=error_msg)
            else:
                raise HTTPException(status_code=500, detail=f"Prediction failed: {error_msg}")
        except Exception as e:
            import traceback
            error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            raise HTTPException(
                status_code=500, 
                detail=f"Prediction failed: {str(e)}"
            )

        # Load plant information
        plant_info = load_plant_info()

        # Get information for the predicted class
        class_info = plant_info.get(prediction_result["class_name"], {})

        # Return comprehensive response
        return PredictionResponse(
            scientific_name=class_info.get("scientific_name", "Unknown"),
            common_name=class_info.get("common_name", "Unknown"),
            confidence=prediction_result["confidence"],
            medicinal_properties=class_info.get("medicinal_properties", []),
            plant_health_status=class_info.get("plant_health_status", "Healthy"),
            detected_diseases=class_info.get("detected_diseases"),
            care_recommendations=class_info.get("care_recommendations", [])
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "medicinal-plant-analysis"}

@app.get("/model-status")
async def model_status():
    """Check if model is loaded and ready"""
    try:
        from predict import load_model_and_classes
        model, class_names = load_model_and_classes()
        return {
            "status": "ready",
            "model_loaded": True,
            "num_classes": len(class_names),
            "device": str(model.device) if hasattr(model, 'device') else "unknown",
            "classes": class_names[:5] if len(class_names) > 5 else class_names  # Show first 5
        }
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
