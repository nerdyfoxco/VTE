import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.database import get_db
from db.models import TenantModel

router = APIRouter(prefix="/api/billing", tags=["SaaS Go-To-Market"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")

@router.post("/create-checkout-session")
async def create_checkout_session(tenant_id: str, db: AsyncSession = Depends(get_db)):
    """
    Creates a Stripe Checkout session for a specific PM Firm.
    """
    try:
        # Validate Tenant
        result = await db.execute(select(TenantModel).filter(TenantModel.tenant_id == tenant_id))
        tenant = result.scalars().first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found.")

        # Create Checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=tenant.stripe_customer_id, # Link if they already have one
            line_items=[
                {
                    # In production this maps to a Stripe Price ID (e.g., $1.00 / per unit)
                    'price': os.getenv("STRIPE_PRICE_ID", "price_test_mock"),
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/settings?success=true",
            cancel_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/settings?canceled=true",
            metadata={"tenant_id": tenant_id}
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None), db: AsyncSession = Depends(get_db)):
    """
    Listens for Stripe lifecycle events (Invoice Paid, Subscription Canceled) 
    and mutates the Tenant database state in the VTE Spine.
    """
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Stripe Payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid Stripe Signature")

    # Handle SaaS Lifecycle Gating
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        tenant_id = session.get('metadata', {}).get('tenant_id')
        customer_id = session.get('customer')
        
        # Hydrate the Database
        if tenant_id:
            result = await db.execute(select(TenantModel).filter(TenantModel.tenant_id == tenant_id))
            tenant = result.scalars().first()
            if tenant:
                tenant.stripe_customer_id = customer_id
                tenant.subscription_status = "active"
                await db.commit()

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        customer_id = subscription.get('customer')
        
        # Kill physical operations for this tenant (Gate the OS)
        if customer_id:
             result = await db.execute(select(TenantModel).filter(TenantModel.stripe_customer_id == customer_id))
             tenant = result.scalars().first()
             if tenant:
                  tenant.subscription_status = "canceled"
                  await db.commit()
                  print(f"[BILLING] Tenant {tenant.tenant_id} subscription canceled. VTE Operations Suspended.")

    return {"status": "success"}
