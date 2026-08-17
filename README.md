# TNE20002 Scenario Calculator

This project contains both a python package that implements the Scenario Calculator and a StreamLit application that
can be installed/used to provide a GUI for students to access the calculator.

## ``tne20002_scenario_calculator`` Package

After installation, two classes can be used, ``Scenario`` and ``AllScenarios``

### ``Scenario``

#### Constructor

<tt>class tne20002_scenario_calculator.<b>Scenario</b>(student_id: <i>str | int</i>, scenario_id: <i>int</i>)

<ul>

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

#### Methods and Properties

<tt>Scenario.<b>id</b></tt>

<ul>

A string containing the student ID associated with the Scenario

</ul>

<tt>Scenario.<b>scenario</b></tt>

<ul>

An integer representing the Scenario number

</ul>

<tt>Scenario.<b>label</b></tt>

<ul>

Scenario Label/description as string

</ul>

<tt>Scenario.<b>vlanxxx</b></tt>

<tt>Scenario.<b>vlanyyy</b></tt>

<tt>Scenario.<b>vlanzzz</b></tt>

<ul>

Calculated VLAN numbers for each of the scenario VLANs

</ul>

<tt>Scenario.<b>corporate_address</b></tt>

<tt>Scenario.<b>isp_address</b></tt>

<ul>

<tt>ipaddress.IPv4Network</tt> instance representing each of the scenario network addresses

</ul>

<tt>Scenario.as_dict()</tt>

<ul>

Dictionary containing calculated parameters that can be used either for display or to generate a CSV file

</ul>

#### Operators

The string representation of a ``Scenario`` instance is a multi-line string displaying all parameters that can be 
printed to screen

### ``AllScenarios``

#### Constructor

<tt>class tne20002_scenario_calculator.<b>AllScenarios</b>(student_id: <i>str | int</i>)

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

#### Methods and Properties

<tt>Scenario.<b>scenarios</b></tt>

<ul>

A dictionary object mapping scenario numbers to <tt>Scenario</tt> instances

</ul>

<tt>Scenario.<b>scenario</b></tt>

<ul>

An integer representing the Scenario number

</ul>

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

