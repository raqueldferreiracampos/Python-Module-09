from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation_Model(BaseModel):
    """Represent a space station with validated operational data."""
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def SpaceStation_print(model: SpaceStation_Model) -> None:
    print(f"ID: {model.station_id}")
    print(f"Name: {model.name}")
    print(f"Crew: {model.crew_size} people")
    print(f"Power: {model.power_level}%")
    print(f"Oxygen: {model.oxygen_level}%")
    if model.is_operational is True:
        print("Status: Operational")
    else:
        print("Status: Not operational")
    if model.notes is not None:
        print(f"Notes: {model.notes}")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    valid_data = SpaceStation_Model(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2026, 11, 12)
    )
    SpaceStation_print(valid_data)
    print("\n========================================")
    try:
        invalid_data = SpaceStation_Model(
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 11, 12)
        )
        SpaceStation_print(invalid_data)
    except ValidationError as error:
        print("Expected validation error:")
        for err in error.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
