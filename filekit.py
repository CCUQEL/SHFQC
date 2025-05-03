
import numpy as np
from tkinter import Tk, filedialog
import ctypes
import csv
from os.path import isdir, join
import os
from datetime import datetime

def get_path(ext: str, title='Select a file path', save_file=False, start_folder=''):
    """Pop up a dialog to browse a file path and return the selected path.

    Example usage:
    >>> from ccukit import get_path
    >>> filepath = get_path('.hdf5', title='MEASUREMENT data', start_folder='C:/Data')

    Parameters
    ----------
    ext : str
        The file extension (including the dot), e.g., '.hdf5'.
    title : str, optional
        The title displayed on the dialog.
    save_file : bool, optional
        If True, open a dialog to select a save path instead of opening a file.
    start_folder : str, optional
        The initial folder where the dialog opens.

    Returns
    -------
    str
        The selected file path. Returns an empty string if the dialog is canceled.
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    dialog = filedialog.asksaveasfilename if save_file else filedialog.askopenfilename

    filepath = dialog(filetypes=[(ext.upper() + ' Files', ext)],
                      title=title,
                      initialdir=start_folder or None)

    return filepath


def get_folderpath(title='Select a folder', start_folder=''):
    """Pop up a dialog to browse and select a folder.

    Example usage:
    >>> folder = get_folderpath(title='Select a data folder', start_folder='C:/Data')

    Args:
        title (str): The title displayed on the dialog.
        start_folder (str): The initial folder where the dialog opens.

    Returns:
        str: The selected folder path. Empty string if canceled.
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folderpath = filedialog.askdirectory(title=title,
                                         initialdir=start_folder or None)
    return folderpath



def save_to_csv(filename, title_array, data_array):
    """Saves the given title_array and data_array to a CSV file with possible unequal column lengths.
        
    Args:
        filename (str): Name of the CSV file to save.
        title_array (list): List containing titles.
        data_array (list or numpy.ndarray): 2D list or numpy array where each sublist represents a column.
        
    Example:
    >>> data1 = np.array([1, 2+1j, 3, 4])
    >>> data2 = [5, 6, 7+2j, 8]
    >>> comments = ['text', 'text2']
    >>> title_array = ["Column 1", "Column 2"]
    >>> data_array = [data1, data2]
    >>> save_to_csv("data.csv", title_array, data_array)
    """
    # Ensure data_array is a numpy array for easier column-wise processing
    data_array = np.array(data_array, dtype=object)
    
    # Find the maximum length of any column
    max_length = max(len(col) for col in data_array)
    
    # Create rows by combining data, filling shorter columns with empty strings
    rows = []
    for i in range(max_length):
        row = []
        for col in data_array:
            row.append(col[i] if i < len(col) else "")  # Add value or empty string if index is out of range
        rows.append(row)
    
    # Write to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(title_array)  # Write the header row
        writer.writerows(rows)  # Write the rows of data


def read_from_csv(filename):
    """Reads a CSV file saved by `save_to_csv` and returns the data as a dictionary.

    Data values are parsed as float first, then complex, finally keep as string.
    Empty string will be deleted from the list.

    Example:
    >>> data = read_from_csv("data.csv")
    >>> print(data)
    OUTPUT: 
    | {'Column 1': array([1., 2., 3., 4.]), 
    |  'Column 2': array([5.+0.j, 6.+0.j, 7.+2.j, 8.+0.j]),
    |  'Column 3': ['text', 'more text', 'final entry', 'last one']}
    """
    result = {}
    
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Read the titles (header)
        titles = next(reader)
        
        # Initialize dictionary with empty lists for each title
        for title in titles:
            result[title] = []
        
        # Read the data rows
        for row in reader:
            for title, value in zip(titles, row):
                if value:
                    # Try converting to float first
                    try:
                        result[title].append(float(value))
                    except ValueError:
                        # If it fails, check if it's a complex
                        try:
                            result[title].append(complex(value))
                        except ValueError:
                            # If it's neither complex nor float, keep it as string
                            result[title].append(value)
                # Skip empty string → don't append anything

        # Clean and convert columns
        for title in result:
            # Remove any empty strings
            cleaned = [val for val in result[title] if val != '']
            if not cleaned:
                result[title] = []  # Leave empty list if nothing left
                continue

            # Determine type of cleaned list
            if all(isinstance(val, float) for val in cleaned):
                result[title] = np.array(cleaned, dtype=float)
            elif all(isinstance(val, (float, complex)) for val in cleaned):
                result[title] = np.array(cleaned, dtype=complex)
            else:
                result[title] = cleaned  # Leave as list of strings

    return result



def get_datafolder_today(database_folder):
    """Get data folder for storing mearuement data, for today's date."""
    # check for the root folder exist
    if not isdir(database_folder):
        raise Exception(f'the labber database folder `{database_folder}` does not exist.')
    
    # check for today's folder exist, create it if not
    yy, mm, dd = datetime.today().strftime('%Y-%m-%d').split('-')
    data_folder_today = join(database_folder, f'{yy}\\{mm}\\Data_{mm}{dd}')
    if not isdir(data_folder_today):
        os.makedirs(data_folder_today)
    return data_folder_today