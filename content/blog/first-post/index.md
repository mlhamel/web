+++
title = "Playing with units and measurements in Python"
date = 2025-10-29
description = "A comprehensive comparison of Python libraries for handling units and measurements: Pint, Quantities, Astropy, and Unyt. Learn which library fits your scientific computing needs."
[taxonomies]
tags = ["general"]
+++

When working on data processing and scientific computing tasks

There's different librairies available in Python for handling units and measurements. Some of the most popular ones include:

- **Pint**: A flexible library for defining, operating on, and converting between physical quantities.
- **Quantities**: A library that adds support for physical quantities to NumPy.
- **Astropy**: A library for astronomy that includes support for units and quantities.
- **Unyt**: A library focused on array-based unit handling with strong astrophysics support.

| Feature            | Pint                          | Quantities                                  | Astropy                          | Unyt                                             |
| ------------------ | ----------------------------- | ------------------------------------------- | -------------------------------- | ------------------------------------------------ |
| Main Focus         | General purpose unit handling | Scientific computing with NumPy integration | Astronomical calculations        | Array-based calculations with astrophysics focus |
| NumPy Integration  | Yes                           | Native                                      | Yes                              | Native                                           |
| Unit Definition    | Flexible, user-definable      | Fixed set                                   | Comprehensive astronomical units | Extensible astronomy units                       |
| Performance        | Good                          | Very good                                   | Optimized for astronomy          | Highly optimized for arrays                      |
| Learning Curve     | Gentle                        | Moderate                                    | Steeper                          | Moderate                                         |
| Installation       | Lightweight                   | Requires NumPy                              | Large package with dependencies  | Lightweight                                      |
| Array Operations   | Supported                     | Native                                      | Supported                        | Native                                           |
| Unit Conversion    | Comprehensive                 | Basic                                       | Comprehensive                    | Comprehensive                                    |
| Polars Integration | Limited                       | No                                          | No                               | Experimental                                     |

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

Using Quantities is another option for handling units in Python, especially if you're working with NumPy arrays. It allows you to perform operations on arrays while keeping track of the associated units.

Here is an example of how to use Quantities:

```python
import quantities as pq
import numpy as np
# Define some quantities with units
length = 5 * pq.meter
time = 10 * pq.second
# Calculate speed
speed = length / time
print(f"Speed: {speed}")
# Convert speed to kilometers per hour
speed_kmh = speed.rescale(pq.kilometer / pq.hour)
print(f"Speed in km/h: {speed_kmh}")
```

## Astropy

Astropy is a powerful library for astronomy that includes support for units and quantities. It provides a comprehensive set of astronomical units and allows you to perform calculations with those units.
Here's an example of how to use Astropy for unit handling:

```python
from astropy import units as u
# Define some quantities with units
length = 5 * u.meter
time = 10 * u.second
# Calculate speed
speed = length / time
print(f"Speed: {speed.to(u.meter / u.second)}")
# Convert speed to kilometers per hour
speed_kmh = speed.to(u.kilometer / u.hour)
print(f"Speed in km/h: {speed_kmh}")
```

## Unyt

Unyt is a library focused on array-based unit handling with strong astrophysics support. It's designed to work seamlessly with NumPy arrays and provides efficient unit operations.

Here's an example of how to use Unyt:

```python
import unyt
import numpy as np
# Define some quantities with units
length = 5 * unyt.meter
time = 10 * unyt.second
# Calculate speed
speed = length / time
print(f"Speed: {speed.to(unyt.meter / unyt.second)}")
# Convert speed to kilometers per hour
speed_kmh = speed.to(unyt.kilometer / unyt.hour)
print(f"Speed in km/h: {speed_kmh}")
# Working with arrays
distances = np.array([1, 2, 3, 4, 5]) * unyt.kilometer
times = np.array([0.5, 1.0, 1.5, 2.0, 2.5]) * unyt.hour
speeds = distances / times
print(f"Array of speeds: {speeds}")
```

## Conclusion

Each of these libraries has its strengths:

- **Pint** is great for general-purpose unit handling with a gentle learning curve
- **Quantities** excels when you need native NumPy integration for scientific computing
- **Astropy** is the go-to choice for astronomical calculations with comprehensive unit support
- **Unyt** provides highly optimized array operations with a focus on astrophysics

Choose the one that best fits your specific use case and requirements. For most general applications, Pint provides an excellent balance of features and ease of use, while specialized fields might benefit from the more targeted approaches of the other libraries.

<!--
Dependencies:
requires-python = ">=3.9"
dependencies = [
    "pint",
    "quantities",
    "astropy",
    "unyt"
]
-->
