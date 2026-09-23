# --------------------------------------
# Bluetooth Voltage and Current Monitor
# --------------------------------------

# This program creates a graphical user interface (GUI) for displaying voltage received from an Arduino through Bluetooth.
# Reads voltage data from the HC-05 Bluetooth module and displays live voltage/current values with programmable span and graphs.
# Bluetooth data is received through the macOS screenlog.0 file.

# -------------------------------
# Importing Python Libraries
# -------------------------------

import tkinter as tk
import threading
import time
import re
import os

# deque is used to store a limited number of readings
from collections import deque

# Matplotlib is used to create the live graphs
import matplotlib.pyplot as plt

# Allows Matplotlib graphs to be displayed inside Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Location of the macOS Bluetooth screen log file where received data is stored.
LOG_FILE = os.path.expanduser("~/screenlog.0")


# ---------------------------------
# Default Programmable Span
# ---------------------------------

# Maximum voltage used by the system
max_voltage = 4.0

# Maximum current corresponding to the maximum voltage
max_current = 800.0


# ------------------
# DATA STORAGE
# ------------------

# Store the latest 60 time values
time_data = deque(maxlen=60)

# Store the latest 60 voltage values
voltage_data = deque(maxlen=60)

# Store the latest 60 calculated current values
current_data = deque(maxlen=60)

# Record the time when the program starts
start_time = time.time()

# -------------
# Main window
# -------------

# Create the main Tkinter window
root = tk.Tk()

# Set the title of the application window
root.title("Bluetooth Voltage and Current Monitor")

# Set the size of the application window
root.geometry("1100x700")


# ---------
# Title
# ---------

# Create the main title displayed at the top of the GUI
title = tk.Label(
    root,
    text="Bluetooth Voltage and Current Monitor",
    font=("Arial", 22, "bold")
)

# Display the title
title.pack(pady=12)


# Create a frame to hold the live voltage and current values
values_frame = tk.Frame(root)

values_frame.pack(pady=5)


# Label for live voltage
tk.Label(
    values_frame,
    text="Live Voltage",
    font=("Arial", 14)
).grid(
    row=0,
    column=0,
    padx=50
)


# Label for calculated current
tk.Label(
    values_frame,
    text="Calculated Current",
    font=("Arial", 14)
).grid(
    row=0,
    column=1,
    padx=50
)


# ----------------------
# Voltage Display
# ----------------------

# This label displays the latest voltage received
voltage_label = tk.Label(
    values_frame,
    text="--.-- V",
    font=("Arial", 32, "bold")
)

voltage_label.grid(
    row=1,
    column=0
)


# ---------------------
# Current Display
# ---------------------

# This label displays the calculated current
current_label = tk.Label(
    values_frame,
    text="--- A",
    font=("Arial", 32, "bold")
)

current_label.grid(
    row=1,
    column=1
)


# Create a frame for the programmable span settings
span_frame = tk.Frame(root)

span_frame.pack(pady=5)


# Label for maximum voltage
tk.Label(
    span_frame,
    text="Maximum Voltage (V):",
    font=("Arial", 11)
).grid(
    row=0,
    column=0,
    padx=5
)


# Entry box for maximum voltage
voltage_entry = tk.Entry(
    span_frame,
    width=8,
    font=("Arial", 11)
)

# Set the default maximum voltage to 4 V
voltage_entry.insert(
    0,
    "4.0"
)

voltage_entry.grid(
    row=0,
    column=1,
    padx=5
)


# Label for maximum current
tk.Label(
    span_frame,
    text="Maximum Current (A):",
    font=("Arial", 11)
).grid(
    row=0,
    column=2,
    padx=5
)


# Entry box for maximum current
current_entry = tk.Entry(
    span_frame,
    width=8,
    font=("Arial", 11)
)

# Set the default maximum current to 800 A
current_entry.insert(
    0,
    "800"
)

current_entry.grid(
    row=0,
    column=3,
    padx=5
)


# -------------------
# Status Display
# -------------------

# Displays the currently selected voltage/current span
status_label = tk.Label(
    root,
    text="Span: 4 V = 800 A",
    font=("Arial", 11)
)

