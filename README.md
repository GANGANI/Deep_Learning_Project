# LSTM-Based Modeling: Detecting Social Media Bots Through Behavioral Changes  

This project focuses on detecting social media bots by analyzing user behavior with the **Behavioral Languages for Online Characterization (BLOC)** framework and implementing **deep learning models** like LSTM, GRU, and RNN to capture behavioral dynamics.  

## Features  
- Utilize **BLOC framework** to encode user behavior into symbolic sequences.  
- Tokenizes and encodes user actions, content, and timing for analysis.  
- Models tested:  
  - **RNN**  
  - **LSTM**  
  - **GRU**  
- Compares the performance of models across three BLOC representations:  
  - Action + Pause  
  - Content  
  - Combined (Action + Pause + Content)  

## Dataset  
The dataset used in this project includes labeled social media accounts from the [Bot Repository](https://botometer.osome.iu.edu/bot-repository/), curated between 2017 and 2019. The final dataset contains 55,408 balanced accounts, equally split between bots and humans, and over 10 million tweets.  

### Data Preprocessing  
- Filtered accounts with at least 20 tweets.  
- Limited analysis to the first 300 tweets per account.  
- Tokenization and vocabulary creation for encoding BLOC strings.  

## Models and Results  
| Model | Representation         | Accuracy | F1-Score |  
|-------|-------------------------|----------|----------|  
| RNN   | Action + Pause          | 0.84     | 0.83     |  
|    | Content                 | 0.61     | 0.60     |  
|    | Combined                | 0.83     | 0.83     |  
| LSTM  | Action + Pause          | 0.91     | 0.91     |  
|   | Content                 | 0.90     | 0.90     |  
|   | Combined                | 0.89     | 0.88     |  
| GRU   | Action + Pause          | 0.90     | 0.90     |  
|    | Content                 | 0.89     | 0.89     |  
|    | Combined                | 0.87     | 0.87     |  
