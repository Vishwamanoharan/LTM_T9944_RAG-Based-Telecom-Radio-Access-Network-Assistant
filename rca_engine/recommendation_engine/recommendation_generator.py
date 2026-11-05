# rca_engine/recommendation_engine/recommendation_generator.py


class RecommendationGenerator:

    RECOMMENDATIONS = {

        "NETWORK_CONGESTION":
            "Perform load balancing and traffic steering",

        "NETWORK_DEGRADATION":
            "Inspect transport network and packet delivery path",

        "RADIO_INTERFERENCE":
            "Investigate interference sources and optimize RF parameters",

        "RADIO_DEGRADATION":
            "Check radio performance and resource allocation",

        "RESOURCE_CONGESTION":
            "Allocate additional PRB resources",

        "PROCESSING_OVERLOAD":
            "Scale compute resources or optimize workloads",

        "CELL_FAILURE":
            "Restart affected cell and inspect alarms",

        "POWER_ISSUE":
            "Inspect power infrastructure and backup systems",

        "BACKHAUL_FAILURE":
            "Restore transport connectivity",

        "UNKNOWN":
            "Further investigation required"
    }

    def generate(
        self,
        root_cause
    ):

        return self.RECOMMENDATIONS.get(
            root_cause,
            self.RECOMMENDATIONS["UNKNOWN"]
        )

    # Backward compatibility
    def generate_recommendation(
        self,
        root_cause
    ):
        return self.generate(
            root_cause
        )