status_label.pack()


# Displays the Bluetooth connection status
connection_label = tk.Label(
    root,
    text="Waiting for Bluetooth data...",
    font=("Arial", 11)
)

connection_label.pack(
    pady=3
)


# -------------
# Graphs
# -------------

# Create the Matplotlib figure
figure = plt.Figure(
    figsize=(10, 4),
    dpi=100
)

# Create the voltage graph on the left side
voltage_axis = figure.add_subplot(121)


# Create the current graph on the right side
current_axis = figure.add_subplot(122)


# --------------------------
# Voltage Graph Settings
# --------------------------

voltage_axis.set_title(
    "Live Voltage"
)

voltage_axis.set_xlabel(
    "Time (s)"
)

voltage_axis.set_ylabel(
    "Voltage (V)"
)

# Set voltage graph range from 0 to maximum voltage
voltage_axis.set_ylim(
    0,
    max_voltage
)

# Display grid lines
voltage_axis.grid(
    True
)


# --------------------------
# Current Graph Settings
# --------------------------

current_axis.set_title(
    "Live Current"
)

current_axis.set_xlabel(
    "Time (s)"
)

current_axis.set_ylabel(
    "Current (A)"
)

# Set current graph range from 0 to maximum current
current_axis.set_ylim(
    0,
    max_current
)

# Display grid lines
current_axis.grid(
    True
)


# Adjust spacing between graphs
figure.tight_layout()

# Create a Tkinter canvas containing the Matplotlib figure
canvas = FigureCanvasTkAgg(
    figure,
    master=root
)

# Draw the graph
canvas.draw()

# Add the graph canvas to the GUI
canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=5
)

# -----------------------
# Apply Span Function
# -----------------------

def update_span():

    # Allow the function to change the global span values
    global max_voltage
    global max_current

    try:

        # Read the maximum voltage entered by the user
        new_voltage = float(
            voltage_entry.get()
        )

        # Read the maximum current entered by the user
        new_current = float(
            current_entry.get()
        )

        # Check that the entered values are valid
        if new_voltage > 0 and new_current >= 0:

            # Update maximum voltage
            max_voltage = new_voltage

            # Update maximum current
            max_current = new_current

            # Update the span information shown on screen
            status_label.config(
                text=f"Span: {max_voltage:g} V = {max_current:g} A"
            )

            # Update voltage graph scale
            voltage_axis.set_ylim(
                0,
                max_voltage
            )

            # Update current graph scale
            current_axis.set_ylim(
                0,
                max_current
            )

            # Refresh the graph
            canvas.draw()

    except ValueError:

        # Display an error if the user enters invalid data
        status_label.config(
            text="Please enter valid numbers"
        )


# Create a button to apply the new span settings
apply_button = tk.Button(
    root,
    text="APPLY SPAN",
    command=update_span,
    font=("Arial", 11, "bold")
)

# Display the button
apply_button.pack(
    pady=3
)


# Function to Clear Graph
def clear_graph():

    # Remove all stored time values
    time_data.clear()

    # Remove all stored voltage values
    voltage_data.clear()

    # Remove all stored current values
    current_data.clear()

    # Clear the voltage graph
    voltage_axis.clear()

    voltage_axis.set_title(
        "Live Voltage"
    )

    voltage_axis.set_xlabel(
        "Time (s)"
    )

    voltage_axis.set_ylabel(
        "Voltage (V)"
    )

    # Restore voltage scale
    voltage_axis.set_ylim(
        0,
        max_voltage
    )

    voltage_axis.grid(
        True
    )

    # Clear the current graph
    current_axis.clear()

    current_axis.set_title(
        "Live Current"
    )

    current_axis.set_xlabel(
        "Time (s)"
    )

    current_axis.set_ylabel(
        "Current (A)"
    )

    # Restore current scale
    current_axis.set_ylim(
        0,
        max_current
    )

    current_axis.grid(
        True
    )


    # Adjust graph spacing
    figure.tight_layout()

    # Refresh the GUI
    canvas.draw()

