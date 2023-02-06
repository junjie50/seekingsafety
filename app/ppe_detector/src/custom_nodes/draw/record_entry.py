"""
Records check-in entry and saves image with bboxes.
"""

from typing import Any, Dict
from time import time, ctime
from peekingduck.pipeline.nodes.abstract_node import AbstractNode


class Node(AbstractNode):
    """Checks if all PPE is detected and records the check-in entry in
    checkin_records.txt

    Outputs are purely for the draw.legend node to display.

    Inputs:
        |bbox_labels_data|
    
    Outputs:
        |ppe_detected_data|

        |entry_data|

    Configs:
        worker_id (str): default = "PLACEHOLDER_ID"
            Worker's entry is recorded using their worker ID.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """Reads bbox labels and checks that all PPE have been detected.
        Records the check-in entry in txt file.

        Args:
            inputs (dict): Dictionary with keys "bbox_labels".

        Returns:
            outputs (dict): Dictionary with keys "ppe_detected", "entry".
        """

        # Check if all required PPE have been detected (TODO: UPDATE THIS)
        ppe_detected = ("Helmet" in inputs["bbox_labels"]) and ("Safety Vest" in inputs["bbox_labels"])
        
        # Record check-in entry to txt file
        entry_success = "FAILED"
        if ppe_detected:
            entry_success = "SUCCESS"
            print("SUCCESS: All PPE items detected.")
        else:
            print("FAILED: Not all PPE items were detected.")
        entry_record = ctime(time()).replace("  ", " ") # date-time string
        with open('.tmp/checkin_records.txt', 'a+') as f:
            f.write(f"{self.worker_id};{entry_record};{entry_success}\n")

        return{
            "all_ppe_detected": ppe_detected, # for legend node
            "entry": entry_record, # for legend node
            "worker_id": self.worker_id
        }
