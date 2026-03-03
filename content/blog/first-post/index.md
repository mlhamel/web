+++
title = "Playing with units and measurements in Python"
date = 2026-03-03
description = "A comprehensive comparison of Python libraries for handling units and measurements: Pint, Quantities, Astropy, and Unyt. Learn which library fits your scientific computing needs."
[taxonomies]
tags = ["general"]
+++

When working on data processing and scientific computing tasks, it's often necessary to handle measurements with associated units. This ensures that calculations are performed correctly and that results are meaningful. Python is widly used for such tasks, and there are several libraries available to help manage units and measurements effectively.

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

<!-- result -->

```text
Speed: 0.5 meter / second
Speed in km/h: 1.8 kilometer / hour
```

<!-- end-result -->

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

<!-- result -->

```text
Speed: 0.5 meter / second
Speed in km/h: 1.8 kilometer / hour
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/h
```

<!-- end-result -->

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

<!-- result -->

```text
Speed: 0.5 meter / second
Speed in km/h: 1.8 kilometer / hour
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/h
Speed: 0.5 m / s
Speed in km/h: 1.7999999999999998 km / h
```

<!-- end-result -->

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

<!-- result -->

```text
Speed: 0.5 meter / second
Speed in km/h: 1.8 kilometer / hour
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/h
Speed: 0.5 m / s
Speed in km/h: 1.7999999999999998 km / h
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/hr
Array of speeds: [2. 2. 2. 2. 2.] km/hr
```

<!-- end-result -->

## Polars Integration

Polars is a blazingly fast DataFrame library that focuses on high-performance Arrow-native data types. While it doesn't have native built-in support for units, you can easily integrate unit conversions using helper functions with `map_batches()`.

```python
import polars as pl
import pint

ureg = pint.UnitRegistry()

def convert_units(from_unit: str, to_unit: str):
    """Create a vectorized function to convert units using pint"""
    def converter(s):
        # Convert to NumPy for fast vectorized operations
        vals = s.to_numpy() * ureg(from_unit)
        return pl.Series(vals.to(to_unit).magnitude)
    return converter

# Usage
df = pl.DataFrame({
    "distance_km": [1.0, 2.5, 5.0, 10.0],
    "time_hr": [0.5, 1.0, 1.5, 2.0]
})

df = df.with_columns(
    distance_m = pl.col("distance_km").map_batches(convert_units("km", "m")),
    speed_mps = (pl.col("distance_km") / pl.col("time_hr")).map_batches(convert_units("km/hr", "m/s"))
)

print(df)
```

<!-- result -->

```text
Speed: 0.5 meter / second
Speed in km/h: 1.8 kilometer / hour
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/h
Speed: 0.5 m / s
Speed in km/h: 1.7999999999999998 km / h
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/hr
Array of speeds: [2. 2. 2. 2. 2.] km/hr
shape: (4, 4)
┌─────────────┬─────────┬────────────┬───────────┐
│ distance_km ┆ time_hr ┆ distance_m ┆ speed_mps │
│ ---         ┆ ---     ┆ ---        ┆ ---       │
│ f64         ┆ f64     ┆ f64        ┆ f64       │
╞═════════════╪═════════╪════════════╪═══════════╡
│ 1.0         ┆ 0.5     ┆ 1000.0     ┆ 0.555556  │
│ 2.5         ┆ 1.0     ┆ 2500.0     ┆ 0.694444  │
│ 5.0         ┆ 1.5     ┆ 5000.0     ┆ 0.925926  │
│ 10.0        ┆ 2.0     ┆ 10000.0    ┆ 1.388889  │
└─────────────┴─────────┴────────────┴───────────┘
```

<!-- end-result -->

## Performance Benchmark

When dealing with large datasets or high-frequency calculations, performance becomes a critical factor. Let's compare how these libraries perform for basic scalar and array operations.

