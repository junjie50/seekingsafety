import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import cv2
import numpy as np

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

# role of this node is to be able to take in multiple frames, stitch them
# together and output them.
# to do: need to have 'live' kind of data when there is no filename
# to do: it will be good to have the accepted file format as a configuration
# to do: somewhere so that input and output can use this config for media related issues

class Node(AbstractNode):
    """Outputs the processed image or video to a file. A timestamp is appended to the
    end of the file name.

    Inputs:
        |img_data|

        |filename_data|

        |saved_video_fps_data|

        |pipeline_end_data|

    Outputs:
        |none_output_data|

    Configs:
        output_dir (:obj:`str`): **default = "PeekingDuck/data/output"**. |br|
            Output directory for files to be written locally.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        self.output_dir = Path(self.output_dir)  # type: ignore
        self._file_name: Optional[str] = None
        self._file_path_with_timestamp: Optional[str] = None
        self._image_type: Optional[str] = None
        self.writer = None
        self._prepare_directory(self.output_dir)
        self._fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.logger.info(f"Output directory used is: {self.output_dir}")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Writes media information to filepath."""
        # reset and terminate when there are no more data
        if inputs["pipeline_end"]:
            if self.writer:  # images automatically releases writer
                self.writer.release()
            return {}
        if not self._file_name:
            self._prepare_writer(
                inputs["filename"], inputs["img"], inputs["saved_video_fps"]
            )
        if inputs["filename"] != self._file_name:
            self._prepare_writer(
                inputs["filename"], inputs["img"], inputs["saved_video_fps"]
            )
        self._write(inputs["img"])

        return {}

    def _get_config_types(self) -> Dict[str, Any]:
        """Returns dictionary mapping the node's config keys to respective types."""
        return {"output_dir": str}

    def _write(self, img: np.ndarray) -> None:
        if self._image_type == "image":
            cv2.imwrite(self._file_path_with_timestamp, img)
        else:
            self.writer.write(img)

    def _prepare_writer(
        self, filename: str, img: np.ndarray, saved_video_fps: int
    ) -> None:
        self._file_path_with_timestamp = self._append_datetime_filename(filename)

        if filename.split(".")[-1] in ["jpg", "jpeg", "png"]:
            self._image_type = "image"
        else:
            self._image_type = "video"
            resolution = img.shape[1], img.shape[0]
            self.writer = cv2.VideoWriter(
                self._file_path_with_timestamp,
                self._fourcc,
                saved_video_fps,
                resolution,
            )

    @staticmethod
    def _prepare_directory(output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)

    def _append_datetime_filename(self, filename: str) -> str:
        self._file_name = filename

        return str(self.output_dir / filename)