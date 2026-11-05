# rca_engine/recommendation_engine/action_prioritizer.py


class ActionPrioritizer:

    def __init__(self):

        self.priority_weights = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

    def validate_recommendation(
        self,
        recommendation
    ):

        if not isinstance(
            recommendation,
            dict
        ):
            raise ValueError(
                "Recommendation must be provided as a dictionary."
            )

        required_fields = [
            "tower_id",
            "incident_type",
            "root_cause",
            "recommendation",
            "priority",
            "confidence"
        ]

        for field in required_fields:

            if field not in recommendation:

                raise ValueError(
                    f"Missing required field: {field}"
                )

        return True

    def get_priority_score(
        self,
        priority
    ):

        return self.priority_weights.get(
            priority,
            0
        )

    def calculate_action_score(
        self,
        recommendation
    ):

        priority_score = (
            self.get_priority_score(
                recommendation[
                    "priority"
                ]
            )
        )

        confidence = recommendation.get(
            "confidence",
            "LOW"
        )

        confidence_score = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }.get(
            confidence,
            1
        )

        confidence_value = float(
            recommendation.get(
                "confidence_score",
                0.0
            )
        )

        action_score = (
            priority_score * 0.6
            +
            confidence_score * 0.2
            +
            confidence_value * 0.2
        )

        return round(
            action_score,
            2
        )

    def prioritize_recommendation(
        self,
        recommendation
    ):

        self.validate_recommendation(
            recommendation
        )

        action_score = (
            self.calculate_action_score(
                recommendation
            )
        )

        if action_score >= 3.0:

            action_priority = "IMMEDIATE"

        elif action_score >= 2.0:

            action_priority = "HIGH"

        elif action_score >= 1.0:

            action_priority = "MEDIUM"

        else:

            action_priority = "LOW"

        return {

            "tower_id":
                recommendation[
                    "tower_id"
                ],

            "incident_type":
                recommendation[
                    "incident_type"
                ],

            "root_cause":
                recommendation[
                    "root_cause"
                ],

            "recommendation":
                recommendation[
                    "recommendation"
                ],

            "original_priority":
                recommendation[
                    "priority"
                ],

            "confidence":
                recommendation[
                    "confidence"
                ],

            "confidence_score":
                recommendation.get(
                    "confidence_score",
                    0.0
                ),

            "action_score":
                action_score,

            "action_priority":
                action_priority
        }

    def prioritize_network_actions(
        self,
        recommendations
    ):

        if not isinstance(
            recommendations,
            list
        ):
            raise ValueError(
                "Recommendations must be provided as a list."
            )

        prioritized_actions = []

        for recommendation in recommendations:

            action = (
                self.prioritize_recommendation(
                    recommendation
                )
            )

            prioritized_actions.append(
                action
            )

        prioritized_actions.sort(
            key=lambda item:
                item["action_score"],
            reverse=True
        )

        return prioritized_actions

    def print_prioritized_actions(
        self,
        actions
    ):

        print(
            "\n================================"
        )

        print(
            "RCA ACTION PRIORITIZATION"
        )

        print(
            "================================"
        )

        if not actions:

            print(
                "No actions available."
            )

            return

        for index, action in enumerate(
            actions,
            start=1
        ):

            print(
                f"\nRank: {index}"
            )

            print(
                f"Tower: "
                f"{action['tower_id']}"
            )

            print(
                f"Incident: "
                f"{action['incident_type']}"
            )

            print(
                f"Root Cause: "
                f"{action['root_cause']}"
            )

            print(
                f"Action Priority: "
                f"{action['action_priority']}"
            )

            print(
                f"Original Priority: "
                f"{action['original_priority']}"
            )

            print(
                f"Confidence: "
                f"{action['confidence']}"
            )

            print(
                f"Confidence Score: "
                f"{action['confidence_score']}"
            )

            print(
                f"Action Score: "
                f"{action['action_score']}"
            )

            print(
                f"Action: "
                f"{action['recommendation']}"
            )


