# rca_engine/rca_agent/rca_report_generator.py


from rca_engine.rca_agent.root_cause_engine import (
    RootCauseEngine
)

from rca_engine.rca_agent.confidence_estimator import (
    ConfidenceEstimator
)

from rca_engine.rca_agent.evidence_collector import (
    EvidenceCollector
)

from rca_engine.recommendation_engine.recommendation_generator import (
    RecommendationGenerator
)

from rca_engine.log_analyzer.log_analyzer import (
    LogAnalyzer
)

from rca_engine.log_analyzer.incident_matcher import (
    IncidentMatcher
)


class RCAReportGenerator:

    def __init__(self):

        self.root_cause_engine = (
            RootCauseEngine()
        )

        self.confidence_estimator = (
            ConfidenceEstimator()
        )

        self.evidence_collector = (
            EvidenceCollector()
        )

        self.recommendation_generator = (
            RecommendationGenerator()
        )

        self.log_analyzer = (
            LogAnalyzer()
        )

        self.incident_matcher = (
            IncidentMatcher()
        )

    # =========================================================
    # Generate Single RCA Report
    # =========================================================

    def generate_report(
        self,
        anomaly
    ):

        # -----------------------------------------------------
        # 1. Basic anomaly information
        # -----------------------------------------------------

        tower_id = anomaly.get(
            "tower_id",
            "UNKNOWN"
        )

        anomaly_type = anomaly.get(
            "anomaly_type",
            "UNKNOWN"
        )

        severity = anomaly.get(
            "severity",
            "UNKNOWN"
        )

        metric = anomaly.get(
            "metric",
            ""
        )

        value = anomaly.get(
            "value"
        )

        threshold = anomaly.get(
            "threshold"
        )

        event = anomaly.get(
            "event",
            "NORMAL"
        )

        # -----------------------------------------------------
        # 2. Rule-Based Root Cause
        # -----------------------------------------------------

        rule_based_root_cause = (
            self.root_cause_engine
            .determine_root_cause(
                anomaly
            )
        )

        # -----------------------------------------------------
        # 3. Historical RCA
        # -----------------------------------------------------

        historical_root_cause = (
            self.incident_matcher
            .get_historical_root_cause(
                anomaly
            )
        )

        historical_match = (
            historical_root_cause is not None
        )

        # -----------------------------------------------------
        # 4. Determine Final Root Cause
        #
        # Live event evidence has priority.
        # Historical RCA is used when there is no
        # stronger live event signal.
        # -----------------------------------------------------

        if event != "NORMAL":

            final_root_cause = (
                rule_based_root_cause
            )

        elif historical_root_cause:

            final_root_cause = (
                historical_root_cause
            )

        else:

            final_root_cause = (
                rule_based_root_cause
            )

        # -----------------------------------------------------
        # 5. Confidence
        # -----------------------------------------------------

        confidence = (
            self.confidence_estimator
            .estimate(
                anomaly
            )
        )

        # Historical evidence increases confidence slightly.
        if historical_match:

            confidence = min(
                confidence + 0.05,
                0.99
            )

        # -----------------------------------------------------
        # 6. Base Evidence
        # -----------------------------------------------------

        evidence = (
            self.evidence_collector
            .collect(
                anomaly
            )
        )

        if evidence is None:

            evidence = []

        # -----------------------------------------------------
        # 7. Related TeleLogs
        # -----------------------------------------------------

        related_logs = (
            self.log_analyzer
            .find_related_logs(
                anomaly
            )
        )

        if (
            related_logs is not None
            and not related_logs.empty
        ):

            related_log_count = len(
                related_logs
            )

            evidence.append(
                f"{related_log_count} related "
                "TeleLogs records found"
            )

        else:

            related_log_count = 0

            evidence.append(
                "No related TeleLogs records found"
            )

        # -----------------------------------------------------
        # 8. Historical RCA Evidence
        # -----------------------------------------------------

        if historical_match:

            evidence.append(
                "Historical RCA case matched: "
                f"{historical_root_cause}"
            )

        else:

            evidence.append(
                "No historical RCA case matched"
            )

        # -----------------------------------------------------
        # 9. Evidence Sources
        # -----------------------------------------------------

        evidence_sources = [
            "ANOMALY_DETECTOR"
        ]

        if related_log_count > 0:

            evidence_sources.append(
                "TELELOGS"
            )

        if historical_match:

            evidence_sources.append(
                "HISTORICAL_RCA"
            )

        # -----------------------------------------------------
        # 10. Recommendation
        # -----------------------------------------------------

        recommended_action = (
            self.recommendation_generator
            .generate(
                final_root_cause
            )
        )

        # -----------------------------------------------------
        # 11. Final Report
        # -----------------------------------------------------

        report = {

            "tower_id":
                tower_id,

            "anomaly_type":
                anomaly_type,

            "severity":
                severity,

            "metric":
                metric,

            "value":
                value,

            "threshold":
                threshold,

            "event":
                event,

            "root_cause":
                final_root_cause,

            "rule_based_root_cause":
                rule_based_root_cause,

            "historical_root_cause":
                historical_root_cause,

            "confidence":
                round(
                    confidence,
                    2
                ),

            "evidence":
                evidence,

            "evidence_sources":
                evidence_sources,

            "related_log_count":
                related_log_count,

            "historical_match":
                historical_match,

            "recommended_action":
                recommended_action
        }

        return report

    # =========================================================
    # Generate Multiple RCA Reports
    # =========================================================

    def generate_reports(
        self,
        anomalies
    ):

        reports = []

        for anomaly in anomalies:

            report = self.generate_report(
                anomaly
            )

            reports.append(
                report
            )

        return reports

    # =========================================================
    # Print RCA Report
    # =========================================================

    def print_report(
        self,
        report
    ):

        print()
        print("=" * 60)
        print("RCA REPORT")
        print("=" * 60)

        print(
            f"Tower ID       : "
            f"{report['tower_id']}"
        )

        print(
            f"Anomaly        : "
            f"{report['anomaly_type']}"
        )

        print(
            f"Severity       : "
            f"{report['severity']}"
        )

        print(
            f"Metric         : "
            f"{report['metric']}"
        )

        print(
            f"Value          : "
            f"{report['value']}"
        )

        print(
            f"Event          : "
            f"{report['event']}"
        )

        print(
            f"Root Cause     : "
            f"{report['root_cause']}"
        )

        print(
            f"Confidence     : "
            f"{report['confidence']}"
        )

        print()
        print("Evidence:")

        for item in report["evidence"]:

            print(
                f"  - {item}"
            )

        print()
        print(
            "Recommendation : "
            f"{report['recommended_action']}"
        )

        print(
            "Evidence Source: "
            + ", ".join(
                report["evidence_sources"]
            )
        )

        print("=" * 60)