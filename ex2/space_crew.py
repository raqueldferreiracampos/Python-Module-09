from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError


class CrewRanks(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def mission_validator(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not any(i.rank in [CrewRanks.COMMANDER,
                              CrewRanks.CAPTAIN] for i in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
                )
        if self.duration_days > 365:
            ok = 0
            for i in self.crew:
                if i.years_experience > 5:
                    ok += 1
            if ok < len(self.crew) / 2:
                raise ValueError(
                    r"Long missions (> 365 days) need 50%"
                    "experienced crew (5+ years)"
                )
        for i in self.crew:
            if i.is_active is False:
                raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    try:
        sarah = CrewMember(
            member_id="A000",
            name="Sarah Connor",
            rank=CrewRanks.COMMANDER,
            age=40,
            specialization="Mission Command",
            years_experience=6
        )
        john = CrewMember(
            member_id="A001",
            name="John Smith",
            rank=CrewRanks.LIEUTENANT,
            age=40,
            specialization="Navigation",
            years_experience=6
        )
        alice = CrewMember(
            member_id="A002",
            name="Alice Johnson",
            rank=CrewRanks.OFFICER,
            age=40,
            specialization="Engineering",
            years_experience=6
        )

        mission_valid = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 3, 3),
            duration_days=900,
            crew=[sarah, john, alice],
            mission_status="planned",
            budget_millions=2500.0
        )

        print(f"Mission: {mission_valid.mission_name}")
        print(f"ID: {mission_valid.mission_id}")
        print(f"Destination: {mission_valid.destination}")
        print(f"Duration: {mission_valid.duration_days} days")
        print(f"Budget: €{mission_valid.budget_millions}M")
        print(f"Crew size: {len(mission_valid.crew)}")
        print("Crew members:")
        for i in mission_valid.crew:
            print(f"- {i.name} ({i.rank.value}) - {i.specialization}")
        print("\n=========================================")

        SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 3, 3),
            duration_days=900,
            crew=[alice],
            mission_status="planned",
            budget_millions=2500.0
        )

    except ValidationError as error:
        print("Expected validation error:")
        for err in error.errors():
            print(err["ctx"]["error"])


if __name__ == "__main__":
    main()
