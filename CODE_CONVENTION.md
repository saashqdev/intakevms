# Code convention and configuration linter Ruff and mypy

## Introduction
This document defines the coding standards for our project. Its purpose is to ensure uniformity, readability, and maintainability of the code base. All project participants must follow these rules when writing new code and refactoring existing code.

The basis of our coding style is the Google Python Style Guide. If a specific feature is not described in this document, then the Ruff linter should be used as a guide. If the linter does not take into account the situation that raises questions, you should refer to [Google style management](https://google.github.io/styleguide/pyguide.html).

The guidelines in this document are mandatory. If they conflict with Google's guidelines, the rules described here take precedence.

### Plugins
When developing, it is strongly recommended to use plugins of the corresponding tools in your IDE. Information on their installation is provided in the description of the corresponding tool.

## Ruff Configuration
We use Ruff as our primary tool for linting and formatting code. Ruff's basic settings include:

- Target version Python: 3.12
- Line length: 80 characters
- Indent width: 4 spaces
- Quote style: single quotes
- Indentation style: spaces
- Automatic line ending detection

Ruff is configured to check a wide range of rules, including standard PEP 8 checks, import checks, documentation, type annotations, security, and various style checks.

To run a code review with Ruff, use the following command:
```bash 
ruff check .
```

To automatically correct some errors, use:
```
ruff check --fix .
```

For a detailed introduction to Ruff's functionality and how its commands work, please visit the page [official Ruff documentation](https://docs.astral.sh/ruff/)

### Plugins for popular IDEs
or ease of checking when writing code, we recommend using plugins for official IDEs, having previously configured them. 
The list of supported development environments and their configurations is described on [official page](https://docs.astral.sh/ruff/integrations/)


### Help on linter rules
Help for each of the rules that Ruff works with can be found at [this page](https://docs.astral.sh/ruff/rules/)

### Ignoring linter warnings
Ignoring linter warnings is acceptable in the following cases:

- When following a rule makes the code less readable or the first line of documentation is longer than it should be and there is no way to describe it more concisely.

For example, for documentation, annotations are used at the end of the docstring for this:
noqa: E501, W505

E501 - line-too-long 

W505 - doc-line-too-long

```python
        """Getting all network interfaces and its extra database. VERY LONG FIRST STRING

        Args:
            is_need_filter (Optional[bool]): Flag indicating if it is
                necessary to filter interfaces or not.

        Returns:
            List of serialized dictionaries of interface's data.

        """  # noqa: E501, W505 It is not possible to describe the operation of this method more concisely
```

- When a rule does not apply in a particular context.
- When it makes sense to do so, or when a specific implementation requires it.

Always add a comment explaining why you are ignoring the warning:

```python
# Ignoring the warning about an unused variable, as it is needed for API compatibility
unused_variable = some_function()  # noqa: F841
```

### The process of discussing and changing linter rules
If you feel that a linter rule is inappropriate or needs to be changed, follow this process:

1. Create an issue in the project repository describing the problem and a proposed solution.
2. Provide code examples that demonstrate the problem.
3. Explain why changing the rule will improve the codebase.
4. Wait for the team to discuss and reach consensus.
5. Once approved, make your changes to the Ruff configuration and update this document.

---
## mypy configuration
```mypy``` – is a static type analyzer for Python that helps identify type incompatibility errors before executing your code. We use mypy for strict typing and code quality. Below are the mypy settings used in the project:

### Basic settings
The mypy configuration is located in the mypy.ini file in the project root directory and contains the following parameters:

```ini
[mypy]
warn_return_any = True
warn_unused_configs = True
strict_optional = True
ignore_missing_imports = True
disallow_any_unimported = True
check_untyped_defs = True
disallow_untyped_defs = True
no_implicit_optional = True
show_error_codes = True
warn_unused_ignores = True
exclude = venv|data|intakevms/libs/messaging/protocol\.py
```

### Description of main options
**warn_return_any** = True: Warns if a function is declared to return a value of any type (Any). This helps identify places in the code where the typing of the return value is not strong enough.

**warn_unused_configs** = True: Warns about unused or incorrect settings in the configuration file. This parameter helps to keep the configuration clean and correct.

**strict_optional** = True: Enables strict checking of the use of types that can be None. This ensures that the possible None value in types is handled correctly, avoiding potential errors related to type mismatches.

**ignore_missing_imports** = True: Ignores errors related to missing type annotations in third-party libraries. This is useful if the project uses libraries that do not contain built-in types, and avoids false warnings.

**disallow_any_unimported** = True: Prevents the use of Any values ​​imported from modules that lack type information. This helps make your code more robust and minimizes the risk of errors due to undefined types.

**check_untyped_defs** = True: Analyzes functions and methods without type annotations, identifying possible problems in them. This option allows you to detect errors in code even if some functions do not have type annotations.

**disallow_untyped_defs** = True: Prohibits declarations of functions and methods without type annotations. This is one of the key rules aimed at ensuring strict typing of all code, which significantly increases its reliability and readability.

**no_implicit_optional** = True: Prevents implicit use of Optional for arguments that may be None. Instead, you must explicitly specify Optional, which makes the code more readable and understandable.

**show_error_codes** = True: Shows error codes along with mypy messages. This allows you to quickly find detailed information about the error and understand how to fix it by referring to the official mypy documentation.

**warn_unused_ignores** = True: Warns if # type: ignore comments are used unnecessarily. This helps keep your code clean and avoid unnecessary type checking exceptions.

**exclude = venv|data|intakevms/libs/messaging/protocol\.py:** Excludes certain files and directories from checking, such as the virtual environment (venv), data (data), and a specific file (intakevms/libs/messaging/protocol.py). This allows you to focus on checking only those parts of the code that are important to the project and exclude parts that require refactoring or where dynamic typing is justified.

### Starting mypy

To run code review using the settings described above, activate the project's venv and run the command:

```
mypy .
```

### Ignoring type errors
Sometimes you need to ignore some mypy warnings, for example when working with third-party library code or when using dynamic types. You can use the # type: ignore comment for this:

```python
from external_module import some_function  # type: ignore

result = some_function()  # Ignore the warning about missing type annotations
```

If you ignore a specific warning, always add an explanation to the comment:

```python
from external_module import some_function  # type: ignore[attr-defined]  # Ignore as the library does not provide a type annotation
```

### Additional settings and plugins
ДFor ease of use, mypy can be integrated with various development environments (IDEs), such as PyCharm or VSCode. This allows for automatic type checking as you write code. Detailed information on integration can be found in [official mypy documentation](https://mypy.readthedocs.io/en/stable/config_file.html).

### Discussion and change of rules
If you feel that a mypy rule or setting is inappropriate for a project, follow a discussion process similar to that used for the Ruff linter.:

Create an issue in the project repository describing the problem and proposing a change.
Provide code examples that demonstrate the problem.
Explain why changing the mypy configuration will improve the codebase.
Wait for the team to discuss and reach consensus.
Once approved, make changes to the mypy configuration and update this document.

---
---

# Code convention and general formatting rules

## Line length and hyphenation

The maximum line length is 80 characters. This rule helps keep the code readable and easy to view on most screens.

If the line exceeds this limit, use line breaks. It is preferable to use parentheses for line breaks.

An example of correct transference:

```python
message = (
    f"Storage status is {storage_status} "
    f"but must be in {available_statuses}"
)
```

In some cases it is acceptable to ignore this rule:

For long strings with URLs or file paths.
For strings in multi-line string literals (docstrings or comments).
If you think a line can't be split without losing readability, discuss it with the team. In exceptional cases, you can use the # noqa:E501 comment to ignore the linter warning:
```python
very_long_variable_name = some_long_function_call(arg1, arg2, ...)  # noqa: E501
```

Remember that excessive disregard of the rules can lead to lower code quality. Always strive to adhere to the 80 character limit whenever possible.

## Indents and spaces

ИUse 4 spaces for indentation. Do not use tabs.

```python
def long_function_name(
        var_one: str,
        var_two: str,
        var_three: str,
) -> None:
    print(var_one)
```

If the method signature does not fit into the line length, then you need to use a comma after the last argument and place each argument on a new line:

```python
foo = long_function_name(
    var_one: str, 
    var_two: int,
    var_three: Dict,
    var_four: List,
) -> None:
```

## Import rules
### Import formats
Imports must be on separate lines:

```python
# Right:
import os
import sys

# Wrong:
import os, sys
```

Imports are always placed at the top of the file, immediately after module comments and docstrings, and before global variables and constants.

Imports should be grouped in the following order:

Standard Libraries
Related Third Party Imports
Local application/library imports
You must put a blank line between each group of imports.

### Importing exceptions
Exceptions from the current layer (e.g. service) are imported as just exceptions. Exceptions from packages in another layer or a separate library should be aliased with the _exc suffix:

```python
from intakevms.libs.messaging import exceptions as msg_exc
from intakevms.modules.storage.service_layer import exceptions
```

### Importing Multiple Classes

If you import multiple classes from a package, list them in parentheses, with a new line after the opening parenthesis and a closing line after listing the last class:

```python
from package import (
    Class1,
    Class2,
    Class3,
)
```

## Syntax rules
### Using f-strings and r-strings
Use f-strings exclusively for string formatting. Do not use the format() method or formatting via the % symbol.

```python
# Right:
name = "Alice"
age = 30
message = f"Hello, {name}! You are {age} years old."

# Wrong:
message = "Hello, {}! You are {} years old.".format(name, age)
message = "Hello, %s! You are %d years old." % (name, age)
```
For regular expressions, use r-strings:
```python
import re

pattern = r"\d{3}-\d{2}-\d{4}"
ssn = "123-45-6789"
if re.match(pattern, ssn):
    print("Valid SSN format")
```

### Implementing the super() method
When calling a superclass method, use super() without passing the class name:

```python
class StorageServiceLayerManager(BackgroundTasks):
    def __init__(self):
        super().__init__()

class BridgePortGroup(BasePortGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

```
### Typification (Type hints)
Be sure to use type hints for function arguments, methods, and return values. Use the typing library for complex types.

For dictionaries and similar structures, do not declare nested types for input arguments, but do declare them for return values. If there may be different data types, provide for this in the annotation.

```python
from typing import Dict, Union

def create_partition(self, data: Dict) -> Dict[str, int]:
    # Implementation method

def process_data(self, data: Dict) -> Dict[str, Union[str, int]]:
    # Implementation method
```

## Naming rules
### Classes
Class names must follow the CapWords convention (also known as PascalCase):

```python
class MyClass:
    pass

class MyABCClass:
    pass
```
### Methods and functions

Method and function names must be written in lowercase, with underscores between words:

```python
def my_function():
    pass

class MyClass:
    def my_method(self):
        pass
```

### Variables
Variable names should also be written in lowercase, with underscores between words:

```python
my_variable = 5
user_name = "John"
```
### Constants
Constants must be written in capital letters with underscores between words:

```python
MAX_OVERFLOW = 100
TOTAL = 0
```

## Comments and documentation
Comments must be complete sentences. If the comment is a phrase or sentence, the first word must be capitalized unless it is a variable name that begins with lowercase.

## Formation docstring
Docstring in Python modules is used to document various elements: modules, classes, functions and methods. There are certain rules and recommendations for their design.

### General formatting rules
- Formatting using 4 spaces for indentation.


### Docstring of the module
The module docstring (.py file) must be at the very beginning of the file. It must contain:

- Brief description of the module and its purpose.
- Detailed description of the module's purpose and features of its operation
- Description of the main classes, enumerations, and other entities defined in the module.

When forming a module's docstring, line breaks should be made in such a way that each paragraph (logical group of sentences) is on a separate line. In the case of a break, the content of the new line should be separated by a tab.

#### Example of module docstring:

```python
"""Module for managing the Block Devices Service Layer.

This module defines the `BlockDevicesServiceLayerManager` class, which serves as
the main entry point for handling block device-related operations in the service
layer. The class is responsible for interacting with the domain layer and the
event store to perform various tasks, such as retrieving the host IQN and
managing ISCSI sessions.

The module also includes the `ISCSIInterfaceStatus` enum, which defines the
possible status values for an ISCSI interface, and the `CreateInterfaceInfo`
namedtuple, which is used to store information about a new ISCSI interface.

Classes:
    ISCSIInterfaceStatus: Enum representing the possible status values for an
        ISCSI interface.
    CreateInterfaceInfo: Namedtuple for storing information about a new ISCSI
        interface.
    BlockDevicesServiceLayerManager: Manager class for handling block devices
        service layer operations.
"""
```



### Docstring of classes, functions and methods
For classes, functions and methods, the docstring should be formatted according to Google style:

- The first line should contain a short description. One line that does not exceed the allowed line length. If there is an excess of a small number of characters, it is permissible to add this line to the exceptions for ruff. But it is recommended to find a laconic description for the first line so that it fits into the format.
- A more detailed description follows. It is necessary to adhere to the line length, if a word does not fit, then it is correct to move it to a new line and continue the description there.
- The "Attributes" section should contain a description of the class attributes. It should be separated from the previous description by a blank line.
- The "Args", "Returns" and "Raises" sections should contain a description of the arguments, return value and exceptions respectively. Each section should be separated by a blank line.
- When describing attributes, arguments and potential exceptions, pay attention to the hyphens; for ease of code readability, a hyphenated line that continues the description of a specific element is supplemented with another indent.

An example:
```python
# Incorrect
"""
    ...

    Attributes:
        domain_rpc (RabbitRPCClient): RPC client for communicating with the
        domain layer.
        service_layer_rpc (RabbitRPCClient): RPC client for communicating
        with the API service layer.

"""
# Correctly
"""
    ...

    Attributes:
        domain_rpc (RabbitRPCClient): RPC client for communicating with the
            domain layer.
        service_layer_rpc (RabbitRPCClient): RPC client for communicating
            with the API service layer.
"""
```

#### Example of class docstring:
```python
class BlockDevicesServiceLayerManager(BackgroundTasks):
    """Manager class for handling block devices service layer operations.

    This class is responsible for coordinating the interactions between the
    service layer and the domain layer, as well as the event store, to manage
    block device-related operations.

    Attributes:
        domain_rpc (RabbitRPCClient): RPC client for communicating with the
            domain layer.
        service_layer_rpc (RabbitRPCClient): RPC client for communicating
            with the API service layer.
        uow (SqlAlchemyUnitOfWork): Unit of work for managing database
            transactions.
        event_store (EventCrud): Event store for handling block device-related
            events.
    """

    def __init__(self):
        """Initialize the BlockDevicesServiceLayerManager.

        This method sets up the necessary components for the
        BlockDevicesServiceLayerManager, including the RabbitMQ RPC clients,
        the unit of work, and the event store.
        """
        super().__init__()
        self.domain_rpc: RabbitRPCClient = Protocol(client=True)(
            SERVICE_LAYER_DOMAIN_QUEUE_NAME
        )
        # ...

    def lip_scan(self) -> Dict:
        """Perform a Fibre Channel LIP (Loop Initialization Procedure) scan.

        This method is responsible for initiating a Fibre Channel LIP scan on
        the host system. It communicates with the domain layer to execute the
        LIP scan and returns the result.

        Returns:
            Dict: The result of the Fibre Channel LIP scan.

        Raises:
            FibreChannelLipScanException: If an error occurs during the LIP scan
                process.
        """
        # ...
```
