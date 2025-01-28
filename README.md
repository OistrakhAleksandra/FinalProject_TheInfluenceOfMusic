# **Project Name**

Influence of different nusic types on heartbeat, reaction type and interoceptive sensitivity.

# **Projet motivation**

This project aims to analyze the influence of different music types on physiological and behavioral responses, including heart rate, reaction time (RT), and interoceptive sensitivity (IS). By combining and analyzing data from trials and PPG recordings, we investigate correlations between music stimuli and physiological changes.

# **Project Data**

1. Trial data(music type, valemce rating): <https://openneuro.org/datasets/ds004894/versions/1.0.0>
2. PPG and Heartbeat discrimination task data: <https://figshare.com/articles/dataset/Heart_rate_and_insula_activity_increase_in_response_to_music_in_individuals_with_high_interoceptive_sensitivity/24874173>

# **Project Documentation**

1. ## *Clearing data*

  Combinig all the needed data of all trials of every participant into one excel file and cleaning it by deleting incorrect values.
2. ## *Analzing data*
  Making correlation graphs

# **Dataset description (the data were used for analyzes)**

The columns were used in the final excel: session, music_type, valence_rating, RT, PPG_response_start, PPG, IS(Interoceptive sensitivity)

1. ## **Trial Data**

session: The session number.
music_type: The type of music stimulus (tonal, atonal, discord).
valence_rating: The strength of the emotional response to the music.
RT: Reaction time.
PPG_music_start: The start time of PPG data at music onset.
PPG_response_start: The start time of PPG data at response onset.
PPG_ITI_start: The start time of PPG data at the onset of the inter-trial interval.
2. ## **PPG Data**
time: Timestamp of the PPG recording.
PPG: The recorded PPG signal.
3. ## **Heartbeat Discrimination Task Data**
delay: The delay time condition.
response: Participant's response (sync or async).
confidence: Confidence level in the response.
resting_RRI: Resting RR interval.

## **Other important variables:**

1. **Interoceptive Sensitivity (IS)** is the ability to perceive internal bodily signals, like heartbeat, breathing, or hunger. It plays a key role in emotional awareness, physical health, and understanding how the body responds to stress or changes.

# **To run the project follow this commands:**

# **RESULTS**

- **Valence rating to Music type:** Tonal music has higher valence ratings, meaning it feels more positive, while atonal and discord music have lower ratings. However, some participants had extreme reactions.
- **Heart rate to Music type:** No significant effect of music type on heart rate.
- **Reaction type by Music type:** Music type does not have a significant effect on reaction time.
- **Interoceptive sensitivity by Music type:** The correlation between music type and IS is very weak or nonexistent.
- **Valence ratong to IS:** There is a weak positive correlation between mean valence score and IS. This means that people with a stronger emotional reaction do not necessarily have a higher IS.
