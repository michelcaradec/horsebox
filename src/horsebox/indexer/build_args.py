from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

from horsebox.collectors import CollectorType
from horsebox.indexer.analyzer import CustomAnalyzerDef


@dataclass
class IndexBuildArgs:
    """Arguments used to build an index."""

    source: List[str]
    """Locations from which to start indexing."""
    pattern: List[str]
    """The containers to index."""
    collector_type: CollectorType
    """The collector to use."""
    collect_as_jsonl: bool
    """Whether the JSON documents should be collected as JSON Lines or not."""
    custom_analyzer: Optional[CustomAnalyzerDef] = None
    """Custom analyzer."""

    def __post_init__(self) -> None:  # noqa: D105
        # Convert enumerations serialized as a string back to the enumeration type
        self.collector_type = CollectorType(self.collector_type)

        if isinstance(self.custom_analyzer, dict):
            # Create from JSON deserialization
            self.custom_analyzer = CustomAnalyzerDef(**self.custom_analyzer)
