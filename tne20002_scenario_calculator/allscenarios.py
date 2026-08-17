import io
import csv
import pathlib
from .scenario import Scenario

class AllScenarios():
    def __init__(self, student_id: str | int):
        self.__scenarios: dict[int, Scenario] = {scenario: Scenario(student_id, scenario) for scenario in Scenario.SCENARIO_ID}

    def write_csv(self, path: pathlib.Path):
        with path.open('w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(self.__scenarios[1].as_dict().keys()))
            writer.writeheader()
            writer.writerows(s.as_dict() for s in self.__scenarios.values())

    def csv_bytes(self, scenario: int | None = None) -> bytes:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(self.__scenarios[1].as_dict().keys()))
        writer.writeheader()
        writer.writerows(s.as_dict() for s in self.__scenarios.values() if scenario is None or s.scenario == scenario)
        return buf.getvalue().encode("utf-8")

    @property
    def scenarios(self) -> dict[int, Scenario]:
        return self.__scenarios
