import streamlit as st
import pandas as pd
from difflib import SequenceMatcher
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image
import os

from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem.Draw import MolDrawing, DrawingOptions


DrawingOptions.bondLineWidth = 1.8
DrawingOptions.atomLabelFontSize = 14
DrawingOptions.includeAtomNumbers = False

def calculate_match_percentage(input_string, sequence):
    matcher = SequenceMatcher(None, input_string, sequence)
    matching_blocks = matcher.get_matching_blocks()
    total_match_length = sum(block.size for block in matching_blocks)
    match_percentage = (total_match_length / max(len(input_string), len(sequence))) * 100
    return match_percentage

def Smile_String(smile):
    Smile_dict = {
        "A": "CC(C(=O)O)N",
        "C": "CSCC(C(=O)O)N",
        "G": "CC(C(=O)O)C(=O)O",
        "P": "Nc1ccccc1C(=O)O",
        "H": "Nc1c[nH]cn1C(=O)O",
        "I": "CCC(C)C(C(=O)O)N",
        "L": "NCCCCCOHN",
        "M": "CSCCC(C(=O)O)N",
        "S": "OCC(C(=O)O)N",
        "T": "CC(C(=O)O)C(O)N",
        "V": "CCC(C)C(C(=O)O)N",
        "W": "Nc1ccc2c(c1)CCOOHN2",
        "Y": "Nc1ccc(O)cc1C(=O)O"
    }
    return Smile_dict.get(smile, "N/A")

def save_molecule_image(mol, folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    img_path = folder_path + "/" + file_name
    Chem.Draw.MolToFile(mol, img_path)
    return img_path

def main():
    st.title('Bioinformatics Toolbox')

    user_input_sequence = st.text_input('Enter the sequence:', value='', max_chars=100)
    if st.button('Submit'):
        st.subheader('Results:')
        df = pd.read_csv("C:\\Users\\pradeep\\Desktop\\UE DATA.csv")

        max_match_percentage = 0
        best_match = ""

        for index, row in df.iterrows():
            sequence_name = row['SequenceName']
            match_percentage = calculate_match_percentage(user_input_sequence, row['Sequences'])
            if match_percentage > max_match_percentage:
                max_match_percentage = match_percentage
                best_match = sequence_name

        st.write(f"Highest match: {best_match} - {max_match_percentage:.2f}% match")

        combined_smile_string = ""
        for char in user_input_sequence:
            combined_smile_string += Smile_String(char)

        st.write(f"Combined Smile String: {combined_smile_string}")

        if combined_smile_string:
            start_mol = Chem.MolFromSmiles(combined_smile_string)
            if start_mol:
                img_path = save_molecule_image(start_mol, "molecule", "molecule.png")
                image = Image.open(img_path)
                st.image(image, use_column_width=True)

        st.sidebar.subheader('Other Matches:')
        for index, row in df.iterrows():
            sequence_name = row['SequenceName']
            match_percentage = calculate_match_percentage(user_input_sequence, row['Sequences'])
            if sequence_name != best_match:
                st.sidebar.write(f"{sequence_name}: {match_percentage:.2f}% match")

if _name_ == "_main_":
    main()
