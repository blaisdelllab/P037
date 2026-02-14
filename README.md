# **P037 Suboptimal Choice Task (Sequential Accept–Reject)**

## **Overview**

This repository contains the experimental control software used to run **Project P037**, a sequential accept–reject version of the suboptimal choice task. The experiment was developed and run in Spring 2023 during Dr. Marco Vasconcelos’s sabbatical at UCLA and was used to study suboptimal preferences in pigeons (*Columba livia*) under sequential decision conditions with an optional rejection key.

The entire experiment is implemented in a **single Python script**, which controls stimulus presentation, response collection, reinforcement delivery, and data logging for operant conditioning chambers.

The task includes:
- Instrumental pre-training  
- Forced-choice trials  
- Free-choice trials  
- Rejection trials with optional time costs  

---

## **File Structure**

    P037_ExpProgram_2023-06-09.py
    P037_Settings-Assignments.csv

- **`P037_ExpProgram_2023-06-09.py`**  
  Main experimental control script.

- **`P037_Settings-Assignments.csv`**  
  Subject-specific configuration file specifying hopper durations, rejection costs, stimulus assignments, and side mappings.

---

## **Experimental Design Summary**

Each session consists of **100 trials**, divided into two blocks of 50. Within each block:

- **20 forced-choice trials**
  - 10 informative  
  - 10 non-informative  

- **20 rejection trials**
  - 10 informative + rejection key  
  - 10 non-informative + rejection key  

- **10 free-choice trials**
  - Informative and non-informative options available simultaneously  

Trial types are semi-randomized such that no more than three identical trials occur consecutively.

### **Choice Structure**

- **Informative option**
  - 20% S⁺ → food after terminal delay  
  - 80% S⁻ → no food after terminal delay  

- **Non-informative option**
  - Two terminal stimuli (S1/S2)  
  - Food delivered on 50% of trials regardless of stimulus identity  

- **Rejection option**
  - Allows switching to the alternative option  
  - Can be cost-free or followed by a fixed-time delay  

---

## **Operant Box vs. Test Mode**

At the top of the script, the variable:

    operant_box_version = True

controls whether the program runs in:

- **Operant box mode (`True`)**
  - Enables hardware access (hopper control)  
  - Uses operant-box file paths  
  - Requires custom hopper software  

- **Test / display mode (`False`)**
  - No hardware access  
  - Allows visualization and debugging on standard computers  

This value must be **manually set** before running the experiment.

---

## **Dependencies**

### **Python Version**
- Python **3.11**

### **Standard Library Modules**
- `tkinter`  
- `datetime`  
- `time`  
- `csv`  
- `os`  
- `random`  
- `sys`  

### **External / Lab-Specific Modules (Operant Box Mode Only)**
- `hopper`  
- `polygon_fill`  

These modules resided inside our local directory:

    ~/OneDrive/Desktop/Hopper_Software/

and must be present on operant-box computers. You can access these files within our blasidelllab/Hopper_Software GitHub repository, or replace them with your hardware code. 

---

## **Required Settings File**

The experiment reads subject-specific parameters from:

    P037_Settings-Assignments.csv

Each row corresponds to one subject and includes:
- Subject ID  
- Hopper duration (ms)  
- Rejection FI duration (ms)  
- Side assignment for informative option  
- Color assignments for all terminal stimuli  

The file is loaded at session start and must be present or the program will halt.

---

## **Output Data**

Trial-by-trial data are stored in memory during each session and written to CSV files at the end of the session.

Each row includes:
- Timestamps  
- Screen coordinates  
- Trial number and type  
- Acceptance / rejection indicators  
- Rejection delay duration  
- Reinforcement outcomes  
- Subject ID and training phase  

Column headers are defined explicitly within the script for transparency and reproducibility.

---

## **Running the Experiment**

1. Set `operant_box_version` appropriately.  
2. Confirm that `P037_Settings-Assignments.csv` is present and correctly formatted.  
3. Ensure hopper software is installed (operant boxes only).  
4. Run the script:

    python3 P037_ExpProgram_2023-06-09.py

5. Place the pigeon in the chamber and press the **space bar** to begin the session.

---

## **Authors**
- **Marco Vasconcelos**
- **Cyrus F. Kirkman**  
- **Aaron P. Blaisdell**
- **Armando Machado**

Department of Psychology, UCLA  
William James Center for Research, University of Aveiro  

---

## **Notes**

This code was written for controlled laboratory use and assumes familiarity with operant conditioning procedures, reinforcement schedules, and pigeon touchscreen setups. It is provided as-is for transparency and reproducibility of the associated behavioral findings.
