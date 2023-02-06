from pathlib import Path

from peekingduck.pipeline.nodes.draw import bbox, legend
from peekingduck.pipeline.nodes.input import visual
from peekingduck.runner import Runner
from app.ppe_detector.src.custom_nodes.model import ppe_cv
from app.ppe_detector.src.custom_nodes.draw import record_entry
from app.ppe_detector.src.custom_nodes.output import media_writer_mod



def pkd_checkin(worker_id="PLACEHOLDER_ID", threshold=0.6, source="test_image.png", output_dir="pkd_screenshots", model_path="app/ppe_detector/ppe_od.tflite"):
    """This function runs PeekingDuck CV to detect PPE. If all items are detected, worker's check-in 
    entry is recorded in "checkin_records.txt". Screenshot with bboxes is saved to output directory regardless.
    Will replace input source image if in same directory (as the filename will be the same).

    Args:
        w_id (str): Worker's ID.
        threshold (float): Only consider objects detected with confidence score above threshold
        source (str): File path for input image
        output_dir (str): File directory to store output images
        model_path (str): File path to CV object detection model

    Returns:
        runner (Runner): PKD Runner instance
    """
    # Peeking Duck Set-Up

    visual_node = visual.Node(source=source)
    bbox_node = bbox.Node(show_labels=True)
    record_node = record_entry.Node(worker_id=worker_id, pkd_base_dir=Path.cwd() / "app" / "ppe_detector" / "src" / "custom_nodes")
        # pass in worker id, load before legend node
    cv_node = ppe_cv.Node(score_threshold=threshold, model_path=model_path, pkd_base_dir=Path.cwd() / "app" / "ppe_detector" / "src" / "custom_nodes")
        # pass in threshold and cv model file path
    legend_node = legend.Node(show=["worker_id", "all_ppe_detected", "entry"], font={"size": 1.5, "thickness": 6})
    media_writer_node = media_writer_mod.Node(output_dir=output_dir, pkd_base_dir=Path.cwd() / "app" / "ppe_detector" / "src" / "custom_nodes")
        # pass in output directory

    runner = Runner(
        nodes=[
            visual_node,
            cv_node, # custom object detection model for PPE
            bbox_node,
            record_node, # place before legend node
            legend_node,
            media_writer_node,
        ]
    )

    runner.run()
    return runner # return PKD runner


if __name__ == "__main__":
    # Test PKD runner
    w_id = input("input worker id: ")
    pkd_checkin(worker_id=w_id, threshold=0.3, source="test_image_2.png")
