<!-- 
Dependencies:
requires-python = ">=3.9"
dependencies = [
    "pint",
]
-->

+++
title = "Playing with units and measurements in Python"
date = 2025-10-29
[taxonomies]
tags = ["general"]
+++

When working on data processing and scientific computing tasks, it's often necessary to handle measurements with associated units. This ensures that calculations are performed correctly and that results are meaningful. Python is widly used for such tasks, and there are several libraries available to help manage units and measurements effectively.

There's different librairies available in Python for handling units and measurements. Some of the most popular ones include:

- **Pint**: A flexible library for defining, operating on, and converting between physical quantities.
- **Quantities**: A library that adds support for physical quantities to NumPy.
- **Astropy**: A library for astronomy that includes support for units and quantities.
- **Unyt**: A library focused on array-based unit handling with strong astrophysics support.

| Feature | Pint | Quantities | Astropy | Unyt |
|---------|------|------------|---------|------|
| Main Focus | General purpose unit handling | Scientific computing with NumPy integration | Astronomical calculations | Array-based calculations with astrophysics focus |
| NumPy Integration | Yes | Native | Yes | Native |
| Unit Definition | Flexible, user-definable | Fixed set | Comprehensive astronomical units | Extensible astronomy units |
| Performance | Good | Very good | Optimized for astronomy | Highly optimized for arrays |
| Learning Curve | Gentle | Moderate | Steeper | Moderate |
| Installation | Lightweight | Requires NumPy | Large package with dependencies | Lightweight |
| Array Operations | Supported | Native | Supported | Native |
| Unit Conversion | Comprehensive | Basic | Comprehensive | Comprehensive |
| Polars Integration | Limited | No | No | Experimental |

## Pint 

Pint is a popular choice for handling units in Python due to its ease of use and flexibility. It allows you to define quantities with units, perform arithmetic operations, and convert between different units seamlessly.

### Example

Here's a simple example using the Pint library to demonstrate how to work with units and measurements in Python:

```python
import pint
# Create a UnitRegistry
ureg = pint.UnitRegistry()
# Define some quantities with units
length = 5 * ureg.meter
time = 10 * ureg.second
# Calculate speed
speed = length / time
print(f"Speed: {speed.to(ureg.meter / ureg.second)}")
# Convert speed to kilometers per hour
speed_kmh = speed.to(ureg.kilometer / ureg.hour)
print(f"Speed in km/h: {speed_kmh}")
```

## Quantities

## Astropy

## Unyt
