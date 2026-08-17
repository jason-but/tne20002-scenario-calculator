import io
import csv
import pathlib
from .scenario import Scenario

class AllScenarios():
    """
    Constructor, create all the scenarios and store as internal dictionary
    """
    def __init__(self, student_id: str | int):
        self.__scenarios: dict[int, Scenario] = {scenario: Scenario(student_id, scenario) for scenario in Scenario.SCENARIO_ID}

    def write_csv(self, path: pathlib.Path):
        """
        Write the Scenarios dictionary to a CSV file

        :param path: Path to the CSV file to be created
        """
        with path.open('w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(self.__scenarios[1].as_dict().keys()))
            writer.writeheader()
            writer.writerows(s.as_dict() for s in self.__scenarios.values())

    def csv_bytes(self, scenario: int | None = None) -> bytes:
        """
        Write all - or one - scenario(s) to a bytes object as a CSV file that can be saved/streamed (for Streamlit application)

        :param scenario: If provided, this scenario number only will be convered to a CSV file. If None, all scenarios will be convered to a CSV file
        """
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(self.__scenarios[1].as_dict().keys()))
        writer.writeheader()
        writer.writerows(s.as_dict() for s in self.__scenarios.values() if scenario is None or s.scenario == scenario)
        return buf.getvalue().encode("utf-8")

    @property
    def scenarios(self) -> dict[int, Scenario]:
        """Return scenarios dictionary"""
        return self.__scenarios
