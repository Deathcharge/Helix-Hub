"""
UCF Dashboard API - Real-time Coordination Metrics
Helix Collective v17.2 - UCF Dashboard
"""

import asyncio
import logging
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..coordination.ucf_protocol import UCFProtocol
from ..coordination.ucf_state_loader import load_ucf_state
from ..coordination.ucf_tracker import UCFTracker

logger = logging.getLogger(__name__)
from ..core.performance_analytics_engine import CoordinationAnalyticsEngine

router = APIRouter()


class UCFMetricsResponse(BaseModel):
    """UCF metrics response model"""

    harmony: float
    resilience: float
    throughput: float
    focus: float
    friction: float
    velocity: float
    phase: str
    timestamp: str
    performance_score: float


class UCFHistoricalResponse(BaseModel):
    """UCF historical data response"""

    timestamp: str
    harmony: float
    resilience: float
    throughput: float
    focus: float
    friction: float
    velocity: float
    phase: str


class UCFAnalyticsResponse(BaseModel):
    """UCF analytics response"""

    current_metrics: UCFMetricsResponse
    trends: dict[str, dict[str, float]]
    predictions: dict[str, float]
    recommendations: list[str]
    health_score: int


class UCFDashboardAPI:
    """UCF Dashboard API endpoints"""

    def __init__(self):
        self.tracker = UCFTracker()
        self.analytics_engine = CoordinationAnalyticsEngine()
        self.last_metrics = None
        self.metrics_cache = {}
        self.cache_ttl = 5  # 5 seconds cache

    async def get_current_metrics(self) -> UCFMetricsResponse:
        """Get current UCF metrics"""
        try:
            cache_key = "current_metrics"
            if cache_key in self.metrics_cache:
                cached_time, cached_data = self.metrics_cache[cache_key]
                if (datetime.now(UTC) - cached_time).total_seconds() < self.cache_ttl:
                    return cached_data

            # Load fresh metrics
            ucf_state = load_ucf_state()

            # Calculate coordination level
            performance_score = self._calculate_performance_score(ucf_state)

            # Determine phase
            phase = UCFProtocol.get_phase(ucf_state.get("harmony", 0.0))

            response = UCFMetricsResponse(
                harmony=ucf_state.get("harmony", 0.0),
                resilience=ucf_state.get("resilience", 0.0),
                throughput=ucf_state.get("throughput", 0.0),
                focus=ucf_state.get("focus", 0.0),
                friction=ucf_state.get("friction", 0.0),
                velocity=ucf_state.get("velocity", 0.0),
                phase=phase,
                timestamp=datetime.now(UTC).isoformat(),
                performance_score=performance_score,
            )

            # Cache the response
            self.metrics_cache[cache_key] = (datetime.now(UTC), response)
            self.last_metrics = response

            return response

        except Exception as e:
            # Return fallback metrics if loading fails
            logger.warning("Failed to load current UCF metrics: %s", e)
            return UCFMetricsResponse(
                harmony=0.0,
                resilience=0.0,
                throughput=0.0,
                focus=0.0,
                friction=0.0,
                velocity=0.0,
                phase="UNKNOWN",
                timestamp=datetime.now(UTC).isoformat(),
                performance_score=0.0,
            )

    async def get_historical_metrics(self, hours: int = 24) -> list[UCFHistoricalResponse]:
        """Get historical UCF metrics"""
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(hours=hours)

            historical_data = self.tracker.get_metrics_range(start_time, end_time)

            response = []
            for record in historical_data:
                response.append(
                    UCFHistoricalResponse(
                        timestamp=record["timestamp"],
                        harmony=record["harmony"],
                        resilience=record["resilience"],
                        throughput=record["throughput"],
                        focus=record["focus"],
                        friction=record["friction"],
                        velocity=record["velocity"],
                        phase=UCFProtocol.get_phase(record["harmony"]),
                    )
                )

            return response

        except Exception as e:
            # Return empty list if no historical data
            logger.warning("Failed to load historical UCF metrics: %s", e)
            return []

    async def get_analytics(self) -> UCFAnalyticsResponse:
        """Get UCF analytics with trends and predictions"""
        try:
            current_metrics = await self.get_current_metrics()

            # Get historical data for trends
            historical = await self.get_historical_metrics(hours=24)

            # Calculate trends
            trends = self._calculate_trends(historical)

            # Generate predictions
            predictions = self._generate_predictions(current_metrics, trends)

            # Get recommendations
            recommendations = self._generate_recommendations(current_metrics, trends)

            # Calculate health score
            health_score = self._calculate_health_score(current_metrics)

            return UCFAnalyticsResponse(
                current_metrics=current_metrics,
                trends=trends,
                predictions=predictions,
                recommendations=recommendations,
                health_score=health_score,
            )

        except Exception as e:
            # Return fallback analytics
            logger.warning("Failed to compute UCF analytics: %s", e)
            fallback_metrics = UCFMetricsResponse(
                harmony=0.0,
                resilience=0.0,
                throughput=0.0,
                focus=0.0,
                friction=0.0,
                velocity=0.0,
                phase="UNKNOWN",
                timestamp=datetime.now(UTC).isoformat(),
                performance_score=0.0,
            )

            return UCFAnalyticsResponse(
                current_metrics=fallback_metrics,
                trends={},
                predictions={},
                recommendations=["UCF analytics temporarily unavailable"],
                health_score=0,
            )

    async def get_realtime_stream(self):
        """Stream real-time UCF metrics updates"""
        while True:
            try:
                metrics = await self.get_current_metrics()

                # Only send if metrics changed significantly
                if (
                    self.last_metrics is None
                    or abs(metrics.performance_score - self.last_metrics.performance_score) > 0.01
                ):
                    yield {
                        "type": "ucf_update",
                        "data": metrics.dict(),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }

                    self.last_metrics = metrics

                await asyncio.sleep(1)  # Update every second

            except Exception as e:
                # Log error but continue streaming
                yield {
                    "type": "error",
                    "message": f"Error in UCF stream: {e!s}",
                    "timestamp": datetime.now(UTC).isoformat(),
                }
                await asyncio.sleep(5)

    def _calculate_performance_score(self, ucf_state: dict[str, float]) -> float:
        """Calculate overall coordination level from UCF metrics"""
        try:
            weights = {
                "harmony": 0.3,
                "resilience": 0.25,
                "throughput": 0.2,
                "focus": 0.15,
                "velocity": 0.05,
                "friction": -0.05,  # Negative weight for friction
            }

            total_weight = sum(weights.values())
            weighted_sum = sum(ucf_state.get(metric, 0.0) * weight for metric, weight in weights.items())

            return max(0.0, min(1.0, weighted_sum / total_weight))

        except (ValueError, TypeError, KeyError, IndexError):
            return 0.5

    def _calculate_trends(self, historical: list[UCFHistoricalResponse]) -> dict[str, dict[str, float]]:
        """Calculate trends from historical data"""
        if len(historical) < 2:
            return {}

        trends = {}
        metrics = ["harmony", "resilience", "throughput", "focus", "friction", "velocity"]

        for metric in metrics:
            values = [getattr(record, metric) for record in historical]

            # Calculate trend (slope)
            n = len(values)
            x_values = list(range(n))

            # Simple linear regression
            x_mean = sum(x_values) / n
            y_mean = sum(values) / n

            numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))

            slope = numerator / denominator if denominator != 0 else 0

            # Calculate momentum (rate of change)
            momentum = (values[-1] - values[0]) / n if n > 0 else 0

            trends[metric] = {
                "slope": slope,
                "momentum": momentum,
                "direction": ("up" if slope > 0.001 else "down" if slope < -0.001 else "stable"),
                "change_24h": values[-1] - values[0] if len(values) > 0 else 0,
            }

        return trends

    def _generate_predictions(self, current: UCFMetricsResponse, trends: dict) -> dict[str, float]:
        """Generate short-term predictions"""
        predictions = {}

        for metric, trend_data in trends.items():
            current_value = getattr(current, metric)
            # Simple linear prediction for next hour
            predicted_change = trend_data["slope"] * 60  # 60 minutes
            predicted_value = current_value + predicted_change

            predictions[metric] = max(0.0, min(2.0, predicted_value))

        return predictions

    def _generate_recommendations(self, current: UCFMetricsResponse, trends: dict) -> list[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Check coordination level
        if current.performance_score < 0.3:
            recommendations.append("⚠️ Critical: Coordination level very low. Consider system reset.")
        elif current.performance_score < 0.5:
            recommendations.append("⚠️ Warning: Coordination level below optimal. Monitor closely.")

        # Check individual metrics
        if current.harmony < 0.3:
            recommendations.append("🎵 Low harmony detected. Consider running Harmony Restoration cycle.")

        if current.resilience < 0.8:
            recommendations.append("🛡️ Resilience low. System may be vulnerable to disruptions.")

        if current.friction > 0.3:
            recommendations.append("🔥 High friction detected. System stress elevated.")

        # Check trends
        if trends.get("harmony", {}).get("direction") == "down":
            recommendations.append("📉 Harmony trending downward. Investigate potential issues.")

        if trends.get("resilience", {}).get("direction") == "down":
            recommendations.append("🛡️ Resilience declining. Consider defensive measures.")

        # Positive recommendations
        if current.performance_score > 0.8:
            recommendations.append("✨ Excellent: Coordination level optimal. Consider expansion.")

        if not recommendations:
            recommendations.append("✅ All metrics within normal ranges.")

        return recommendations

    def _calculate_health_score(self, current: UCFMetricsResponse) -> int:
        """Calculate overall system health score (0-100)"""
        # Base score from coordination level
        score = current.performance_score * 100

        # Adjustments based on individual metrics
        if current.harmony < 0.4:
            score -= 10
        if current.resilience < 0.8:
            score -= 5
        if current.friction > 0.2:
            score -= 10
        if current.focus < 0.3:
            score -= 5

        # Phase adjustments
        if current.phase == "COHERENT":
            score += 10
        elif current.phase == "ENTROPIC":
            score -= 15
        elif current.phase == "CHAOTIC":
            score -= 25

        return max(0, min(100, int(score)))


# Initialize the API
ucf_dashboard_api = UCFDashboardAPI()

# API Endpoints


@router.get("/api/ucf/current", response_model=UCFMetricsResponse)
async def get_current_ucf_metrics():
    """Get current UCF metrics"""
    return await ucf_dashboard_api.get_current_metrics()


@router.get("/api/ucf/historical", response_model=list[UCFHistoricalResponse])
async def get_historical_ucf_metrics(hours: int = 24):
    """Get historical UCF metrics"""
    if hours < 1 or hours > 168:  # Max 1 week
        raise HTTPException(status_code=400, detail="Hours must be between 1 and 168")

    return await ucf_dashboard_api.get_historical_metrics(hours)


@router.get("/api/ucf/analytics", response_model=UCFAnalyticsResponse)
async def get_ucf_analytics():
    """Get UCF analytics with trends and predictions"""
    return await ucf_dashboard_api.get_analytics()


@router.get("/api/ucf/health")
async def get_system_health():
    """Get overall system health status"""
    try:
        current = await ucf_dashboard_api.get_current_metrics()
        health_score = ucf_dashboard_api._calculate_health_score(current)

        return {
            "health_score": health_score,
            "status": ("CRITICAL" if health_score < 30 else "WARNING" if health_score < 70 else "HEALTHY"),
            "timestamp": datetime.now(UTC).isoformat(),
            "metrics_summary": {
                "performance_score": current.performance_score,
                "phase": current.phase,
                "harmony": current.harmony,
                "resilience": current.resilience,
            },
        }
    except Exception as e:
        logger.error("UCF health calculation failed: %s", e)
        return {
            "health_score": 0,
            "status": "UNKNOWN",
            "error": "Health calculation failed",
            "timestamp": datetime.now(UTC).isoformat(),
        }


@router.get("/api/ucf/trends")
async def get_ucf_trends():
    """Get UCF trends analysis"""
    try:
        historical = await ucf_dashboard_api.get_historical_metrics(hours=24)
        trends = ucf_dashboard_api._calculate_trends(historical)

        return {
            "trends": trends,
            "analysis": {
                "overall_direction": (
                    "improving"
                    if any(t["slope"] > 0.001 for t in trends.values())
                    else ("declining" if any(t["slope"] < -0.001 for t in trends.values()) else "stable")
                ),
                "metrics_at_risk": [k for k, v in trends.items() if v["direction"] == "down"],
                "metrics_improving": [k for k, v in trends.items() if v["direction"] == "up"],
                "timestamp": datetime.now(UTC).isoformat(),
            },
        }
    except Exception as e:
        logger.error("UCF trend analysis failed: %s", e)
        return {
            "trends": {},
            "analysis": {
                "error": "Trend analysis failed",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        }


@router.get("/api/ucf/recommendations")
async def get_ucf_recommendations():
    """Get UCF-based recommendations"""
    try:
        historical = await ucf_dashboard_api.get_historical_metrics(hours=24)
        trends = ucf_dashboard_api._calculate_trends(historical)
        current = await ucf_dashboard_api.get_current_metrics()
        recommendations = ucf_dashboard_api._generate_recommendations(current, trends)

        return {
            "recommendations": recommendations,
            "priority": (
                "high" if current.performance_score < 0.3 else "medium" if current.performance_score < 0.6 else "low"
            ),
            "timestamp": datetime.now(UTC).isoformat(),
        }
    except Exception as e:
        logger.error("UCF recommendations generation failed: %s", e)
        return {
            "recommendations": ["Unable to generate recommendations at this time"],
            "priority": "unknown",
            "error": "Recommendations generation failed",
            "timestamp": datetime.now(UTC).isoformat(),
        }
