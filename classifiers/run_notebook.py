import papermill as pm

# both action, content
pm.execute_notebook(
    './rnn/only_action_method/rnn.ipynb',  # Path to the input notebook
    './rnn/only_action_method/notebooks/output_notebook_v5(100 epoch).ipynb'        # Path to the output notebook
)

# #  action
# pm.execute_notebook(
#     './rnn/only_action_method/rnn-action.ipynb',  # Path to the input notebook
#     './rnn/only_action_method/notebooks/output_notebook_v3(100 epoch).ipynb'        # Path to the output notebook
# )

# #  content
# pm.execute_notebook(
#     './rnn/only_action_method/rnn-content.ipynb',  # Path to the input notebook
#     './rnn/only_action_method/notebooks/output_notebook_v4(100 epoch).ipynb'        # Path to the output notebook
# )
