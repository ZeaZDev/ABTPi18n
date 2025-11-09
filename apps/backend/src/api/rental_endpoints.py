"""// ZeaZDev [Rental API Endpoints] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 4) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.services.rental_service import RentalService

router = APIRouter()
rental_service = RentalService()


class CreateContractRequest(BaseModel):
    plan: str
    auto_renew: bool = False


class RenewContractRequest(BaseModel):
    plan: Optional[str] = None


@router.get("/contract")
async def get_user_contract(
    user_id: int = 1  # TODO: Get from auth token
):
    """Get user's current rental contract"""
    try:
        contract = await rental_service.get_user_contract(user_id)
        if not contract:
            return {"message": "No active contract found", "contract": None}
        return {"contract": contract}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/contract")
async def create_contract(
    request: CreateContractRequest,
    user_id: int = 1  # TODO: Get from auth token
):
    """Create a new rental contract"""
    try:
        contract = await rental_service.create_contract(
            user_id=user_id,
            plan=request.plan,
            auto_renew=request.auto_renew
        )
        return contract
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/renew")
async def renew_contract(
    request: RenewContractRequest,
    user_id: int = 1  # TODO: Get from auth token
):
    """Renew user's contract"""
    try:
        contract = await rental_service.renew_contract(
            user_id=user_id,
            plan=request.plan
        )
        return contract
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plans")
async def list_plans():
    """List all available subscription plans"""
    plans = rental_service.list_all_plans()
    return {"plans": plans}


@router.get("/plans/{plan_id}")
async def get_plan_info(plan_id: str):
    """Get information about a specific plan"""
    plan = rental_service.get_plan_info(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"plan": plan}


@router.get("/features")
async def get_contract_features(
    user_id: int = 1  # TODO: Get from auth token
):
    """Get enabled features for current contract"""
    try:
        contract = await rental_service.get_user_contract(user_id)
        if not contract:
            return {"features": []}
        return {"features": contract.get("features", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/has-feature/{feature_name}")
async def check_feature_access(
    feature_name: str,
    user_id: int = 1  # TODO: Get from auth token
):
    """Check if user has access to a specific feature"""
    try:
        has_access = await rental_service.has_feature(user_id, feature_name)
        return {"feature": feature_name, "has_access": has_access}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
