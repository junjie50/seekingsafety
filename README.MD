# **Context**:
We have built an application using computer vision to detect if construction worker PPE(Personal Protective Equipment) protocol is being followed diligently. It serves two purposes; it can register the employees’ reporting time and record their shift details when they scan their identity card. The system proceeds to capture an image of the employee and our computer vision model then detects whether the PPE protocols are being complied with. The system can also record a breach of protocols when the employee fails to wear the required equipment and alert the management staff to intervene immediately.

# **Usage**
The software is used when the worker is clocking in for work. The software first capture a photo of the workers along with the nric.

![Alt text](assets/imgs/user_camera.png?raw=true "Photo capture page")

The image is then processed via peekingduck to verify if the worker has the correct equipment on.

![Alt text](.tmp/20230206/S0123456X.png?raw=true "Photo of worker without ppe")


The image above shows a worker without PPE.

![Alt text](.tmp/20230206/S1234567X.png?raw=true "Photo of worker with ppe")

The image above shows a worker with PPE.

![Alt text](assets/imgs/demon1.png?raw=true "Photo capture page")

The image above shows the dashboard for the manager. The software can be expanded to include Human Resource Management, pay calculation...

