# Smart Gas Valve Control

Control a gas valve based on sensor readings with email notifications.

## Overview

This project uses a Raspberry Pi and a gas sensor to monitor gas levels. If the gas concentration exceeds a certain threshold, the gas valve is closed, and an email notification is sent. The configuration is easily adjustable through a YAML file.

## Features

- GPIO control for gas sensor and relay (for gas valve).
- Email notifications for gas leak alerts.
- Adjustable thresholds and sleep duration through configuration.

## Prerequisites

- Raspberry Pi (or equivalent platform) with GPIO pins.
- Python 3 installed.
- Required Python libraries installed: RPi.GPIO, pyyaml.

## Setup

1. Clone this repository to your Raspberry Pi:

   ```bash
   git clone https://github.com/danielazizyan/smart-gas-valve-control.git
   cd smart-gas-valve-control
2. Install the required Python libraries:

   ```bash
   pip install RPi.GPIO pyyaml

3. Configure the **'config.yaml'** file
4. Run the Python script:
   ```bash
   python gas_valve_control.py

## Logs
Log files are stored in **'gas_valve_control.log'** and provide information about gas levels, valve actions, and email notifications.