# Create the Clear Graph button
clear_button = tk.Button(
    root,
    text="CLEAR GRAPH",
    command=clear_graph,
    font=("Arial", 11, "bold")
)

# Display the button
clear_button.pack(
    pady=3
)


# -------------------------
# Update Graph Function
# -------------------------
def update_graph():

    # Check whether any data has been received
    if len(time_data) > 0:

        # Clear the previous voltage graph
        voltage_axis.clear()

        # Plot the stored voltage values against time
        voltage_axis.plot(
            list(time_data),
            list(voltage_data)
        )

        voltage_axis.set_title(
            "Live Voltage"
        )

        voltage_axis.set_xlabel(
            "Time (s)"
        )

        voltage_axis.set_ylabel(
            "Voltage (V)"
        )

        # Keep the voltage graph within the selected span
        voltage_axis.set_ylim(
            0,
            max_voltage
        )

        voltage_axis.grid(
            True
        )

        # Clear the previous current graph
        current_axis.clear()

        # Plot the calculated current values against time
        current_axis.plot(
            list(time_data),
            list(current_data)
        )

        current_axis.set_title(
            "Live Current"
        )

        current_axis.set_xlabel(
            "Time (s)"
        )

        current_axis.set_ylabel(
            "Current (A)"
        )

        # Keep the current graph within the selected span
        current_axis.set_ylim(
            0,
            max_current
        )

        current_axis.grid(
            True
        )

        # Adjust graph spacing
        figure.tight_layout()

        # Refresh the graphs
        canvas.draw()

    # Call this function again after 1 second
    # This creates the live graph update.
    root.after(
        1000,
        update_graph
    )

# -------------------------
# Reading Bluetooth Data
# -------------------------
def read_log():

    try:

        # Open the Bluetooth log file
        with open(
            LOG_FILE,
            "r"
        ) as f:

            # Move to the end of the file.
            # This means the program starts reading new bluetooth data rather than old data.
            f.seek(
                0,
                2
            )

            # Update the connection status
            root.after(
                0,
                connection_label.config,
                {
                    "text":
                    "Bluetooth Connected"
                }
            )


            # Continuously monitor the log file
            while True:

                # Read one line from the file
                line = f.readline()


                # Check whether a new line was received
                if line:

                    # Search for the voltage value.
                    match = re.search(
                        r"Voltage\s*=\s*([0-9.]+)",
                        line
                    )


                    # If a voltage value was found
                    if match:

                        # Convert the received voltage from text into a floating-point number.
                        voltage = float(
                            match.group(1)
                        )

                        # --------------------------
                        # Current Calculation
                        # --------------------------
                        
                        current = voltage * (
                            max_current /
                            max_voltage
                        )

                        # Calculate elapsed time since the program started
                        elapsed = (
                            time.time()
                            - start_time
                        )


                        # ----------------
                        # Store Data
                        # ----------------

                        # Store time value
                        time_data.append(
                            elapsed
                        )

                        # Store voltage value
                        voltage_data.append(
                            voltage
                        )

                        # Store calculated current value
                        current_data.append(
                            current
                        )


                        # Update Live Voltage Display


                        root.after(
                            0,
                            voltage_label.config,
                            {
                                "text":
                                f"{voltage:.2f} V"
                            }
                        )

                        # Update Live Current Display

                        root.after(
                            0,
                            current_label.config,
                            {
                                "text":
                                f"{current:.1f} A"
                            }
                        )
                else:

                    # If there is no new data, wait before checking again.
                    time.sleep(
                        0.1
                    )

    # ----------------------
    # Error Handling
    # ----------------------

    except FileNotFoundError:

        # Display an error if screenlog.0 does not exist
        root.after(
            0,
            connection_label.config,
            {
                "text":
                "screenlog.0 not found"
            }
        )


# Create a separate thread for reading Bluetooth data.
thread = threading.Thread(
    target=read_log,
    daemon=True
)

# Start the Bluetooth reading thread
thread.start()

# Start updating the graphs after 1 second
root.after(
    1000,
    update_graph
)

root.mainloop()