if __name__ == "__main__":

    from simulation_engine.kpi_generator.tower_generator import (
        TowerGenerator
    )

    from simulation_engine.kpi_generator.traffic_generator import (
        TrafficGenerator
    )

    from simulation_engine.kpi_generator.kpi_generator import (
        KPIGenerator
    )

    from simulation_engine.event_generator.event_manager import (
        EventManager
    )

    from anomaly_detection.anomaly_engine.anomaly_detector import (
        AnomalyDetector
    )

    from rca_engine.log_analyzer.alarm_parser import (
        AlarmParser
    )

    from rca_engine.log_analyzer.log_analyzer import (
        LogAnalyzer
    )

    from rca_engine.log_analyzer.incident_matcher import (
        IncidentMatcher
    )

    from rca_engine.rca_agent.evidence_collector import (
        EvidenceCollector
    )

    from rca_engine.rca_agent.root_cause_engine import (
        RootCauseEngine
    )

    from rca_engine.rca_agent.confidence_estimator import (
        ConfidenceEstimator
    )

    from rca_engine.recommendation_engine.recommendation_generator import (
        RecommendationGenerator
    )


    # --------------------------------
    # Generate towers
    # --------------------------------

    towers = (
        TowerGenerator()
        .generate_towers()
    )


    # --------------------------------
    # Generate traffic
    # --------------------------------

    traffic = (
        TrafficGenerator()
        .generate_network_traffic(
            towers
        )
    )


    # --------------------------------
    # Generate KPIs
    # --------------------------------

    kpis = (
        KPIGenerator()
        .generate_network_kpis(
            traffic
        )
    )


    # --------------------------------
    # Apply network events
    # --------------------------------

    event_manager = EventManager()

    network_data = (
        event_manager.apply_network_events(
            kpis
        )
    )


    # --------------------------------
    # Detect anomalies
    # --------------------------------

    detector = AnomalyDetector()

    anomalies = (
        detector.detect_network_anomalies(
            network_data
        )
    )


    # --------------------------------
    # Parse alarms
    # --------------------------------

    parser = AlarmParser()

    alarms = (
        parser.parse_anomalies(
            anomalies
        )
    )

    alarms = (
        parser.sort_alarms(
            alarms
        )
    )


    # --------------------------------
    # Analyze alarms
    # --------------------------------

    analyzer = LogAnalyzer()

    summaries = (
        analyzer.analyze_network(
            alarms
        )
    )


    # --------------------------------
    # Match incidents
    # --------------------------------

    matcher = IncidentMatcher()

    incidents = (
        matcher.match_network_incidents(
            summaries
        )
    )


    # --------------------------------
    # Collect evidence
    # --------------------------------

    collector = EvidenceCollector()

    evidence_records = (
        collector.collect_network_evidence(
            network_data,
            alarms,
            incidents
        )
    )


    # --------------------------------
    # Root cause analysis
    # --------------------------------

    root_cause_engine = RootCauseEngine()

    root_causes = (
        root_cause_engine.analyze_network(
            evidence_records
        )
    )


    # --------------------------------
    # Confidence estimation
    # --------------------------------

    estimator = ConfidenceEstimator()

    confidence_results = (
        estimator.estimate_network_confidence(
            root_causes
        )
    )


    # --------------------------------
    # Generate recommendations
    # --------------------------------

    recommendation_generator = (
        RecommendationGenerator()
    )

    recommendations = (
        recommendation_generator
        .generate_network_recommendations(
            confidence_results
        )
    )


    # --------------------------------
    # Prioritize actions
    # --------------------------------

    prioritizer = ActionPrioritizer()

    actions = (
        prioritizer.prioritize_network_actions(
            recommendations
        )
    )


    # --------------------------------
    # Print results
    # --------------------------------

    prioritizer.print_prioritized_actions(
        actions
    )