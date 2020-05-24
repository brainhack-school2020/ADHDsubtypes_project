The data used for this project was given by the Centre Alpha-Neuro, a neuropsychology research lab. The data was pre-processed at the lab, 
before we acquired it. Here are the specifications: 
1. Sampling rate 2000 Hz/channel filtered down 250 Hz
2. 19 electrodes cap  using the international 10-20 system (A1 and A2 are for referencing)
3. Recording lasted 5 minutes. Subjects were instructed to fix their gaze on a specific point in front of them on the wall and to move as little 
	as possible, as well as to avoid moving/blinking their eyes.
4. Notch filter 55-65 Hz 
5. Low cut filter 0.3 Hz
6. High cut filter 30 Hz (the reason for such a low filter is that this data is used for neurofeedback protocol creation and Gamma wavebands are not 
	used for neurofeedback)
7. Artifact rejection: software included in the NeuroGuide/WinEEG licensed pack. 
	- Artifact are identified as signal which is higher/lower than the mean signal by 2 standard deviation.
	- Artifact-free epochs are identified when, for a period of at least 1 consecutive second, the signal is equal to or less than 2 standard deviations from the mean amplitude.
	- The selection of artifact-free epochs results in a split-half correlation set at a minimum of 0.9 and a test-retest correlation set at a minimum of 0.9.
	- Of the 5 minutes recorded, 1 minute of artifact free  signal was kept for analysis.
8. Bi-spectral analysis was applied to the artifact free data in order to quantify the different wavebands. The Bi-Spectrum of the instantaneous time series of absolute power, relative power, amplitude
asymmetry, coherence, phase differences and phase reset (1st derivative of straightened phase) were computed. The Bi-Spectrum of the instantaneous time series provides information about the frequency of bursts and the
frequency of changes in coherence and phase and phase reset over long intervals of time. The frequency range is from the Infra-Slow 0.03 Hz to 5.0 Hz. 
9. The absolute power of the following wavebands was then selected for further analysis:
	- Delta (1.0 - 4.0 Hz)
	- Theta (4.0 - 8.0 Hz)
	- Alpha (8.0 - 12.0 Hz)
	- Beta (12.0 - 25.0 Hz)
	- High Beta (25.0 - 30.0 Hz)
	- Gamma (30.0 - 40.0 Hz)
	- High Gamma (40.0 - 50.0Hz)
	- Alpha 1 (8.0 - 10.0 Hz)
	- Alpha 2 (10.0 - 12.0 Hz)
	- Beta 1 (12.0 - 15.0 Hz)
	- Beta 2 (15.0 - 18.0 Hz)
	- Beta 3 (18.0 - 25.0 Hz)
	- Gamma 1 (30.0 - 35.0 Hz)
	- Gamma 2 (35.0 - 40.0 Hz)
