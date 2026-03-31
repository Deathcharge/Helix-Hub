# backend/core/ucf_helpers.py
"""
UCF (Universal Coherence Field) helper functions for Helix v18.0
Provides utilities for reading, calculating, and updating UCF state
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# UCF State file location
UCF_STATE_FILE = Path("Helix/state/ucf_state.json")


def get_current_ucf() -> dict:
    """
    Get current UCF state from file system.

    Returns:
        Dictionary with UCF dimensions (harmony, resilience, throughput, focus, friction, velocity)
    """
    try:
        if UCF_STATE_FILE.exists():
            with open(UCF_STATE_FILE, encoding="utf-8") as f:
                ucf_state = json.load(f)
            return ucf_state
        else:
            # Return default balanced state
            logger.warning("UCF state file not found, returning default state")
            return get_default_ucf()
    except Exception as e:
        logger.error("Error reading UCF state: %s", e)
        return get_default_ucf()


def get_default_ucf() -> dict:
    """
    Get default balanced UCF state.

    Returns:
        Default UCF state with balanced values
    """
    return {
        "harmony": 0.75,
        "resilience": 0.70,
        "throughput": 0.65,
        "focus": 0.60,
        "friction": 0.20,  # Lower is better for friction (obstacles)
        "velocity": 0.50,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def calculate_performance_score(ucf_state: dict) -> float:
    """
    Calculate overall coordination level from UCF dimensions.

    Formula: Average of positive dimensions - friction penalty

    Args:
        ucf_state: UCF state dictionary

    Returns:
        Coordination level (0.0-10.0 scale)
    """
    try:
        harmony = ucf_state.get("harmony", 0.5)
        resilience = ucf_state.get("resilience", 0.5)
        throughput = ucf_state.get("throughput", 0.5)
        focus = ucf_state.get("focus", 0.5)
        friction = ucf_state.get("friction", 0.5)
        velocity = ucf_state.get("velocity", 0.5)

        # Average of positive dimensions
        positive_avg = (harmony + resilience + throughput + focus + velocity) / 5

        # Friction acts as a penalty (lower is better)
        friction_penalty = friction * 0.3

        # Calculate coordination level (0.0-10.0 scale)
        coordination = (positive_avg - friction_penalty) * 10

        # Clamp to valid range
        return max(0.0, min(10.0, coordination))

    except Exception as e:
        logger.error("Error calculating coordination level: %s", e)
        return 5.0  # Return mid-point on error


def update_ucf_state(ucf_state: dict, save_to_file: bool = True) -> bool:
    """
    Update UCF state in memory and optionally save to file.

    Args:
        ucf_state: New UCF state dictionary
        save_to_file: Whether to persist to disk

    Returns:
        True if successful, False otherwise
    """
    try:
        if "timestamp" not in ucf_state:
            ucf_state["timestamp"] = datetime.now(UTC).isoformat()

        if save_to_file:
            # Ensure directory exists
            UCF_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

            # Write to file
            with open(UCF_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(ucf_state, f, indent=2)

            logger.debug("UCF state updated: coordination=%.2f", calculate_performance_score(ucf_state))

        # Also update cache if Redis is available (optional)
        try:
            from helix_core.utils import RedisCache
            RedisCache.set_ucf_state(ucf_state)
        except (ImportError, ModuleNotFoundError):
            logger.debug("Redis cache not available - skipping cache update")
        except (ValueError, TypeError, KeyError, IndexError) as e:
            logger.debug("Redis cache update skipped: %s", e)

        return True

    except Exception as e:
        logger.error("Error updating UCF state: %s", e)
        return False


def classify_coordination_state(performance_score: float) -> str:
    """
    Classify coordination level into named states.

    Args:
        performance_score: Coordination level (0.0-10.0)

    Returns:
        State classification string
    """
    if performance_score >= 9.0:
        return "TRANSCENDENT"
    elif performance_score >= 7.5:
        return "ELEVATED"
    elif performance_score >= 6.0:
        return "OPERATIONAL"
    elif performance_score >= 4.0:
        return "STABLE"
    elif performance_score >= 2.5:
        return "CHALLENGED"
    else:
        return "CRISIS"


def get_ucf_with_classification() -> dict:
    """
    Get current UCF state with coordination level and classification.

    Returns:
        UCF state with added performance_score and state_classification fields
    """
    ucf_state = get_current_ucf()
    performance_score = calculate_performance_score(ucf_state)
    state_classification = classify_coordination_state(performance_score)

    return {
        **ucf_state,
        "performance_score": round(performance_score, 2),
        "state_classification": state_classification,
    }


def validate_ucf_dimensions(ucf_state: dict) -> bool:
    """
    Validate that the provided UCF state contains all required dimensions with numeric values between 0.0 and 1.0.

    Parameters:
        ucf_state (Dict): Mapping containing UCF dimension keys and their numeric values.

    Returns:
        bool: `True` if all required dimensions are present and each value is between 0.0 and 1.0 (inclusive), `False` if any dimension is missing, any value is invalid, or an error occurs during validation.
    """
    required_dimensions = [
        "harmony",
        "resilience",
        "throughput",
        "focus",
        "friction",
        "velocity",
    ]

    try:
        for dim in required_dimensions:
            if dim not in ucf_state:
                logger.warning("Missing UCF dimension: %s", dim)
                return False

            # Check values are in valid range (0.0-1.0)
            value = ucf_state[dim]
            if not isinstance(value, (int, float)) or value < 0.0 or value > 1.0:
                logger.warning("Invalid UCF dimension value: %s=%s", dim, value)
                return False

        return True

    except Exception as e:
        logger.error("Error validating UCF dimensions: %s", e)
        return False


def calculate_universal_coordination_fields(ucf_state: dict) -> dict[str, Any]:
    """
    Produce a set of derived coordination metrics from a UCF state.

    Computes:
    - `performance_score`: overall score derived from the provided UCF dimensions.
    - `field_strength`: the 5th-root geometric mean of harmony, resilience, throughput, focus, and velocity.
    - `harmony_score`: 1.0 minus the variance across those five dimensions, clamped to a minimum of 0.0.
    Includes the original `ucf_state` under the "dimensions" key and a UTC ISO timestamp.

    Parameters:
        ucf_state (dict): UCF state containing the dimensions `harmony`, `resilience`, `throughput`, `focus`, and `velocity` (expected in the range 0.0–1.0).

    Returns:
        dict: A dictionary with keys:
            - "performance_score" (float): 0.0–10.0 overall score.
            - "field_strength" (float): geometric-mean-based field intensity (approximately 0.0–1.0).
            - "harmony_score" (float): balance metric in 0.0–1.0.
            - "dimensions" (dict): the original `ucf_state`.
            - "timestamp" (str): UTC ISO 8601 timestamp (present on success).
        On failure, returns a fallback dictionary containing `performance_score` = 5.0, `field_strength` = 0.5, `harmony_score` = 0.5, and an "error" string describing the failure.
    """
    try:
        performance_score = calculate_performance_score(ucf_state)

        # Calculate field strength (geometric mean of positive dimensions)
        harmony = ucf_state.get("harmony", 0.5)
        resilience = ucf_state.get("resilience", 0.5)
        throughput = ucf_state.get("throughput", 0.5)
        focus = ucf_state.get("focus", 0.5)
        velocity = ucf_state.get("velocity", 0.5)

        # Geometric mean for field strength
        field_strength = (harmony * resilience * throughput * focus * velocity) ** 0.2

        # Calculate harmony score (balance between dimensions)
        dimensions = [harmony, resilience, throughput, focus, velocity]
        mean_val = sum(dimensions) / len(dimensions)
        variance = sum((x - mean_val) ** 2 for x in dimensions) / len(dimensions)
        harmony_score = max(0.0, 1.0 - variance)  # Lower variance = higher harmony

        return {
            "performance_score": performance_score,
            "field_strength": field_strength,
            "harmony_score": harmony_score,
            "dimensions": ucf_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    except Exception as e:
        logger.error("Error calculating universal coordination fields: %s", e)
        return {
            "performance_score": 5.0,
            "field_strength": 0.5,
            "harmony_score": 0.5,
            "error": str(e),
        }


def normalize_coordination_field(value: float) -> float:
    """
    Normalize a coordination field value to the 0.0–1.0 range.

    Clamps the input so that negative values become 0.0 and values
    above 1.0 are capped at 1.0.

    Parameters:
        value: Raw coordination field value.

    Returns:
        Normalized float in [0.0, 1.0].
    """
    return float(max(0.0, min(1.0, value)))
