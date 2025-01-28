# **Project Name**

**Influence of Different Music Types on Heartbeat, Reaction Time, and Interoceptive Sensitivity**

## **Project Motivation**

This project aims to analyze the influence of different music types on physiological and behavioral responses, including **heart rate (HR), reaction time (RT), and interoceptive sensitivity (IS)**.  
By combining trial data and PPG recordings, we investigate whether **music stimuli affect physiological changes**.

## **Project Data**

1. **Trial Data (Music Type, Valence Rating, RT)**:  
   [Dataset Link](https://openneuro.org/datasets/ds004894/versions/1.0.0)
2. **PPG and Heartbeat Discrimination Task Data**:  
   [Dataset Link](https://figshare.com/articles/dataset/Heart_rate_and_insula_activity_increase_in_response_to_music_in_individuals_with_high_interoceptive_sensitivity/24874173)

---

## **Data Processing Workflow**

1. **Data Cleaning**  
   - Combine all participant trial data into one Excel file.  
   - Remove incorrect or missing values.  

2. **Data Analysis**  
   - Perform statistical tests (ANOVA, correlation).  
   - Generate visualization graphs.  

---

## **Dataset Description**

The raw dataset includes the following key variables:

### **1. Trial Data**

| Column Name        | Description  |
|--------------------|-------------|
| **session**        | The session number. |
| **music_type**     | The type of music stimulus (tonal, atonal, discord). |
| **valence_rating** | The emotional response strength to the music. |
| **RT**            | Reaction time in milliseconds. |
| **PPG_music_start** | Start time of PPG data at music onset. |
| **PPG_response_start** | Start time of PPG data at response onset. |
| **PPG_ITI_start** | Start time of PPG data during inter-trial intervals. |

### **2. PPG Data**

| Column Name  | Description |
|-------------|-------------|
| **time** | Timestamp of the PPG recording. |
| **PPG**  | The recorded PPG signal. |
| **Note:** The original data was recorded at **1000Hz** but has been **resampled to 100Hz** for efficiency. |

### **3. Heartbeat Discrimination Task Data**

| Column Name      | Description |
|------------------|-------------|
| **delay**       | The delay time condition. |
| **response**    | Participant's response ("sync" or "async"). |
| **confidence**  | Confidence level in the response. |
| **resting_RRI** | Resting RR interval. |

## **Key Variables**

| Variable | Description |
|----------|-------------|
| **Interoceptive Sensitivity (IS)** | Measures a person's ability to perceive internal bodily signals (e.g., heartbeat awareness). It is calculated using a Gaussian fitting model. |

---

## **Implemented Functions**

- **Data Processing:**
  - `filter_to_new_excel()`: Merges trial data files into a single dataset.
  - `match_ppg_data()`: Matches PPG values to trial data.
  - `process_ppg_folder()`: Extracts R-peaks from PPG signals and calculates **heart rate (HR)**.
  - `calculate_is()`: Computes **interoceptive sensitivity (IS)** for each participant.

- **Analysis & Visualization:**
  - `plot_valence_by_music_type()`: Compares **valence rating** across music types.
  - `plot_hr_by_music_type()`: Examines **heart rate (HR)** differences across music types.
  - `analyze_reaction_time_by_music_type()`: Checks if **reaction time (RT)** is affected by music.
  - `analyze_valence_vs_IS()`: Tests correlation between **valence rating and IS**.
  - `analyze_music_type_vs_IS()`: Tests if **IS differs across music types**.

---

## **Results**

- **Valence Rating by Music Type:**  
  Tonal music has **higher valence ratings**, meaning it feels **more positive**, while **atonal and discord music** have lower ratings. Some participants showed **extreme reactions**.

- **Heart Rate by Music Type:**  
  **No significant effect** of music type on heart rate.

- **Reaction Time by Music Type:**  
  Music type **does not** significantly affect reaction time.

- **Interoceptive Sensitivity (IS) by Music Type:**  
  There is **very weak or no correlation** between IS and music type.

- **Valence Rating and IS:**  
  **Weak positive correlation** – people who reacted more emotionally to music **do not necessarily have a higher IS**.

---

## **How to Run the Project**

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