```python
import timeit
import numpy as np
from tabulate import tabulate

def benchmark_all():
    # 1. Pint Setup
    import pint
    ureg = pint.UnitRegistry()

    # 2. Quantities Setup
    import quantities as pq

    # 3. Astropy Setup
    from astropy import units as u

    # 4. Unyt Setup
    import unyt

    iterations = 1000
    array_size = 1000
    arr = np.random.random(array_size)

    # Benchmark Scalar Creation & Conversion
    def run_pint_scalar():
        v = (5 * ureg.m) / (10 * ureg.s)
        return v.to(ureg.km / ureg.hr)

    def run_pq_scalar():
        v = (5 * pq.m) / (10 * pq.s)
        return v.rescale(pq.km / pq.hr)

    def run_astropy_scalar():
        v = (5 * u.m) / (10 * u.s)
        return v.to(u.km / u.hr)

    def run_unyt_scalar():
        v = (5 * unyt.m) / (10 * unyt.s)
        return v.to(unyt.km / unyt.hr)

    # Benchmark Array Creation & Arithmetic
    def run_pint_array():
        v = (arr * ureg.m) / (arr * ureg.s)
        return v.to(ureg.km / ureg.hr)

    def run_pq_array():
        v = (arr * pq.m) / (arr * pq.s)
        return v.rescale(pq.km / pq.hr)

    def run_astropy_array():
        v = (arr * u.m) / (arr * u.s)
        return v.to(u.km / u.hr)

    def run_unyt_array():
        v = (arr * unyt.m) / (arr * unyt.s)
        return v.to(unyt.km / unyt.hr)

    libraries = [
        ("Pint", run_pint_scalar, run_pint_array),
        ("Quantities", run_pq_scalar, run_pq_array),
        ("Astropy", run_astropy_scalar, run_astropy_array),
        ("Unyt", run_unyt_scalar, run_unyt_array),
    ]

    table_data = []
    for name, scalar_fn, array_fn in libraries:
        scalar_time = timeit.timeit(scalar_fn, number=iterations)
        array_time = timeit.timeit(array_fn, number=iterations)
        table_data.append([name, f"{scalar_time:.4f}s", f"{array_time:.4f}s"])

    headers = ["Library", f"Scalar ({iterations} iters)", f"Array ({iterations} iters, size {array_size})"]
    print(tabulate(table_data, headers=headers, tablefmt="github"))

benchmark_all()
```

<!-- result -->

```text
Speed: 0.5 meter / second
Speed in km/h: 1.8 kilometer / hour
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/h
Speed: 0.5 m / s
Speed in km/h: 1.7999999999999998 km / h
Speed: 0.5 m/s
Speed in km/h: 1.7999999999999998 km/hr
Array of speeds: [2. 2. 2. 2. 2.] km/hr
shape: (4, 4)
┌─────────────┬─────────┬────────────┬───────────┐
│ distance_km ┆ time_hr ┆ distance_m ┆ speed_mps │
│ ---         ┆ ---     ┆ ---        ┆ ---       │
│ f64         ┆ f64     ┆ f64        ┆ f64       │
╞═════════════╪═════════╪════════════╪═══════════╡
│ 1.0         ┆ 0.5     ┆ 1000.0     ┆ 0.555556  │
│ 2.5         ┆ 1.0     ┆ 2500.0     ┆ 0.694444  │
│ 5.0         ┆ 1.5     ┆ 5000.0     ┆ 0.925926  │
│ 10.0        ┆ 2.0     ┆ 10000.0    ┆ 1.388889  │
└─────────────┴─────────┴────────────┴───────────┘
Traceback (most recent call last):
  File "/home/mlhamel/src/github.com/mlhamel/web/run_md_yarkho5r.py", line 89, in <module>
    from tabulate import tabulate
ModuleNotFoundError: No module named 'tabulate'
```

<!-- end-result -->

## Conclusion

Each of these libraries has its strengths:

- **Pint** is great for general-purpose unit handling with a gentle learning curve.
- **Quantities** excels when you need native NumPy integration for scientific computing.
- **Astropy** is the go-to choice for astronomical calculations with comprehensive unit support.
- **Unyt** provides highly optimized array operations with a focus on astrophysics.

Choose the one that best fits your specific use case and requirements. For most general applications, Pint provides an excellent balance of features and ease of use, while specialized fields might benefit from the more targeted approaches of the other libraries.

### References

- [A Comprehensive Look at Representing Physical Quantities in Python" - SciPy 2013](https://pyvideo.org/scipy-2013/a-comprehensive-look-at-representing-physical-qua.html)

<!--
Dependencies:
requires-python = ">=3.9"
dependencies = [
    "pint",
    "quantities",
    "astropy",
    "unyt",
    "numpy",
    "tabulate",
    "polars"
]
-->
