# **Context**:
We have built an application using computer vision to detect if construction worker PPE(Personal Protective Equipment) protocol is being followed diligently. It serves two purposes; it can register the employees’ reporting time and record their shift details when they scan their identity card. The system proceeds to capture an image of the employee and our computer vision model then detects whether the PPE protocols are being complied with. The system can also record a breach of protocols when the employee fails to wear the required equipment and alert the management staff to intervene immediately.

# **Usage**
The software is used when the worker is clocking in for work. The software first capture a photo of the workers along with the nric.

# **Step1 Capture**
![Alt text](assets/imgs/user_camera.png?raw=true "Photo capture page")

The image is then processed via peekingduck to verify if the worker has the correct equipment on.

# **Step2 Process**
![Alt text](.tmp/20230206/S0123456X.png?raw=true "Photo of worker without ppe")

The image above shows a worker without PPE.

![Alt text](.tmp/20230206/S1234567X.png?raw=true "Photo of worker with ppe")

The image above shows a worker with PPE.

# **Step3 Display**
![Alt text](assets/imgs/demo1.png?raw=true "Dashboard for the manager")

The image above shows the dashboard for the manager. Workers without PPE will be highlighted in red to tell the manager that there is a lapse in safety control measures.
The software can be expanded to include Human Resource Management, pay calculation to create an all-in-one software to assist businesses.


# **Benefits**
MOM (Ministry of Manpower) reported falling from heights and vehicular incidents as the top two causes of workplace fatalities as they constituted to 50% of all workplace fatalities. Such mishaps can be easily avoided by wearing the appropriate protective gear. Using our technology can help implementing the safety protocols which can help save lives of so many workers and create a safer workspace. If the our model can help save the life of even a single worker its impact would be invaluable to the worker and their family. Our model could be easily scaled up for various other purposes by re-training it with different datasets. It could be used at laboratories, hospitals, adventure sports and many more places. This could help safeguard the lives of millions of people and their families.

