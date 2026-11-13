from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_contact(self) -> None:
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        if self.contact_type == self.contact_type.physical and self.is_verified is False:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_type == self.contact_type.telepathic and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should include received messages")
    

def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    try:
        alien = AlienContact(
            contact_id="AC_2024_001",
            timestamp=2026-11-5,
            location="Area 51, Nevada",
            contact_type="radio",
            signal_strength="8.5",
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
            )
        print(f"ID: {alien.contact_id}")
        print(f"Type: {alien.contact_type}")
        print(f"Location: {alien.location}")
        print(f"Signal: {alien.signal_strength}")
        print(f"Duration: {alien.duration_minutes} minuts")
        print(f"Witnesses: {alien.witness_count}")
        print(f"Message: {alien.message_received}")
        print("======================================")
        AlienContact(
                    contact_id="AC_2024_001",
                    timestamp=2026-11-5,
                    location="Area 51, Nevada",
                    contact_type="radio",
                    signal_strength="8.5",
                    duration_minutes=45,
                    witness_count=1,
                    message_received="Greetings from Zeta Reticuli"
                    )
    except ValidationError as error:
        print(f"Expected validation error: {error}")
        for error in error.error():
            print(f"{error['ctx']['error']}")


if __name__ == "__main__":
    main()
