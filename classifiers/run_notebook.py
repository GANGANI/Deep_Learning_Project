import papermill as pm

# Execute the notebook and save the output to a new file
pm.execute_notebook(
    '.rnn/rnn.ipynb',  # Path to the input notebook
    './rnn/output_notebook_v1.ipynb'        # Path to the output notebook
)
