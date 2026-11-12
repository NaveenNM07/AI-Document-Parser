from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict


# ==========================================
# Generic API Response Schemas
# ==========================================

class ExtractionResponse(BaseModel):
    filename: str = Field(..., description="Name of the processed PDF file")
    document_type: str = Field(..., description="Document type: invoice or resume")
    status: str = Field(..., description="Processing status: completed or failed")
    parsed_data: Dict[str, Any] = Field(default_factory=dict, description="Extracted JSON data matching schema")
    error: Optional[str] = Field(default=None, description="Error message if processing failed")


# ==========================================
# Invoice Schemas
# ==========================================

class InvoiceItem(BaseModel):
    description: Optional[str] = Field(default=None, description="Description of the item or service")
    quantity: Optional[float] = Field(default=1.0, description="Quantity ordered")
    unit_price: Optional[float] = Field(default=0.0, description="Price per unit")
    amount: Optional[float] = Field(default=0.0, description="Total amount for this line item")


class InvoiceSchema(BaseModel):
    vendor_name: Optional[str] = Field(default=None, description="Name of the company or vendor issuing the invoice")
    invoice_number: Optional[str] = Field(default=None, description="Invoice identifier or number")
    date: Optional[str] = Field(default=None, description="Invoice issue date")
    due_date: Optional[str] = Field(default=None, description="Invoice payment due date")
    items: List[InvoiceItem] = Field(default_factory=list, description="List of line items")
    subtotal: Optional[float] = Field(default=0.0, description="Subtotal amount before tax")
    tax_amount: Optional[float] = Field(default=0.0, description="Tax amount applied")
    total_amount: Optional[float] = Field(default=0.0, description="Final total amount due")


# ==========================================
# Resume Schemas
# ==========================================

class WorkExperience(BaseModel):
    company: Optional[str] = Field(default=None, description="Company or organization name")
    role: Optional[str] = Field(default=None, description="Job title or designation")
    duration: Optional[str] = Field(default=None, description="Employment dates or duration")
    highlights: List[str] = Field(default_factory=list, description="Responsibilities and key achievements")


class ResumeSchema(BaseModel):
    candidate_name: Optional[str] = Field(default=None, description="Full name of the candidate")
    email: Optional[str] = Field(default=None, description="Contact email address")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    skills: List[str] = Field(default_factory=list, description="Technical and soft skills list")
    experience: List[WorkExperience] = Field(default_factory=list, description="Work history details")
    education: List[str] = Field(default_factory=list, description="Degrees, institutions, and education history")