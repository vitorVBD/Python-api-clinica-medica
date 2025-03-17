from fastapi import APIRouter
from .Doctor_Controller import router as Doctor_Router
from .Patient_Controller import router as Patient_Router
from .Secretary_Controller import router as Secretary_Router

router = APIRouter()

router.include_router(Doctor_Router, prefix="/doctors", tags=["Doctors"])
router.include_router(Patient_Router, prefix="/patients", tags=["Patients"])
router.include_router(Secretary_Router, prefix="/secretaries", tags=["Secretaries"])