"""
Network Routing Principles - Scenario Network Calculator
========================================================
Core logic module (Python port of the Excel workbook).
Import this from the Streamlit app or use the CLI directly.
"""
import ipaddress
import re


class Scenario:
    class StudentIDError(ValueError):
        """Raised when the student ID cannot be normalised to 9 digits."""

        def __init__(self, message: str):
            """
            :param message: Error message indicating reason for failuer
            """
            super().__init__(
                f'{message}: Use 9 digits (873467036), 7 digits (1234567), or 6 digits followed by X (123456X).')

    # List of allowed scenario IDs
    SCENARIO_ID = list(range(1, 7))
    # Map scenario number to a scenario name
    SCENARIO_LABELS = {1: 'Scenario 1: RIP', 2: 'Scenario 2: ACL', 3: 'Scenario 3: EIGRP', 4: 'Scenario 4: OSPF',
                       5: 'Scenario 5: DHCP', 6: 'Scenario 6: NAT', }
    # Illegal / reserved first octets for the /8 scenarios (weeks 5-6)
    _BAD_FIRST_OCTETS = {0, 10, 127}
    # Map scenario number to the initial VLANZZZ number
    _VLANZZZ: dict[int, int] = {1: 256, 2: 130, 3: 112, 4: 154, 5: 195, 6: 516}
    # Map scenario number to the first octet of corporate network address
    _CORPORATE_FIRST_OCTET: dict[int, int] = {1: 158, 2: 148, 3: 131, 4: 145, 5: 0, 6: 0}
    # Map scenario number to the subnet mask prefix of corporate network address
    _CORPORATE_PREFIX: dict[int, int] = {1: 16, 2: 16, 3: 17, 4: 16, 5: 8, 6: 8}
    # Map scenario number to a string containing first two octets of ISP Link Network Address
    _ISP_OCTETS_1_2: dict[int, str] = {1: "201.24", 2: "204.3", 3: "211.13", 4: "211.11", 5: "201.45", 6: "191.22"}
    # Map scenario number to the base value of the third octet of corporate network address
    _ISP_OCTET3_BASE: dict[int, int] = {1: 40, 2: 50, 3: 80, 4: 50, 5: 30, 6: 40}

    def __init__(self, student_id: str | int, scenario_id: int):
        self.__id: str = self._normalise_id(student_id)
        self.__id_digits: list[int] = [int(digit) for digit in self.__id]
        if scenario_id not in self.SCENARIO_ID: raise ValueError(f"Scenario must be one of {', '.join(f'{self.SCENARIO_ID}')}, got {scenario_id!r}.")
        self.__scenario: int = scenario_id
        self.__label: str = self.SCENARIO_LABELS[self.__scenario]
        self.__vlanxxx: int = 0
        self.__vlanyyy: int = 0
        self.__vlanzzz: int = 0

        self._set_vlans()
        self._set_corporate_address()
        self._set_isp_address()

    def _normalise_id(self, student_id: str | int) -> str:
        """
        Normalise any accepted student ID into a 9-digit number. Process for conversion is:
          * Existing 9 digits              123456789  -> 123456789   (used as-is)
          * Existing 7 digits              1234567    -> 991234567   (990000000 + ID)
          * Existing 6 digits + X or x     123456X    -> 991234560   ("99" + 6 digits + "0")

        :param student_id: Student ID to normalise, either in string or int format
        :return: Normalised student ID to nine digits in string form
        :raises StudentIDError: If student ID is invalid
        """
        # Convert provided ID to uppercase string and remove spaces
        clean_id = str(student_id).strip().upper().replace(' ', '')
        if not clean_id: raise Scenario.StudentIDError('Student ID is empty')

        if m := re.fullmatch(r'(\d{9})|(\d{7})|(\d{6})X', clean_id):
            nine_dig, seven_dig, sev_dig_six_dig_x = m.groups()
            if nine_dig: return nine_dig
            if seven_dig: return f'99{seven_dig}'
            if sev_dig_six_dig_x: return f'99{sev_dig_six_dig_x}0'

        raise Scenario.StudentIDError(f'Student ID({student_id}) is not a valid 9-digit student ID')

    def _calc_vlan_id(self, digits: list[int]) -> int:
        """
        Build a 3-digit VLAN ID from three ID digits. If result is <100 (ie. hundreds == 0), then increment by 100

        :param digits: List of three integers indicating which ID digits to use to construct the VLAN ID
        :return: 3-digit integer in range 100-999
        """
        if not isinstance(digits, list): raise TypeError(f'Expected list of digits, got {type(digits)}')
        if len(digits) != 3 or not all(type(x) is int for x in digits): raise ValueError(f'Expected list of three integers for digits, got {digits}')

        return (self.__id_digits[digits[0]] if self.__id_digits[digits[0]] > 0 else 1) * 100 + self.__id_digits[digits[1]] * 10 + self.__id_digits[digits[2]]

    def _set_vlans(self):
        """
        Calculate and set the three VLAN values (XXX, YYY, ZZZ) for the scenario

        Make sure values do not clash
        """
        # Calculate the initial VLAN values
        if self.__scenario in (1, 2, 3):
            self.__vlanxxx = self._calc_vlan_id([6, 7, 8])
            self.__vlanyyy = self._calc_vlan_id([3, 4, 5])
        else:
            self.__vlanxxx = self._calc_vlan_id([4, 5, 6])
            self.__vlanyyy = self._calc_vlan_id([5, 6, 7])

        self.__vlanzzz = self._VLANZZZ[self.__scenario]

        # Resolve clashes
        if self.__vlanxxx == self.__vlanyyy:
            self.__vlanxxx = self.__vlanxxx - 1 if self.__vlanxxx == 999 else self.__vlanxxx + 1

        while self.__vlanzzz in (self.__vlanxxx, self.__vlanyyy):
            self.__vlanzzz = self.__vlanzzz - 3

        validate = {name: value for name, value in {'VLANXXX': self.__vlanxxx, 'VLANYYY': self.__vlanyyy, 'VLANZZZ': self.__vlanzzz}.items() if value < 100 or value > 999}
        if validate:
            raise ValueError(f'Error calculating the following VLANs: {', '.join(f'{name}({value})' for name, value in validate.items())}')

        if len({self.__vlanxxx, self.__vlanyyy, self.__vlanzzz}) != 3:
            raise ValueError(f'VLAN IDs are not unique (VLANXXX={self.__vlanxxx}, VLANYYY={self.__vlanyyy}, VLANZZZ={self.__vlanzzz})')

    def _calc_octet(self, digits: list[int], first_octet: bool) -> int:
        """
        Build an IP address octet from two ID digits. If the octet is supposed to be the first octet, ensure that the number created is not in the
        set of un-allowed octets

        :param digits: List of two integers indicating which ID digits to use to construct the octet
        :param first_octet: Whether the calculated octet will be the first octet in an IP address or not
        :return: Integer in range 0-99
        """
        if not isinstance(digits, list): raise TypeError(f'Expected list of digits, got {type(digits)}')
        if len(digits) != 2 or not all(type(x) is int for x in digits): raise ValueError(f'Expected list of two integers for digits, got {digits}')

        octet = self.__id_digits[digits[0]] * 10 + self.__id_digits[digits[1]]

        if first_octet:
            while octet in self._BAD_FIRST_OCTETS or not 1 <= octet <= 223:
                if octet > 223: octet = octet % 100
                octet += 100

        return octet

    def _validated_net_address(self, address_string: str, label: str) -> ipaddress.IPv4Network:
        """
        Validate a calculated network address and raise an exception if invalid

        :param address_string: String containing network address in slash notation
        :param label: Text label for descriptive purposes
        :return: ipaddress.IPv4Network representing the validated network address
        """
        try:
            net = ipaddress.ip_network(address_string, strict=True)
        except ValueError as e:
            raise ValueError(f'{label} address {address_string} is invalid: {e}')

        first_octet = int(str(net.network_address).split('.')[0])

        if first_octet in self._BAD_FIRST_OCTETS or not 1 <= first_octet <= 223:
            raise ValueError(f'{label} address {address_string} is using a reserved first octet')
        if any(o.lstrip("0") != o and o != "0" for o in address_string.split("/")[0].split(".")):
            raise ValueError(f'{label} address {address_string} has a leading-zero octet.')

        return net

    def _set_corporate_address(self):
        """Calculate and set the Corporate Network address as a string"""
        match self.__scenario:
            case 1 | 2 | 3:
                address = f'{self._CORPORATE_FIRST_OCTET[self.__scenario]}.{self._calc_octet([6, 8], False)}.0.0/{self._CORPORATE_PREFIX[self.__scenario]}'
            case 4:
                address = f'{self._CORPORATE_FIRST_OCTET[self.__scenario]}.{self._calc_octet([6, 4], False)}.0.0/{self._CORPORATE_PREFIX[self.__scenario]}'
            case _:
                address = f'{self._calc_octet([5, 4], True)}.0.0.0/{self._CORPORATE_PREFIX[self.__scenario]}'

        self.__corporate_address = self._validated_net_address(address, 'Corporate')

    def _set_isp_address(self):
        """Calculate and set the ISP Network link address as a string"""
        address = f'{self._ISP_OCTETS_1_2[self.__scenario]}.{self._ISP_OCTET3_BASE[self.__scenario] + self.__id_digits[7]}.0/30'

        self.__isp_address = self._validated_net_address(address, 'ISP')

    def __str__(self) -> str:
        return (
            f'Student ID     : {self.id}\n'
            f'Scenario       : {self.__scenario}\n'
            f"-----------------------------------------\n"
            f"Corporate Addr : {self.__corporate_address}\n"
            f"ISP Link Addr  : {self.__isp_address}\n"
            f"VLANXXX        : VLAN{self.__vlanxxx}\n"
            f"VLANYYY        : VLAN{self.__vlanyyy}\n"
            f"VLANZZZ        : VLAN{self.__vlanzzz}"
        )

    @property
    def id(self) -> str:
        """Student ID"""
        return self.__id

    @property
    def scenario(self) -> int:
        """Scenario number"""
        return self.__scenario

    @property
    def label(self) -> str:
        """Scenario Label as string"""
        return self.__label

    @property
    def vlanxxx(self):
        """Calculated VLANXXX number"""
        return self.__vlanxxx

    @property
    def vlanyyy(self):
        """Calculated VLANYYY number"""
        return self.__vlanyyy

    @property
    def vlanzzz(self):
        """Calculated VLANZZZ number"""
        return self.__vlanzzz

    @property
    def corporate_address(self):
        """Calculated Corporate Network address"""
        return self.corporate_address

    @property
    def isp_address(self):
        """Calculated ISP Network address"""
        return self.isp_address

    def as_dict(self) -> dict:
        """Return a dictionary representation of the calculated scenario"""
        return {'Scenario #': f'Scenario {self.scenario}',
                'ID': self.id,
                'Corporate Net': self.corporate_address,
                'ISP Link (/30)': self.isp_address,
                'VLAN XXX': self.vlanxxx,
                'VLAN YYY': self.vlanyyy,
                'VLAN ZZZ': self.vlanzzz
                }
