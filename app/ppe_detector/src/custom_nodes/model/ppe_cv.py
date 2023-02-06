"""
Node that runs custom tflite object detection model.
Detects 'Helmet', 'Safety Vest'
"""

import numpy as np
import tensorflow as tf
from typing import Any, Dict
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

LABELS = ['Helmet', 'Safety Vest'] # classes

class Node(AbstractNode):
    """Initialises and uses tflite object detection model (effnet4) to detect PPE from
    image frame. 

    Inputs:
        |img_data|
    
    Outputs:
        |bboxes_data|

        |bbox_labels_data|

        |bbox_scores_data|

    Configs:
        score_threshold (float): default = 0.5
            Bounding box with confidence score less than the specified
            confidence score threshold is discarded. 
        model_path (str): default = "ppe_od.tflite"
            File path to CV object detection model.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        
        ### Load the TFLITE model
        self.classes = LABELS
        self.DETECTION_THRESHOLD = self.score_threshold # config (default 0.5)
        interpreter = tf.lite.Interpreter(model_path=self.model_path, num_threads=4) # thread count affects inference speed
        interpreter.allocate_tensors()
        
        # Load the input shape required by the model
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
        self.input_size = (input_height, input_width)

        # Run model
        self.signature_fn = interpreter.get_signature_runner()

        self.logger.info(f"CV object detection model file path: {self.model_path}")


    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """Reads the image input and returns the bboxes of the detected PPE.

        Args:
            inputs (dict): Dictionary with key "img".

        Returns:
            outputs (dict): bbox output in dictionary format with keys 
            "bboxes", "bbox_labels", "bbox_scores".
        """

        ### Load & process image data

        # Load image data
        img = inputs["img"] # np array of shape (height,width,channels)
        
        # Process image data
        img = tf.image.convert_image_dtype(img, tf.uint8)
        preprocessed_image = tf.image.resize(img, self.input_size)
        preprocessed_image = preprocessed_image[tf.newaxis, :]
        preprocessed_image = tf.cast(preprocessed_image, dtype=tf.uint8)
        

        ### Detect objects

        # Feed the input preprocessed image to the model
        output = self.signature_fn(images=preprocessed_image) # adds one more dimension to front
        
        # Get all outputs from the model
        count = int(np.squeeze(output['output_0'])) # N (number of objects detected)
        scores = np.squeeze(output['output_1']) # (N,) np array
        classes = np.squeeze(output['output_2']).astype('U6') # (N,) np array
        boxes = np.squeeze(output['output_3']) # (N,4) np array

        # Filter objects that have confidence scores below threshold
        filter_list = [scores[i] >= self.DETECTION_THRESHOLD for i in range(count)]
        scores = scores[filter_list]
        classes = classes[filter_list]
        boxes = boxes[filter_list]

        # Arranging bbox data from (y1,x1,y2,x2) to (x1,y1,x2,y2):
        boxes[:,[0,1]] = boxes[:,[1,0]]
        boxes[:,[2,3]] = boxes[:,[3,2]]

        # Change numerical labels to string labels (0: Helmet 1: Safety Vest)
        classes = classes.astype('U12') # change array dtype from int to string
        classes[classes == '0.0'] = "Helmet"
        classes[classes == '1.0'] = "Safety Vest"

        ### Return outputs
        return {
            "bbox_scores": scores,
            "bbox_labels": classes,
            "bboxes": boxes,
        }