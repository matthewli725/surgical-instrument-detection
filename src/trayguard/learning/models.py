from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Instrument:
    id: str
    display_name: str
    family: str
    aliases: list[str] = field(default_factory=list)
    distinguishing_features: list[str] = field(default_factory=list)
    image_refs: list[dict[str, Any]] = field(default_factory=list)
    study_prompts: list[dict[str, str]] = field(default_factory=list)
    local_verification_status: str = "pending_review"


@dataclass(frozen=True)
class RequiredItem:
    instrument_id: str
    quantity: int
    reference_number: str = ""
    location_or_layer: str = ""
    notes: str = ""


@dataclass(frozen=True)
class LookalikePair:
    id: str
    expected_id: str
    selected_id: str
    feedback_message: str


@dataclass(frozen=True)
class AssessmentVariant:
    id: str
    mode: str
    required_item_ids: list[str]
    distractor_item_ids: list[str]
    random_seed: str
    feedback_enabled: bool


@dataclass(frozen=True)
class MarkerCard:
    marker_id: int
    instrument_id: str
    card_id: str
    role: str = "assessment"


@dataclass(frozen=True)
class TrayModule:
    module_id: str
    version: str
    name: str
    procedure_family: str
    source_note: str
    instruments: dict[str, Instrument]
    required_items: dict[str, RequiredItem]
    distractor_item_ids: list[str]
    lookalike_pairs: list[LookalikePair]
    assessment_variants: dict[str, AssessmentVariant]
    marker_cards: list[MarkerCard]

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "name": self.name,
            "procedure_family": self.procedure_family,
            "source_note": self.source_note,
            "instruments": {key: asdict(value) for key, value in self.instruments.items()},
            "required_items": {key: asdict(value) for key, value in self.required_items.items()},
            "distractor_item_ids": self.distractor_item_ids,
            "lookalike_pairs": [asdict(pair) for pair in self.lookalike_pairs],
            "assessment_variants": {key: asdict(value) for key, value in self.assessment_variants.items()},
            "marker_cards": [asdict(card) for card in self.marker_cards],
        }

    @property
    def marker_map(self) -> dict[int, str]:
        return {card.marker_id: card.instrument_id for card in self.marker_cards}

    @property
    def total_required_units(self) -> int:
        return sum(item.quantity for item in self.required_items.values())


@dataclass(frozen=True)
class DetectedCard:
    marker_id: int
    instrument_id: str | None
    corners: list[list[float]]


@dataclass(frozen=True)
class ItemResult:
    expected_instrument_id: str
    expected_instrument_name: str
    required_quantity: int
    selected_instrument_id: str
    selected_instrument_name: str
    selected_quantity: int
    correct_quantity: int
    error_category: str
    lookalike_pair_id: str
    item_confidence: int | None
    item_uncertainty: bool
    is_high_confidence_error: bool
    is_low_confidence_correct: bool
    feedback_message_id: str


@dataclass(frozen=True)
class AttemptResult:
    run_id: str
    learner_id_hash: str
    participant_group: str
    prior_experience_level: str
    tray_module_id: str
    tray_module_version: str
    assessment_variant_id: str
    mode: str
    started_at: str
    completed_at: str
    duration_seconds: float
    completed_full_flow: bool
    help_requests_count: int
    blocking_help_requests: int
    confidence_scale: str
    overall_confidence: int | None
    total_required_units: int
    selected_units: int
    correct_units: int
    error_points: int
    accuracy_score: float
    required_recall: float
    missing_count: int
    extra_count: int
    wrong_substitution_count: int
    misidentified_count: int
    wrong_count_error_count: int
    not_sure_count: int
    high_confidence_error_count: int
    low_confidence_correct_count: int
    item_results: list[ItemResult]

    def attempt_row(self) -> dict[str, Any]:
        row = asdict(self)
        row.pop("item_results")
        return row
