# TNE20002 Scenario Calculator

This project contains both a python package that implements the Scenario Calculator and a StreamLit application that
can be installed/used to provide a GUI for students to access the calculator.

## ``tne20002_scenario_calculator`` Package

After installation, two classes can be used, ``Scenario`` and ``AllScenarios``

### ``Scenario``

Simple example of using the `Scenario` class

```python
>>> from tne20002_scenario_calculator import Scenario

>>> s = Scenario('123456789', 2)
>>> print(s)
Student ID     : 123456789
Scenario       : 2
-----------------------------------------
Corporate Addr : 148.79.0.0/16
ISP Link Addr  : 204.3.58.0/30
VLANXXX        : VLAN789
VLANYYY        : VLAN456
VLANZZZ        : VLAN13
```

#### Constructor

<tt>class tne20002_scenario_calculator.<b>Scenario</b>(student_id: <i>str | int</i>, scenario_id: <i>int</i>)</tt>

<ul>

| Parameter      | Type         | Description                                                              |
|----------------|--------------|--------------------------------------------------------------------------|
| `student_id`   | `str \| int` | Student ID to construct the scenario for, either in string or int format |
| `scenario_id`  | `int`        | Scenario ID to construct                                                 |

Create all parameters for a single scenario

Upon construction, the class will contain all calculated variables/parameters internally which are accessable via properties

> [!WARNING]
> The provided student ID <b>must</b> be one of
>  - A 9-digit number
>  - A 7-digit number
>  - A 6-digit number followed by a 'x' or 'X'

> [!NOTE]
> Creating a <tt>Scenario</tt> may raise an exception
>  - If an invalid student ID is provided, a <tt>StudentIDError</tt> exception will be raised
>  - If an invalid scenario number is provided, a <tt>ValueError</tt> exception will be raised
>  - Provision of invalid types will raise a <tt>TypeError</tt> exception

</ul>

#### Properties

<ul>

| Property                                | Type                    | Description                                                          |
|------------------------------------------------|-------------------------|----------------------------------------------------------------------|
| <code>Scenario.<b>id</b></code>                | `str`                   | A string containing the student ID associated with the Scenario      |
| <code>Scenario.<b>scenario</b></code>          | `int`                   | An integer representing the Scenario number                          |
| <code>Scenario.<b>label</b></code>             | `str`                   | Scenario Label/description as string                                 |
| <code>Scenario.<b>vlanxxx</b></code>           | `int`                   | Calculated VLAN number for VLANXXX in the scenario                   |
| <code>Scenario.<b>vlanyyy</b></code>           | `int`                   | Calculated VLAN number for VLANYYY in the scenario                   |
| <code>Scenario.<b>vlanzzz</b></code>           | `int`                   | Calculated VLAN number for VLANZZZ in the scenario                   |
| <code>Scenario.<b>corporate_address</b></code> | `ipaddress.IPv4Network` | Calculated network address for the Corporate network in the scenario | 
| <code>Scenario.<b>isp_address</b></code>       | `ipaddress.IPv4Network` | Calculated network address for the ISP Link network in the scenario  | 

</ul>

#### Methods

<tt>Scenario.as_dict()</tt>

<ul>

Dictionary containing calculated parameters that can be used either for display or to generate a CSV file

</ul>

#### Operators

The string representation of a ``Scenario`` instance is a multi-line string displaying all parameters that can be 
printed to screen

### <code>class tne20002_scenario_calculator.<b>AllScenarios</b>(student_id: <i>str | int</i>)</code>

#### Constructor

<code>class tne20002_scenario_calculator.<b>AllScenarios</b>(student_id: <i>str | int</i>)</code>

<ul>

Create all <tt>Scenario</tt> instances for a single student ID

Upon construction, the class will contain a dictionary mapping valid scenario numbers to <tt>Scenario</tt> instances for
a single student

> [!WARNING]
> The provided student ID <b>must</b> be one of
>  - A 9-digit number
>  - A 7-digit number
>  - A 6-digit number followed by a 'x' or 'X'

> [!NOTE]
> Creating an <tt>AllScenarios</tt> may raise an exception
>  - If an invalid student ID is provided, a <tt>StudentIDError</tt> exception will be raised

</ul>

#### Properties

| Property                                   | Type                 | Description                                                                |
|--------------------------------------------|----------------------|----------------------------------------------------------------------------|
| <code>AllScenarios.<b>scenarios</b></code> | `dict[int, Scenario` | A dictionary object mapping scenario numbers to `Scenario`</tt>` instances  |

#### Methods


<tt>Scenario.<b>write_csv</b>(path: <i>pathlib.Path</i>)</tt>

<ul>

Write the Scenarios dictionary to a CSV file

</ul>

<tt>Scenario.<b>csv_bytes</b>(scenario: <i>int | None = None</i>)</tt>

<ul>

Write all - or one - scenario(s) to a bytes object as a CSV file that can be saved/streamed (for Streamlit application)

> [!IMPORTANT]
> If <tt>None</tt> is provided as a parameter, <b>all</b> Scenarios will be output to the CSV object. If a valid scenario
> number is provided, <b>only</b> one scenario will be output to the CSV object
 
> [!NOTE]
> Calling this method may raise an exception
>  - If an invalid scenario ID is provided, a <tt>KeyError</tt> exception will be raised

</ul>

## Streamlit App

The streamlit app can be launched from the parent directory via:

``streamlit run app.py``
