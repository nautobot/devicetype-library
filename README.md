# Nautobot Device Type Library

## About this Library

This library is intended to be used for populating device types in [Nautobot](https://github.com/nautobot/nautobot). It contains a set of device type definitions expressed in YAML and arranged by manufacturer. Each file represents a discrete physical device type (e.g. make and model). These definitions can be loaded into Nautobot instead of creating new device type definitions manually.

If you would like to contribute to this library, please read through our [contributing guide](CONTRIBUTING.md) before submitting content.

## Device Type Definitions

Each definition **must** include at minimum the following fields:

- `manufacturer`: The name of the manufacturer which produces this device type.
  - Type: String
- `model`: The model number of the device type. This must be unique per manufacturer.
  - Type: String

>:test_tube: **Valid Example**:
>```
>manufacturer: Cisco
>model: C9200L-48P-4G
>```

The following fields may **optionally** be declared:

- `part_number`: An alternative representation of the model number (e.g. a SKU). (**Default: None**)
  - Type: String
> :test_tube: **Example**: `part_number: C9200L-48P-4G`
- `u_height`: The height of the device type in rack units. (**Default: 1**)
  - Type: number (minimum of `0`, multiple of `1`)
> :test_tube: **Example**: `u_height: 12`
- `is_full_depth`: A boolean which indicates whether the device type consumes both the front and rear rack faces. (**Default: true**)
  - Type: Boolean
> :test_tube: **Example**: `is_full_depth: false`
- `front_image`: Indicates that this device has a front elevation image within the [elevation-images](elevation-images/) folder. (**Default: None**)
  - NOTE: The elevation images folder requires the same folder name as this device. The file name must also adhere to <model>.front.<acceptable_format>
  - Type: Boolean
> :test_tube: **Example**: `front_image: True`
- `rear_image`: Indicates that this device has a rear elevation image within the [elevation-images](elevation-images/) folder. (**Default: None**)
  - NOTE: The elevation images folder requires the same folder name as this device. The file name must also adhere to <model>.rear.<acceptable_format>
  - Type: Boolean
> :test_tube: **Example**: `rear_image: True`
- `subdevice_role`: Indicates that this is a `parent` or `child` device. (**Default: None**)
  - Type: String
  - Options:
    - `parent`
    - `child`
> :test_tube: **Example**: `subdevice_role: parent`
- `comments`: A string field which allows for comments to be added to the device. (**Default: None**)
  - Type: String
> :test_tube: **Example**: `comments: This is a comment that will appear on all Nautobot devices of this type`

For further detail on these attributes and those listed below, please reference the
[schema definitions](schema/) and the [Component Definitions](#component-definitions) below.

### Component Definitions

Valid component types are listed below. Each type of component must declare a list of the individual component templates
to be added.

- [`console-ports`](#console-ports)
- [`console-server-ports`](#console-server-ports)
- [`power-ports`](#power-ports)
- [`power-outlets`](#power-outlets)
- [`interfaces`](#interfaces)
- [`front-ports`](#front-ports)
- [`rear-ports`](#rear-ports)
- [`device-bays`](#device-bays)
- [`inventory-items`](#inventory-items)

The available fields for each type of component are listed below.

#### Console Ports ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/consoleport/))
> A console port provides connectivity to the physical console of a device. These are typically used for temporary access by someone who is physically near the device, or for remote out-of-band access provided via a networked console server.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `poe`: Does this port access/provide POE? (Boolean)

#### Console Server Ports ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/consoleserverport/))
> A console server is a device which provides remote access to the local consoles of connected devices. They are typically used to provide remote out-of-band access to network devices, and generally connect to console ports.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)

#### Power Ports ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/powerport/))
> A power port is a device component which draws power from some external source (e.g. an upstream power outlet), and generally represents a power supply internal to a device.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `maximum_draw`: The port's maximum power draw, in watts (optional)
- `allocated_draw`: The port's allocated power draw, in watts (optional)

#### Power Outlets ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/poweroutlet/))
> Power outlets represent the outlets on a power distribution unit (PDU) or other device that supplies power to dependent devices. Each power port may be assigned a physical type, and may be associated with a specific feed leg (where three-phase power is used) and/or a specific upstream power port. This association can be used to model the distribution of power within a device.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `power_port`: The name of the power port on the device which powers this outlet (optional)
- `feed_leg`: The phase (leg) of power to which this outlet is mapped; A, B, or C (optional)

#### Interfaces ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/interface/))
> Interfaces in Nautobot represent network interfaces used to exchange data with connected devices. On modern networks, these are most commonly Ethernet, but other types are supported as well. IP addresses and VLANs can be assigned to interfaces.

- `name`: Name
- `label`: Label
- `type`: Interface type slug (Array)
- `mgmt_only`: A boolean which indicates whether this interface is used for management purposes only (default: false)

#### Front Ports ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/frontport/))
> Front ports are pass-through ports which represent physical cable connections that comprise part of a longer path. For example, the ports on the front face of a UTP patch panel would be modeled in Nautobot as front ports. Each port is assigned a physical type, and must be mapped to a specific rear port on the same device. A single rear port may be mapped to multiple front ports, using numeric positions to annotate the specific alignment of each.

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `rear_port`: The name of the rear port on this device to which the front port maps
- `rear_port_position`: The corresponding position on the mapped rear port (default: 1)

#### Rear Ports ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/rearport/))
> Like front ports, rear ports are pass-through ports which represent the continuation of a path from one cable to the next. Each rear port is defined with its physical type and a number of positions: Rear ports with more than one position can be mapped to multiple front ports. This can be useful for modeling instances where multiple paths share a common cable (for example, six discrete two-strand fiber connections sharing a 12-strand MPO cable).

- `name`: Name
- `label`: Label
- `type`: Port type slug (Array)
- `positions`: The number of front ports that can map to this rear port (default: 1)
- `poe`: Does this port access/provide POE? (Boolean)

#### Device Bays ([Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/devicebay/))
>Device bays represent a space or slot within a parent device in which a child device may be installed. For example, a 2U parent chassis might house four individual blade servers. The chassis would appear in the rack elevation as a 2U device with four device bays, and each server within it would be defined as a 0U device installed in one of the device bays. Child devices do not appear within rack elevations or count as consuming rack units.
>
> Child devices are first-class Devices in their own right: That is, they are fully independent managed entities which don't share any control plane with the parent. Just like normal devices, child devices have their own platform (OS), role, tags, and components. LAG interfaces may not group interfaces belonging to different child devices.

- `name`: Name
- `label`: Label

## Data Validation / Commit Quality Checks

There are two ways this repo focuses on keeping quality device-type definitions:

- **Pre-Commit Checks** - Optional, but **highly recommended**, for helping to identify simple issues before committing. (trailing-whitespace, end-of-file-fixer, check-yaml, yamlfmt, yamllint)
  - Installation
    - Virtual Environment Route
      - It is recommended to create a virtual env for your repo (`python3 -m venv .venv && source .venv/bin/activate`)
      - Install the required pip packages (`pip install -r requirements.txt`)
      - Continue to the "Install `pre-commit` Hooks"
    - `pre-commit` Only Route
      - [Install pre-commit](https://pre-commit.com/#install) (`pip install pre-commit`)
    - Install `pre-commit` Hooks
      - To install the pre-commit script: `pre-commit install`
  - Usage & Useful `pre-commit` Commands
    - After staging your files with `git`, to run the pre-commit script on changed files: `pre-commit run`
    - To run the pre-commit script on all files: `pre-commit run --all`
    - To uninstall the pre-commit script: `pre-commit uninstall`
  - Learn more about [pre-commit](https://pre-commit.com/)
- **GitHub Actions** - Automatically run before a PR can be merged. Repeats `yamllint` & validates against Nautobot Device-Type Schema.
